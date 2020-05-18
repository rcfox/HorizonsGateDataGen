#!/bin/sh
set -x
for script in generate*.sh; do
    sh $script
done
