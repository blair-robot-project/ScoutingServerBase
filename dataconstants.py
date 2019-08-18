from enum import Enum

DATA_FILE = 'data.json'
ABS_DATA_DIR = DATA_FILE  # '/home/carter/Desktop/' + DATA_FILE
MEDIA_DIR = '/home/carter/ScoutingDrive/'

MESSAGE_SIZE = 1024

LOG_FILE = 'log'

TEAM = 'Ill update summarize.py later, for now this lets it compile'


class Fields(Enum):
    SCOUT_NAME = 'scoutName'
    TEAM_ID = 'teamId'
    MATCH_ID = 'matchId'
    ALLIANCE_COLOR = 'alliance'
    NO_SHOW = 'noShow'
    PRELOAD = 'preload'
    AUTO_MOVE = 'autoMove'
    PLACED_PIECE = 'placedAThing'
    CLIMBED = 'climbed'
    COMMENTS = 'comments'
