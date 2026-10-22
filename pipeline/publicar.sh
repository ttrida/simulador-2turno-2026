#!/bin/sh
# Atualização diária: regenera a página e publica no GitHub Pages
python3 pipeline/render.py
git add -A && git commit -m "Atualização $(date '+%d/%m %H:%M')" && git push
