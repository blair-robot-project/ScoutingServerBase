import requests
import json

class TBA:
    url = 'https://www.thebluealliance.com/api/v3/'
    auth_key = 'wUIrT2VGJOsHSz9zIOWHttKm4Ahid37DVYMmgb9gNyrtqS39cZkofL1dBBZNsx13'
    session = requests.Session()
    event_key = None

    def __init__(self, event=None):
        self.session.headers.update({'X-TBA-Auth-Key':self.auth_key})
        if event:
            self.event_key = event

    def _get(self, url):
        # TODO: handle error messages
        return self.session.get(self.url + url).json()

    def get_all_matches(self, event=None):
        if event_key is None: event_key=self.event_key
        return self._get('event/{}/matches/simple'.format(event_key)) if event_key is not None else None

    def get_teams_in_match(self, event, match):
        ...

    def get_schedule(self, event, team):
        ...
