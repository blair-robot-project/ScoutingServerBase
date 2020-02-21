from _thread import interrupt_main
from threading import Thread

from controllers.messagectl import make_message, MsgTypes
from dataconstants import EVENT
from interface import printing
from tba.tba import main_event as tba_event


class InputHandler:
    def __init__(self, server):
        self.commands = Commands(server)

    def start_listening(self):
        Thread(target=self.input_loop).start()

    def input_loop(self):
        while self.commands.running:
            try:
                i = input().split(' ')
                exec('self.commands.' + i[0] + '("' + '","'.join(i[1:]) + '")')
            except Exception as e:
                printing.printf("Invalid command.", e.__class__.__name__, e, style=printing.YELLOW)


class Commands:
    running = True

    def __init__(self, server):
        self.server = server

    def quit(self, *args):
        printing.printf('Are you sure you want to quit? (y/n)', style=printing.QUIT, end=' ')
        if input() == 'y':
            self.running = False
            interrupt_main()

    def send_schedule(self, *args):
        schedule = tba_event.full_schedule()
        if schedule:
            self.server.socketctl.blanket_send(make_message(MsgTypes.SCHEDULE, schedule))
        else:
            printing.printf("Schedule not available for event:", EVENT, style=printing.YELLOW)

    def send_teams(self, *args):
        teams = tba_event.team_list()
        if teams:
            self.server.socketctl.blanket_send(make_message(MsgTypes.TEAM_LIST, teams))
        else:
            printing.printf("Team list not availible for event:",EVENT, style=printing.YELLOW)

    def strat(self, *args, **kwargs):
        if len(args) == 1:
            # Match num
            print(tba_event.teams_in_match(*args, **kwargs))
        else:
            # List of teams
            print(*args)

    def data(self, *args):
        self.server.data_controller.drive_update_request()

    def send(self, *args):
        self.server.socketctl.blanket_send(' '.join(args))

    def sum(self, *args):
        pass

    q = quit
    ss = send_schedule
    st = send_teams
    s = strat
    d = drive = data
