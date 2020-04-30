import boatlib.data
import plants
import tools

if __name__ == '__main__':
    with boatlib.data.collect_records() as c:
        tools.define_tools()
        plants.define_plants()
        print(c.serialize())
