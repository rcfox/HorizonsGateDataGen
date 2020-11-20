from boatlib.data import Parser
import sys
import pprint
import os
import shutil

from collections import defaultdict

from pprint import pprint
from PIL import Image

palettes = {
    'Alvora': {
        'filename': f'/home/rcfox/.local/share/Steam/steamapps/common/Alvora Tactics/Content/Images/Palettes/palettes.png',
        'colours': [],
        'used': set(),
    },
    'Horizon': {
        'filename': f"/home/rcfox/.local/share/Steam/steamapps/common/Horizon's Gate/Content/Images/Palettes/palettes.png",
        'colours': [],
        'used': set(),
    }
}

def used_alvora_palettes():
    base_path = f'/home/rcfox/.local/share/Steam/steamapps/common/Alvora Tactics/Content/Data/'

    seen = set()

    for directory, _, filenames in os.walk(base_path):
        for filename in filenames:
            if not filename.endswith('.txt'):
                continue
            path = os.path.join(directory, filename)
            with open(path) as f:
                for item in Parser.parse(f.read()):
                    for value in item.values():
                        if isinstance(value, list):
                            seen.update(value)
                        else:
                            seen.add(value)

    palettes = {}
    with open('/home/rcfox/Mods/AlvoraReturns/orig.txt') as f:
        for item in Parser.parse(f.read()):
            palettes[item['ID']] = item['num']

    needed = set(palettes.keys()).intersection(seen)
    return {key: palettes[key] for key in needed}

def parse_palettes():
    for game, palette in palettes.items():
        img = Image.open(palette['filename'])

        for y in range(0, img.height, 4):
            for x in range(img.width):
                used = palette['used']
                p = tuple(img.getpixel((x,y+i)) for i in range(4))
                used.add(p)
                palette['colours'].append(p)


def find_unused_spot(img):
    unused_colours = (
        ((255, 0, 250, 255), (255, 0, 250, 255), (255, 0, 250, 255), (255, 0, 250, 255)),
        ((0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0))
    )
    num = 32
    for y in range(4, img.height, 4):
        for x in range(img.width):
            p = tuple(img.getpixel((x,y+i)) for i in range(4))
            if p in unused_colours:
                return num
            num += 1
    raise Exception('full!!')

def add_to_palette(img, num, colours):
    x = num % 32
    y = num // 32 * 4
    for i, c in enumerate(colours):
        img.putpixel((x, y+i), c)

parse_palettes()
dest_img = Image.open(palettes['Horizon']['filename']).copy()

mappings = {}

for name, num in used_alvora_palettes().items():
    c = palettes['Alvora']['colours'][num]

    new_num = -1
    if c in palettes['Horizon']['used']:
        new_num = palettes['Horizon']['colours'].index(c)
    else:
        new_num = find_unused_spot(dest_img)
        add_to_palette(dest_img, new_num, c)

    mappings[name] = new_num


dest_img.save('/home/rcfox/Mods/AlvoraReturns/palettes.png')

for name, num in mappings.items():
    print(f'[Palette] ID={name}; num={num};')
    
