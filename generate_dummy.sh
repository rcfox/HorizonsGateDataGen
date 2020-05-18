#!/bin/sh

mkdir -p rcfox_dummy

rm rcfox_dummy.zip

python -m dummy > rcfox_dummy/rcfox_dummy.txt
zip -r rcfox_dummy.zip rcfox_dummy
