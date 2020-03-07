import json

LOCAL_CONSTANTS_FILE = 'local_constants.json'
try:
    local_constants = json.load(open(LOCAL_CONSTANTS_FILE))
except FileNotFoundError:
    print('Please enter the following file names and directory locations:')
    local_constants = {
        'DATA_FILE_NAME': input('Data file base name (e.g. \'data\') '),
        'ABS_DATA_DIR': input('Absolute data directory (e.g. \'/home/user/Desktop\') '),
        'TEAM': input('Team number (e.g. 449) '),
        'EVENT': input('TBA event id (e.g. \'2020mdbet\') ')
    }
    with open(LOCAL_CONSTANTS_FILE, 'w') as f:
        json.dump(local_constants, f)

JSON_FILE = local_constants['DATA_FILE_NAME'] + '.json'
CSV_FILE = local_constants['DATA_FILE_NAME'] + '.csv'
ABS_DATA_DIR = local_constants['ABS_DATA_DIR']
EVENT = local_constants['EVENT']
TEAM = local_constants['TEAM']

TBA_SAVE_FILE = 'tba.json'

MESSAGE_SIZE = 1024

LOG_FILE = 'log'


def enum(**enums):
    return type('Enum', (), enums)


# TODO: do this in a less dumb way
FieldsEnum = enum(TEAM_ID='teamId',
                  MATCH_ID='matchId',
                  ALLIANCE_COLOR='alliance',
                  NO_SHOW='noShow',
                  PRELOAD='preload',
                  AUTO_MOVE='autoMove',
                  HIT_PARTNER='hitPartner',
                  AUTO_INTAKE='autoIntake',
                  AUTO_CENTER='autoCenter',
                  AUTO_HIGH='autoHigh',
                  AUTO_LOW='autoLow',
                  AUTO_MISS='autoMiss',
                  HIGH='high',
                  CENTER='center',
                  LOW='low',
                  MISS='miss',
                  SPINNER_ROT='spinnerRot',
                  SPINNER_POS='spinnerPos',
                  ATTEMPTED_CLIMB='attemptedClimb',
                  PARK='park',
                  SOLO_CLIMB='soloClimb',
                  DOUBLE_CLIMB='doubleClimb',
                  WAS_LIFTED='wasLifted',
                  CLIMB_TIME='climbTime',
                  ENDGAME_SCORE='endgameScore',
                  LEVEL='level',
                  DEAD='dead',
                  DEFENSE='defense',
                  COMMENTS='comments',
                  SCOUT_NAME='scoutName',
                  REVISION='revision',
                  TIMESTAMP='timestamp',
                  MATCH='match',
                  TEAM='team',
                  SOLO_CLIMB_NYF='soloClimbNYF',
                  DOUBLE_CLIMB_NYF='doubleClimbNYF',
                  WAS_LIFTED_NYF='wasLiftedNYF')

Fields = FieldsEnum()

ORDER = [Fields.TEAM, Fields.MATCH, Fields.ALLIANCE_COLOR, Fields.NO_SHOW, Fields.AUTO_MOVE, 
         Fields.HIT_PARTNER, Fields.AUTO_INTAKE, Fields.AUTO_LOW, Fields.AUTO_HIGH, Fields.AUTO_CENTER, 
         Fields.AUTO_MISS, Fields.LOW, Fields.HIGH, Fields.CENTER, Fields.MISS, Fields.SPINNER_ROT, 
         Fields.SPINNER_POS, Fields.ATTEMPTED_CLIMB, Fields.PARK, Fields.SOLO_CLIMB, Fields.DOUBLE_CLIMB, 
         Fields.WAS_LIFTED, Fields.SOLO_CLIMB_NYF, Fields.DOUBLE_CLIMB_NYF, Fields.WAS_LIFTED_NYF, 
         Fields.CLIMB_TIME, Fields.ENDGAME_SCORE, Fields.LEVEL, Fields.DEAD, Fields.DEFENSE, Fields.COMMENTS, 
         Fields.SCOUT_NAME, Fields.REVISION, Fields.TIMESTAMP]

MAC_DICT = {'00:FC:8B:3B:42:46': 'R1 Demeter',
            '00:FC:8B:39:C1:09': 'R2 Hestia',
            '78:E1:03:A3:18:78': 'R3 Hera',
            '78:E1:03:A1:E2:F2': 'B1 Hades',
            '78:E1:03:A4:F7:70': 'B2 Poseidon',
            '00:FC:8B:3F:E4:EF': 'B3 Zeus',
            '00:FC:8B:3F:28:28': 'Backup 1'}
