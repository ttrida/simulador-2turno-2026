# Pipeline TSE -> Parquet (DuckDB). Uso: python3 pipeline/build.py <dir_csvs>
import sys, duckdb, json
src = sys.argv[1]
con = duckdb.connect()
con.execute(f"""
CREATE TABLE v AS SELECT * FROM read_csv('{src}/votacao_candidato_munzona_2026_*.csv',
  delim=';', header=true, encoding='latin-1', all_varchar=true, union_by_name=true, filename=true)
WHERE filename NOT LIKE '%BRASIL%'""")
con.execute("""COPY (SELECT ANO_ELEICAO::INT ano, NR_TURNO::INT turno, SG_UF uf, CD_MUNICIPIO::INT cd_mun,
  NM_MUNICIPIO municipio, NR_ZONA::INT zona, DS_CARGO cargo, NR_CANDIDATO::INT nr, NM_URNA_CANDIDATO candidato,
  SG_PARTIDO partido, QT_VOTOS_NOMINAIS_VALIDOS::BIGINT votos FROM v)
  TO 'data/votacao_munzona_2026.parquet' (FORMAT parquet, COMPRESSION zstd)""")
p = "read_parquet('data/votacao_munzona_2026.parquet')"
pres = f"FROM {p} WHERE cargo='Presidente' AND turno=1"
uf = con.execute(f"SELECT uf, candidato, partido, sum(votos) v {pres} GROUP BY ALL ORDER BY uf, v DESC").fetchall()
mun = con.execute(f"SELECT uf, cd_mun, municipio, candidato, sum(votos) v {pres} GROUP BY ALL").fetchall()
con.execute(f"COPY (SELECT uf, cd_mun, municipio, candidato, partido, sum(votos) votos {pres} GROUP BY ALL) TO 'data/presidente_1t_mun.parquet' (FORMAT parquet)")
out = {}
for u,c,pt,v in uf: out.setdefault(u, {})[f"{c} ({pt})"] = v
json.dump(out, open('data/presidente_1t_uf.json','w'), ensure_ascii=False)
print(con.execute(f"SELECT candidato, partido, sum(votos) v {pres} GROUP BY ALL ORDER BY v DESC").fetchall())
