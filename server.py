# noinspection PyProtectedMember
from os import _exit as osexit

from controllers import datactl
from controllers.messagectl import MessageController
from controllers.socketctl import SocketController
from dataconstants import EVENT
from interface import printing
from interface.header import print_header
from interface.input_handler import InputHandler
from interface.logger import log
from tba.tba_saver import TBASaver


class Server:
    def __init__(self):
        log("server.main", "+" * 20)
        log("server.main", "Server started")

        print_header()
        self.input_handler = InputHandler(self)

        self.data_controller = datactl.DataController()
        msgctl = MessageController(self.data_controller)
        self.socketctl = SocketController(msgctl.handle_msg)

        self.tba = TBASaver(EVENT)

    def main(self):
        self.input_handler.start_listening()

        printing.printf(
            "Waiting for connections",
            style=printing.STATUS,
            log=True,
            logtag="server.main",
        )
        self.socketctl.start_connecting()

        while True:
            try:
                self.data_controller.update()
            except KeyboardInterrupt:
                # Make sure everything made it into the data file
                self.data_controller.update()

                self.socketctl.close()

                log("server.main", "Server stopped")
                log("server.main", "-" * 20)

                # Quit everything (closes all the many threads)
                osexit(1)


if __name__ == "__main__":
    server = Server()
    server.main()
