import requests

import tba.API as API
from dataconstants import EVENT
from interface import printing


class TBA:
    url = 'https://www.thebluealliance.com/api/v3/'
    auth_key = 'wUIrT2VGJOsHSz9zIOWHttKm4Ahid37DVYMmgb9gNyrtqS39cZkofL1dBBZNsx13'
    session = requests.Session()

    def __init__(self):
        self.session.headers.update({'X-TBA-Auth-Key': self.auth_key})

    def _get(self, url):
        get = self.session.get(self.url + url).json()
        if 'Errors' in get:
            printing.printf('Invalid TBA API call: ', url, '\n', get['Errors'], style=printing.YELLOW)
            return None
        return get


class Event(TBA):
    def __init__(self, event):
        super().__init__()
        self.event_key = event

    def get_all_matches(self):
        return self._get(API.ALL_MATCHES.format(event=self.event_key))

    def get_match(self, match, level='qm', set_num=None):
        return self._get(API.MATCH.format(event=self.event_key,
                                          match=match if set_num is None else set_num + 'm' + str(match), level=level))

    def get_matches_for_team(self, team):
        return self._get(API.TEAM_MATCHES.format(team=team, event=self.event_key))

    def get_schedule(self, team):
        return {(m['comp_level'] + str(m['set_number']) + 'm' if m['comp_level'] != 'qm' else '') +
                str(m['match_number']): match_to_teams(m) for m in self.get_matches_for_team(team)}

    def full_schedule(self):
        return {(m['comp_level'] + str(m['set_number']) + 'm' if m['comp_level'] != 'qm' else '') +
                str(m['match_number']): match_to_teams(m) for m in self.get_all_matches()}

    def teams_in_match(self, match, level='qm', set_num=None):
        return match_to_teams(self.get_match(match, level=level, set_num=set_num))


def frc_strip(s):
    return s.strip('frc')


def match_to_teams(match_json):
    return {k: list(map(frc_strip, v['team_keys'])) for k, v in match_json['alliances'].items()} if match_json else None


main_event = Event(EVENT)
