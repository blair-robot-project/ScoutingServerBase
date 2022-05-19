from _thread import interrupt_main
from threading import Thread

from scoutingserver.interface import printing
from scoutingserver.strat.summarize import strategy


class InputHandler:
    def __init__(self, server):
        self.commands = Commands(server)

    def start_listening(self):
        Thread(target=self.input_loop).start()

    def input_loop(self):
        while self.commands.running:
            # try:
            i = input().split(" ")
            try:
                cmd = self.commands.cmds[i[0]]
            except AttributeError:
                printing.printf(
                    f"Command '{i[0]}' not found",
                    log=True,
                    logtag="input_handler.input_loop",
                    style=printing.ERROR,
                )
                continue
            cmd(*i[1:])
            # except Exception as e:
            # printing.printf("Invalid command.", e.__class__.__name__, e, style=printing.YELLOW)


class Commands:
    running = True

    def __init__(self, server, data_dir):
        self.server = server
        self.config = server.config
        self.data_dir = data_dir
        self.cmds = {
            "q": quit_,
            "tba": update_tba,
            "s": strat,
            "d": data,
            "m": missing,
        }

    def quit_(self, *args):
        printing.printf(
            "Are you sure you want to quit? (y/n)", style=printing.QUIT, end=" "
        )
        if input() == "y":
            self.running = False
            interrupt_main()

    def update_tba(self, *args):
        self.server.tba.update()

    def strat(self, *args, **kwargs):
        if len(args) == 1:
            printing.printf(
                strategy(
                    self.server.tba.teams_in_match(*args), self.config, self.data_dir
                ),
                style=printing.DATA_OUTPUT,
            )
        else:
            printing.printf(
                strategy(args, self.config, self.data_dir), style=printing.DATA_OUTPUT
            )

    def data(self, *args):
        self.server.data_controller.drive_update_request()

    def missing(self, *args):
        self.server.data_controller.find_missing(self.server.tba.match_schedule())

    # For testing only
    # def send(self, *args):
    # self.server.socketctl.blanket_send(' '.join(args))

