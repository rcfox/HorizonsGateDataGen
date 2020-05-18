import boatlib.data
from . import plants
from . import tools
from . import dialogs

if __name__ == '__main__':
    with boatlib.data.collect_records() as c:
        boatlib.data.Comment('''
        Horizon's Gate Farming Mod
        Version: 1.1
        By: rcfox (https://github.com/rcfox/HorizonsGateMods)
        Crop sprites by: josehzz (https://opengameart.org/content/farming-crops-16x16)
        ''')
        tools.define_tools()
        plants.define_plants()
        dialogs.define_dialogs()
        print(c.serialize())
