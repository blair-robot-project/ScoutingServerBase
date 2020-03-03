import json

from dataconstants import EVENT, TBA_SAVE_FILE
from tba.tba import main_event


class TBASaver:
    def __init__(self):
        try:
            self.data = json.load(open(TBA_SAVE_FILE))
        except FileNotFoundError:
            self.data = {'teams':[],'schedule':{}}

    def update(self):
        self.data = {
            'teams': main_event.team_list(),
            'schedule': main_event.full_schedule(),
        }
        self.save()

    def save(self):
        with open(TBA_SAVE_FILE, 'w') as f:
            json.dump(self.data, f)

    def team_list(self):
        return self.data['teams']

    def match_schedule(self):
        return self.data['schedule']

    def schedule_for_team(self, team):
        return [m for m in self.all_matches() if team in self.data['schedule'][m]['red']+self.data['schedule'][m]['blue']]

    def teams_in_match(self, match, level='qm', set_num=None):
        return self.data['schedule'][str(match)]

    def all_matches(self):
        return self.data['schedule'].keys()


def frc_strip(s):
    return s.strip('frc')

def match_to_teams(match_json):
    return {k: list(map(frc_strip, v['team_keys'])) for k, v in match_json['alliances'].items()} if match_json else None
