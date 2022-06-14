#!/bin/bash
FILES="./testes-takuzu/inputs/*"
for f in $FILES
do
    echo "Testing $f..."

    python3 takuzu.py < $f
done
echo "Done."