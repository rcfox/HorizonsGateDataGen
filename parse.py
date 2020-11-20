from boatlib.data import Parser
import sys
import pprint
import os
import shutil

from collections import defaultdict

items = {}

for game in ('Alvora Tactics', "Horizon's Gate"):
    items[game] = defaultdict(dict)
    base_path = f'/home/rcfox/.local/share/Steam/steamapps/common/{game}/Content/Data/SystemData/Definitions/level/'
    for directory, _, filenames in os.walk(base_path):
        for filename in filenames:
            path = os.path.join(directory, filename)
            print(path)
            with open(path) as f:
                for item in Parser.parse(f.read()):
                    t = item['__type__']
                    i = item['ID']
                    print(t, i)
                    items[game][t][i] = item


for item_type in items['Alvora Tactics'].keys():
    a = set(items['Alvora Tactics'][item_type])
    b = set(items["Horizon's Gate"][item_type])

    print('\n\n', item_type)
    print('Alvora only:', a - b)
    print('\nHorizon only:', b - a)


a = set(items['Alvora Tactics']['SetPiece'])
b = set(items["Horizon's Gate"]['SetPiece'])

game = 'Alvora Tactics'
for spid in a - b:
    for sp_file in [f'/home/rcfox/.local/share/Steam/steamapps/common/{game}/Content/Data/ZoneData/{spid}.txt',
                    f'/home/rcfox/.local/share/Steam/steamapps/common/{game}/Content/Data/ZoneData/{spid}.png']:
        if os.path.exists(sp_file):
            shutil.copy2(sp_file, f'/home/rcfox/Mods/AlvoraReturns/SetPieces/{os.path.basename(sp_file)}')
        else:
            print(spid)
