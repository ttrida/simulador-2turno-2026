# Casamento de municípios TSE x IBGE por UF + nome normalizado (com aliases de grafia)
import re, unicodedata
norm = lambda s: re.sub(r"[^A-Z]", "", unicodedata.normalize("NFKD", s.upper()).encode("ascii", "ignore").decode())
ALIAS = {("PR","MUNHOZDEMELLO"):"MUNHOZDEMELO",("RN","BOASAUDE"):"JANUARIOCICCO",("PA","ELDORADODOSCARAJAS"):"ELDORADODOCARAJAS",
 ("MG","BARAODEMONTEALTO"):"BARAODOMONTEALTO",("MG","SAOTHOMEDASLETRAS"):"SAOTOMEDASLETRAS",("MG","DONAEUSEBIA"):"DONAEUZEBIA",
 ("RO","ESPIGAODOOESTE"):"ESPIGAODOESTE",("SE","AMPARODESAOFRANCISCO"):"AMPARODOSAOFRANCISCO",("GO","BOMJESUS"):"BOMJESUSDEGOIAS",
 ("MT","SANTOANTONIODOLEVERGER"):"SANTOANTONIODELEVERGER",("RR","SAOLUIZ"):"SAOLUIZDOANAUA",("RO","ALVORADADOOESTE"):"ALVORADADOESTE",
 ("SP","SAOLUISDOPARAITINGA"):"SAOLUIZDOPARAITINGA"}
def match(rows, loc):
    """rows: (uf, nome_tse, *valores) -> {codigo_ibge: valores}"""
    ibge = {(m["UF-sigla"], norm(m["municipio-nome"])): str(m["municipio-id"]) for m in loc}
    out = {}
    for uf, nm, *vals in rows:
        code = ibge.get((uf, ALIAS.get((uf, norm(nm)), norm(nm))))
        if code: out[code] = tuple(vals)
    return out
