import boatlib.data
import plants
import tools
import dialogs

if __name__ == '__main__':
    with boatlib.data.collect_records() as c:
        tools.define_tools()
        plants.define_plants()
        dialogs.define_dialogs()
        print(c.serialize())
