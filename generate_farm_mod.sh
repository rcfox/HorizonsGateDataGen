#!/bin/sh

mkdir -p rcfox_farming

rm rcfox_farming.zip

python -m farm_mod.main > rcfox_farming/rcfox_farming.txt
cp farm_mod/*.png rcfox_farming
zip -r rcfox_farming.zip rcfox_farming
