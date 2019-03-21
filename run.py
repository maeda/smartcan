#!/home/pi/trashclassifier/venv/bin/python

import sys
from time import sleep


def get_app(app_name):
    print(app_name)
    module = __import__('embedded_app')
    class_ = getattr(module, app_name)

    return class_()


if __name__ == '__main__':

    args = sys.argv

    print(args)

    app = get_app(args[1])

    while True:
        app.run()
        sleep(.1)
