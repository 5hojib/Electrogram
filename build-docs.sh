#!/bin/bash

export DOCS_KEY
VENV="$(pwd)/venv"
export VENV

if [[ "$(echo "$GITHUB_REF" | cut -d '/' -f "1 2")" == "refs/tags" ]]; then
    branch="dev"
elif [[ "$GITHUB_REF" == "refs/heads/err" ]]; then
    branch="err"
else
    b="$(echo "$GITHUB_REF" | cut -d '/' -f '3 4')"
    if [[ $(echo "$b" | cut -d '/' -f 1) == "dev" ]]; then
        b="$(echo "$b" | cut -d '/' -f 2)"
        if [[ "$b" =~ ^[0-9]\.[0-9]\.x ]]; then
            branch="$b"
        else
            exit 0
        fi
    else
        exit 0
    fi
fi

make clean
make clean-docs
make venv
make api
"$VENV/bin/pip" install -e '.[docs]'

cd compiler/docs || exit 1
"$VENV/bin/python" compiler.py
cd ../.. || exit 1

"$VENV/bin/sphinx-build" -b html "docs/source" "docs/build/html" -j auto

git clone https://5hojib:"$DOCS_KEY"@github.com/5hojib/Electrogram-docs.git
cd Electrogram-docs || exit 1

mkdir -p "$branch"
cd "$branch" || exit 1

rm -rf _includes api genindex.html intro py-modindex.html sitemap.xml \
       support.html topics _static faq index.html objects.inv \
       searchindex.js start telegram

cp -r ../../docs/build/html/* .

git config --local user.name "5hojib"
git config --local user.email "yesiamshojib@gmail.com"

git add --all
git commit -a -m "docs: $branch: Update docs $(date '+%Y-%m-%d | %H:%m:%S %p %Z')" --signoff
git push -u origin --all
