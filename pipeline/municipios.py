# Cruza municípios TSE x IBGE por nome+UF e gera data/mun_compact.json
import sys, json, unicodedata, re, duckdb
loc = json.load(open(sys.argv[1]))
norm = lambda s: re.sub(r"[^A-Z]", "", unicodedata.normalize("NFKD", s.upper()).encode("ascii","ignore").decode())
ibge = {(m["UF-sigla"], norm(m["municipio-nome"])): m for m in loc}
ALIAS = {("PR","MUNHOZDEMELLO"):"MUNHOZDEMELO",("RN","BOASAUDE"):"JANUARIOCICCO",("PA","ELDORADODOSCARAJAS"):"ELDORADODOCARAJAS",
 ("MG","BARAODEMONTEALTO"):"BARAODOMONTEALTO",("MG","SAOTHOMEDASLETRAS"):"SAOTOMEDASLETRAS",("MG","DONAEUSEBIA"):"DONAEUZEBIA",
 ("RO","ESPIGAODOOESTE"):"ESPIGAODOESTE",("SE","AMPARODESAOFRANCISCO"):"AMPARODOSAOFRANCISCO",("GO","BOMJESUS"):"BOMJESUSDEGOIAS",
 ("MT","SANTOANTONIODOLEVERGER"):"SANTOANTONIODELEVERGER",("RR","SAOLUIZ"):"SAOLUIZDOANAUA",("RO","ALVORADADOOESTE"):"ALVORADADOESTE",
 ("SP","SAOLUISDOPARAITINGA"):"SAOLUIZDOPARAITINGA"}  # (uf, nome TSE normalizado) -> nome IBGE normalizado, para grafias divergentes
rows = duckdb.sql("""SELECT uf, cd_mun, municipio,
  sum(votos) FILTER (candidato='FLAVIO BOLSONARO') f, sum(votos) FILTER (candidato='LULA') l,
  sum(votos) FILTER (candidato='ESCRITOR AUGUSTO CURY') c, sum(votos) FILTER (candidato='RENAN SANTOS') r,
  sum(votos) FILTER (candidato='RONALDO CAIADO') k, sum(votos) t
  FROM 'data/presidente_1t_mun.parquet' WHERE uf<>'ZZ' GROUP BY ALL""").fetchall()
out, miss = {}, []
for uf, cd, nm, f, l, c, r, k, t in rows:
    key = (uf, ALIAS.get((uf, norm(nm)), norm(nm)))
    m = ibge.get(key)
    if not m: miss.append((uf, nm)); continue
    out[str(m["municipio-id"])] = [nm.title(), uf, m["regiao-sigla"], f or 0, l or 0, c or 0, r or 0, k or 0, t]
json.dump(out, open("data/mun_compact.json", "w"), ensure_ascii=False, separators=(",", ":"))
print(len(out), "ok;", len(miss), "sem match:", miss)
