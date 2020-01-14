import json

from dataconstants import EVENT, TBA_SAVE_FILE
from tba.tba import Event


class TBASaver:
    def __init__(self):
        self.event = Event(EVENT)
        try:
            self.schedules = json.load(open(TBA_SAVE_FILE))
        except FileNotFoundError:
            self.schedules = dict()

    def update(self):
        self.schedules[EVENT] = {
            'teams': self.event.get_teams(),
            'matches': self.event.full_schedule(),
            'revision': self.schedules.get(EVENT, {'revision': 0})['revision']
        }
        self.save()

    def save(self):
        with open(TBA_SAVE_FILE, 'w') as f:
            json.dump(self.schedules, f)
