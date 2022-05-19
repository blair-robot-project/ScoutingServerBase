from _thread import interrupt_main
from threading import Thread

from scoutingserver.interface import printing
from scoutingserver.summarize import strategy


class InputHandler:
    def __init__(self, server):
        self.server = server

    def start_listening(self):
        Thread(target=self.input_loop).start()

    def input_loop(self):
        running = True
        while running:
            cmd, *args = input().split(" ")

            if cmd == "q":
                printing.printf(
                    "Are you sure you want to quit? (y/n)", style=printing.QUIT, end=" "
                )
                if input() == "y":
                    running = False
                    interrupt_main()
            # elif cmd == "tba":
            #     self.server.tba.update()
            elif cmd == "s":
                if len(args) == 1:
                    printing.printf(
                        strategy(
                            self.server.tba.teams_in_match(*args),
                            self.server.config,
                            self.data_dir,
                        ),
                        style=printing.DATA_OUTPUT,
                    )
                else:
                    printing.printf(
                        strategy(args, self.server.config, self.server.data_dir),
                        style=printing.DATA_OUTPUT,
                    )
            elif cmd == "s":
                self.server.data_controller.drive_update_request()
            elif cmd == "m":
                self.server.data_controller.find_missing(
                    self.server.tba.match_schedule()
                )
            else:
                printing.printf(
                    f"Command '{cmd}' not found",
                    log=True,
                    logtag="input_handler.input_loop",
                    style=printing.ERROR,
                )
                continue
