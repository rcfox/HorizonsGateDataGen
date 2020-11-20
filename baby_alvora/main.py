import boatlib.data
from . import dialog

if __name__ == '__main__':
    with boatlib.data.collect_records() as c:
        dialog.define_dialogs()
        print(c.serialize())
