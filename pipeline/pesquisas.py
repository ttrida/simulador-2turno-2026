# Monta data/pesquisas.json: todas as rodadas pós-1º turno, válidos, última rodada por instituto e valor PNAD (Arvor)
import csv, json
rows = list(csv.DictReader(open('data/pesquisas_raw.tsv'), delimiter='\t'))
arvor = json.load(open('data/arvor_reponderacao.json'))['polls']
key = lambda s: s.lower().split('/')[0].split()[0].replace('á', 'a')
pn = {(key(p['instituto']), p['campo']['fim']): 100*p['pnad']['flavio']/(p['pnad']['flavio']+p['pnad']['lula']) for p in arvor}
out, seen = [], set()
for r in sorted(rows, key=lambda r: r['fim'], reverse=True):
    fv = float(r['fV']) if r['fV'] else 100*float(r['fT'])/(float(r['fT'])+float(r['lT']))
    k = key(r['instituto'])
    p = pn.get((k, r['fim'])) or (pn.get((k, '2026-10-14')) if k == 'datafolha' and r['fim'] == '2026-10-14' else None)
    out.append({"instituto": r['instituto'], "campo_inicio": r['inicio'], "campo_fim": r['fim'], "divulgacao": r['divulg'] or None,
                "flavio_validos": round(fv, 2), "flavio_total": float(r['fT']) if r['fT'] else None, "lula_total": float(r['lT']) if r['lT'] else None,
                "flavio_pnad": round(p, 2) if p else None, "n": int(r['n']) if r['n'] else None, "margem": float(r['margem']) if r['margem'] else None,
                "ultima": k not in seen, "fonte": r['fonte'], "obs": r['obs']})
    seen.add(k)
json.dump(out, open('data/pesquisas.json', 'w'), ensure_ascii=False, indent=1)
for o in out:
    if o['ultima']: print(f"{o['instituto']:24}{o['campo_fim']}  {o['flavio_validos']:6}  {o['flavio_pnad']}")
