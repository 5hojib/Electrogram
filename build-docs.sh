#!/bin/bash

export DOCS_KEY
VENV="$(pwd)/venv"
export VENV

make clean
make clean-docs
make venv
make api
"$VENV/bin/pip" install -e '.[docs]'

cd compiler/docs
"$VENV/bin/python" compiler.py
cd ../..

"$VENV/bin/sphinx-build" -b html "docs/source" "docs/build/html" -j auto

git clone https://5hojib:"$DOCS_KEY"@github.com/5hojib/Electrogram-docs.git
cd Electrogram-docs

mkdir -p main
cd main

rm -rf _includes api genindex.html intro py-modindex.html sitemap.xml \
       support.html topics _static faq index.html objects.inv \
       searchindex.js start telegram

cp -r ../../docs/build/html/* .

git config --local user.name "5hojib"
git config --local user.email "yesiamshojib@gmail.com"
git add --all
git commit -m "Update docs" --signoff
git checkout --orphan x
git commit -m "Update docs" --signoff
git branch -D main
git branch -m main
git push --force origin main
