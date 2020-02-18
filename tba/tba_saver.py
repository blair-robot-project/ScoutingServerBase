import json

from dataconstants import EVENT, TBA_SAVE_FILE
from tba.tba import main_event


class TBASaver:
    def __init__(self):
        try:
            self.schedules = json.load(open(TBA_SAVE_FILE))
        except FileNotFoundError:
            self.schedules = dict()

    def update(self):
        self.schedules[EVENT] = {
            'teams': main_event.get_teams(),
            'matches': main_event.full_schedule(),
            'revision': self.schedules.get(EVENT, {'revision': 0})['revision']
        }
        self.save()

    def save(self):
        with open(TBA_SAVE_FILE, 'w') as f:
            json.dump(self.schedules, f)
