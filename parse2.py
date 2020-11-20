from boatlib.data import Parser
import sys
import pprint
import os
import shutil

from collections import defaultdict

base_path = f'/home/rcfox/.local/share/Steam/steamapps/common/Alvora Tactics/Content/Data/'

seen = set()

for directory, _, filenames in os.walk(base_path):
    for filename in filenames:
        if not filename.endswith('.txt'):
            continue
        path = os.path.join(directory, filename)
        print(path)
        with open(path) as f:
            for item in Parser.parse(f.read()):
                for value in item.values():
                    if isinstance(value, list):
                        seen.update(value)
                    else:
                        seen.add(value)

palettes = {}
with open('/home/rcfox/Mods/AlvoraReturns/compat.txt') as f:
    for item in Parser.parse(f.read()):
        palettes[item['ID']] = item['num']

needed = set(palettes.keys()).intersection(seen)
print(needed)
print(len(needed))
