# noinspection PyProtectedMember
from os import _exit as osexit

import sys

from scoutingserver.config import load_config
from scoutingserver.controllers import datactl
from scoutingserver.controllers.messagectl import MessageController
from scoutingserver.controllers.gattctl import GattController
from scoutingserver.interface import printing
from scoutingserver.interface.header import print_header
from scoutingserver.interface.input_handler import InputHandler
from scoutingserver.interface.logger import log
from scoutingserver.tba.tba_saver import TBASaver


class Server:
    def __init__(self):
        log("server.main", "+" * 20)
        log("server.main", "Server started")

        print_header()
        if len(sys.argv) > 1:
            data_dir = sys.argv[1]
        else:
            data_dir = input("Absolute data directory (e.g. '/home/user/Desktop') ")
        # The location of the removable device to copy data to
        drive = input("Flash drive location (e.g. 'D:') (default none) ") or None

        self.config = load_config(input("Event config file: "))

        self.input_handler = InputHandler(self)

        self.data_controller = datactl.DataController(self.config, data_dir, drive)
        msgctl = MessageController(self.data_controller)
        self.gattcl = GattController(msgctl.handle_msg, self.config)

        self.tba = TBASaver(self.config.event_name)

    def run(self):
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
