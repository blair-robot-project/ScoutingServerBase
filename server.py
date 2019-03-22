from _thread import interrupt_main
# noinspection PyProtectedMember
from os import _exit as osexit
from threading import Thread

import printing
import datactl
import socketctl
from header import print_header


def main():
    print_header()

    datactl.makefile()

    printing.printf('Waiting for connections', style=printing.STATUS)

    Thread(target=handleinput).start()

    socketctl.init()
    Thread(target=socketctl.connect).start()

    while True:
        try:
            datactl.update()
        except KeyboardInterrupt:
            datactl.update()
            socketctl.close()
            osexit(1)


def handleinput():
    i = input()
    if i in ('q', 'quit'):
        printing.printf('Are you sure you want to quit? (y/n)', style=printing.QUIT, end=' ')
        q = input()
        if q == 'y':
            interrupt_main()
    elif i in ('d', 'data', 'drive', 'flash drive', 'u', 'update', 'dump', 'data dump'):
        datactl.driveupdaterequest()
    elif i in ('s', 'strat', 'match strat', 'strategy', 'match strategy'):
        # noinspection PyUnusedLocal
        teams = [input("Our alliance: ") for i in range(3)] + [input("Other alliance: ") for i in range(3)]
        printing.printf(datactl.getdata(teams), style=printing.DATA_OUTPUT)
    Thread(target=handleinput).start()


if __name__ == '__main__':
    main()
