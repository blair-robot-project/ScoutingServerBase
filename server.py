from _thread import interrupt_main
# noinspection PyProtectedMember
from os import _exit as osexit
from threading import Thread

from controllers import datactl
from controllers.messagectl import MessageController
from controllers.socketctl import SocketController
from interface import printing
from interface.header import print_header
from interface.logger import log
from strat import summarize


class Server:
    def __init__(self):
        log('server.main', '+' * 20)
        log('server.main', 'Server started')

        print_header()

        self.data_controller = datactl.DataController()
        msgctl = MessageController(self.data_controller)
        self.socketctl = SocketController(msgctl.handle_msg)

    def main(self):
        Thread(target=self.handleinput).start()
        printing.printf('Waiting for connections', style=printing.STATUS, log=True, logtag='server.main')
        self.socketctl.start_connecting()

        while True:
            try:
                self.data_controller.update()
            except KeyboardInterrupt:
                # Make sure everything made it into the data file
                self.data_controller.update()

                self.socketctl.close()

                log('server.main', 'Server stopped')
                log('server.main', '-' * 20)

                # Quit everything (closes all the many threads)
                osexit(1)

    def handleinput(self):
        while True:
            i = input()
            ii = i.split()
            if i in ('q', 'quit'):
                printing.printf('Are you sure you want to quit? (y/n)', style=printing.QUIT, end=' ')
                q = input()
                if q == 'y':
                    interrupt_main()
                    break

            elif i in ('d', 'data', 'drive', 'flash drive', 'u', 'update', 'dump', 'data dump'):
                self.data_controller.drive_update_request()

            elif i in ('s', 'strat', 'match strat', 'strategy', 'match strategy'):
                # noinspection PyUnusedLocal
                teams = [input("Our alliance: ") for i in range(3)] + [input("Other alliance: ") for i in range(3)]
                printing.printf(summarize.strategy(teams), style=printing.DATA_OUTPUT)

            elif i in ('missing', 'm', 'count', 'msng'):
                datactl.find_missing()

            elif len(ii):
                if ii[0] in ('sum', 'summary', 'detail', 'info', 'detailed', 'full', 'ds', 'dcomp', 'dc'):
                    [printing.printf(q) for q in summarize.detailed_summary(ii[1:])]

                elif ii[0] in ('qsum', 'quick', 'brief', 'qsummary', 'qinfo', 'qk', 'qs', 'comp', 'c'):
                    [printing.printf(q) for q in summarize.quick_summary(ii[1:])]

                elif ii[0] == 'send':
                    self.socketctl.blanket_send(ii[1])


if __name__ == '__main__':
    server = Server()
    server.main()
