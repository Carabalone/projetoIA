#!/bin/bash
FILES="./testes-takuzu/inputs/*"
for f in $FILES
do
    echo "Testing $f..."

    time (python3 takuzu.py < $f) | echo
done
echo "Done."