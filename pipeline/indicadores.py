# Indicadores municipais: abstenção 1T (TSE), IDHM e renda per capita (Atlas Brasil/Censo 2010, via Ipeadata), PIB per capita (IBGE 2023 / Censo 2022)
# Uso: python3 pipeline/indicadores.py <dir_detalhe_tse> <loc.json> <idhm.json> <rdpc.json> <pib.json> <pop.json>
import sys, json, duckdb
det, loc, idhm, rdpc, pib, pop = sys.argv[1:7]
sys.path.insert(0, 'pipeline')
con = duckdb.connect()
con.execute(f"""COPY (SELECT SG_UF uf, CD_MUNICIPIO::INT cd_mun, NM_MUNICIPIO municipio,
  sum(QT_APTOS::BIGINT) aptos, sum(QT_COMPARECIMENTO::BIGINT) comparec, sum(QT_ABSTENCOES::BIGINT) abst
  FROM read_csv('{det}/detalhe_votacao_munzona_2026_*.csv', delim=';', header=true, encoding='latin-1', all_varchar=true, union_by_name=true, filename=true)
  WHERE filename NOT LIKE '%BRASIL%' AND DS_CARGO='Presidente' AND NR_TURNO='1' GROUP BY ALL)
  TO 'data/comparecimento_1t_mun.parquet' (FORMAT parquet)""")
from municipios_match import match
ab = match(con.execute("SELECT uf, municipio, aptos, abst FROM 'data/comparecimento_1t_mun.parquet' WHERE uf<>'ZZ'").fetchall(), json.load(open(loc)))
ipea = lambda f: {v['TERCODIGO']: v['VALVALOR'] for v in json.load(open(f))['value'] if v['VALDATA'].startswith('2010') and v['NIVNOME'] == 'Municípios'}
I, R = ipea(idhm), ipea(rdpc)
P = {r['D1C']: float(r['V']) for r in json.load(open(pib))[1:] if r['V'] not in ('-', '...', 'X')}
POP = {r['D1C']: float(r['V']) for r in json.load(open(pop))[1:] if r['V'] not in ('-', '...', 'X')}
out = {}
for code, (apt, abst) in ab.items():
    pc = P[code] * 1000 / POP[code] if code in P and POP.get(code) else None
    out[code] = [apt, round(abst / apt * 100, 2), I.get(code), R.get(code), round(pc) if pc else None]
json.dump(out, open('data/mun_ind.json', 'w'), separators=(',', ':'))
nat = con.execute("SELECT sum(aptos), sum(abst) FROM 'data/comparecimento_1t_mun.parquet'").fetchone()
print(len(out), 'municípios; abstenção nacional', round(nat[1] / nat[0] * 100, 2), '%; idhm', sum(v[2] is not None for v in out.values()), 'renda', sum(v[3] is not None for v in out.values()), 'pib', sum(v[4] is not None for v in out.values()))
