from _thread import interrupt_main
# noinspection PyProtectedMember
from os import _exit as osexit
from threading import Thread

import datactl
import printing
import socketctl
import summarize
from header import print_header
from logger import log


def main():
    log('server.main', '+'*20)
    log('server.main', 'Server started')

    print_header()

    datactl.makefile()

    printing.printf('Waiting for connections', style=printing.STATUS, log=True, logtag='server.main')

    Thread(target=handleinput).start()

    socketctl.init()
    Thread(target=socketctl.connect).start()

    while True:
        try:
            datactl.update()
        except KeyboardInterrupt:
            # Make sure everything made it into the data file
            datactl.update()

            socketctl.close()

            log('server.main', 'Server stopped')
            log('server.main', '-' * 20)

            # Quit everything (closes all the many threads)
            osexit(1)


def handleinput():
    i = input()
    ii = i.split()
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
        printing.printf(summarize.strategy(teams), style=printing.DATA_OUTPUT)

    elif ii[0] in ('sum', 'summary', 'detail', 'info', 'detailed', 'full', 'ds'):
        printing.printf(summarize.detailed_summary(handleargument(ii)[0]))

    elif ii[0] in ('qsum', 'quick', 'brief', 'qsummary', 'qinfo', 'qk', 'qs'):
        printing.printf(summarize.quick_summary(handleargument(ii)[0]))

    elif ii[0] in ('comp', 'c', 'compare', 'comparison', 'diff'):
        printing.printf(summarize.quick_summary(handleargument(ii, n=len(ii)-1 if len(ii) > 2 else input('n: '))))

    elif ii[0] in ('dcomp', 'dc', 'dcompare', 'dcomparison', 'ddiff', 'detail comp', 'full comp'):
        printing.printf(summarize.detailed_summary(handleargument(ii, n=len(ii)-1 if len(ii) > 2 else input('n: '))))

    Thread(target=handleinput).start()


def handleargument(ii, n=1):
    [ii[i] if len(ii) > i else input('Team: ') for i in range(1)]


if __name__ == '__main__':
    main()
