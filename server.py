from threading import Thread

import datactl
import header
import socketctl


def main():
    header.print_header()

    datactl.makefile()

    print('Waiting for connections')

    Thread(target=socketctl.connect).start()

    while True:
        try:
            datactl.update()
        except KeyboardInterrupt:
            q = input('Are you sure you want to quit? (y/n) ')
            if q == 'y':
                socketctl.close()
                break


if __name__ == '__main__':
    main()
