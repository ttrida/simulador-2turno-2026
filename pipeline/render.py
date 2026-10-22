# Injeta os dados no template -> site/index.html
import json, datetime
t=open('site/template.html').read()
d=open('data/uf_compact.json').read()
open('site/index.html','w').write(t.replace('__DATA__',d).replace('__UPD__',datetime.datetime.now().strftime('%d/%m %H:%M')))
