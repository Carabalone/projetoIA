#!/bin/bash
INPUTS=(./testes-takuzu/inputs/*)
OUTPUTS=(./testes-takuzu/outputs/*)

for f in ${!INPUTS[@]}
do
    echo "Testing ${INPUTS[$f]}..."

    python3 takuzu.py < ${INPUTS[$f]}
done
echo "Done."