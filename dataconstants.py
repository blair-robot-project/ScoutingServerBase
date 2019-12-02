JSON_FILE = 'data.json'
CSV_FILE = 'data.csv'
ABS_DATA_DIR = ''  # '/home/carter/Desktop/' + DATA_FILE
MEDIA_DIR = '/home/carter/ScoutingDrive/'

MESSAGE_SIZE = 1024

LOG_FILE = 'log'

EVENT = '2019chcmp'


def enum(**enums):
    return type('Enum', (), enums)


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
