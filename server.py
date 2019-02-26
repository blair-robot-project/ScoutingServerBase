from threading import Thread

import datactl
import header
import socketctl


def main():
    header.print_header()

    datactl.makefile()

    print('Waiting for connections')

    Thread(target=socketctl.connect).start()

    running = True
    while running:
        try:
            datactl.update()
        except KeyboardInterrupt:
            q = input('Would you like to access strategy data (s), quit (q), or cancel (c)? ')
            if q == 's':
                # noinspection PyUnusedLocal
                teams = [input("Our alliance: ") for i in range(3)] + [input("Other alliance: ") for i in range(3)]
                print(datactl.getdata(teams))
            elif q == 'q' or q == 'quit':
                socketctl.close()
                running = False


if __name__ == '__main__':
    main()
