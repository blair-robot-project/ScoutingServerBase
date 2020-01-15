import json

LOCAL_CONSTANTS_FILE = 'local_constants.json'
try:
    local_constants = json.load(open(LOCAL_CONSTANTS_FILE))
except FileNotFoundError:
    print('Please enter the following file names and directory locations:')
    local_constants = {
        'DATA_FILE_NAME': input('Data file base name (e.g. \'data\') '),
        'ABS_DATA_DIR': input('Absolute data directory (e.g. \'/home/user/Desktop\') '),
        'MEDIA_DIR': input('Media directory (location flash drive is mounted to) ')
    }
    with open(LOCAL_CONSTANTS_FILE, 'w') as f:
        json.dump(local_constants, f)

JSON_FILE = local_constants['DATA_FILE_NAME'] + '.json'
CSV_FILE = local_constants['DATA_FILE_NAME'] + '.csv'
ABS_DATA_DIR = local_constants['ABS_DATA_DIR']
MEDIA_DIR = local_constants['MEDIA_DIR']

TBA_SAVE_FILE = 'tba.json'

MESSAGE_SIZE = 1024

LOG_FILE = 'log'

EVENT = '2019chcmp'


def enum(**enums):
    return type('Enum', (), enums)


# TODO: do this in a less dumb way
FieldsEnum = enum(TEAM_ID='teamId',
                  MATCH_ID='matchId',
                  ALLIANCE_COLOR='alliance',
                  NO_SHOW='noShow',
                  PRELOAD='preload',
                  AUTO_MOVE='autoMove',
                  PLACED_PIECE='placedAThing',
                  CLIMBED='climbed',
                  COMMENTS='comments',
                  SCOUT_NAME='scoutName',
                  REVISION='revision',
                  TIMESTAMP='timestamp')

Fields = FieldsEnum()

ORDER = [Fields.TEAM_ID, Fields.MATCH_ID, Fields.ALLIANCE_COLOR, Fields.NO_SHOW, Fields.PRELOAD, Fields.AUTO_MOVE,
         Fields.PLACED_PIECE, Fields.CLIMBED, Fields.COMMENTS, Fields.SCOUT_NAME, Fields.REVISION, Fields.TIMESTAMP]

MAC_DICT = {'00:FC:8B:3B:42:46': 'R1 Demeter',
            '00:FC:8B:39:C1:09': 'R2 Hestia',
            '78:E1:03:A3:18:78': 'R3 Hera',
            '78:E1:03:A1:E2:F2': 'B1 Hades',
            '78:E1:03:A4:F7:70': 'B2 Poseidon',
            '00:FC:8B:3F:E4:EF': 'B3 Zeus',
            '00:FC:8B:3F:28:28': 'Backup 1'}
