# Injeta os dados no template -> site/index.html e index.html (raiz, GitHub Pages)
import datetime, shutil
t = open('site/template.html').read()
upd = datetime.datetime.now().strftime('%d/%m %H:%M')
for k, f in [('__DATA__', 'data/uf_compact.json'), ('__MUN__', 'data/mun_compact.json'), ('__POLLS__', 'data/pesquisas.json'), ('__IND__', 'data/mun_ind.json')]:
    t = t.replace(k, open(f).read())
open('site/index.html', 'w').write(t.replace('__UPD__', upd))
shutil.copy('site/index.html', 'index.html')
shutil.copy('site/br_municipios.topo.json', 'br_municipios.topo.json')
