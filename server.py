from _thread import interrupt_main
# noinspection PyProtectedMember
from os import _exit as osexit
from threading import Thread

import datactl
import socketctl
from header import print_header


def main():
    print_header()

    datactl.makefile()

    print('Waiting for connections')

    Thread(target=handleinput).start()

    Thread(target=socketctl.connect).start()

    running = True
    while running:
        try:
            datactl.update()
        except KeyboardInterrupt:
            q = input('Are you sure you want to quit? (y/n) ')
            if q == 'y':
                datactl.update()
                socketctl.close()
                running = False
                osexit(1)


def handleinput():
    i = input()
    if i == 'q' or i == 'quit':
        interrupt_main()
    else:
        if i == 's':
            # noinspection PyUnusedLocal
            teams = [input("Our alliance: ") for i in range(3)] + [input("Other alliance: ") for i in range(3)]
            print(datactl.getdata(teams))
        Thread(target=handleinput).start()


if __name__ == '__main__':
    main()
