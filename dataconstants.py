DATA_FILE = 'whitman.csv'
ABS_DATA_DIR = '/home/carter/Desktop/' + DATA_FILE
MEDIA_DIR = '/home/carter/ScoutingDrive/'

LOG_FILE = 'log'

HEADERS = 'team #,match #,alliance color,starting level,preload,no show,moved forward,auto piece placed,double auto,' \
          'ship cargo,level 1 cargo,level 2 cargo,level 3 cargo,ship hatches,level 1 hatches,level 2 hatches,' \
          'level 3 hatches,hatches dropped,cargo dropped,hab attempt level,hab success,hab level reached,climb time,' \
          'dead,defense,comments,scout name,time stamp, '


EDIT_TRIGGER = 'REPLACE'
GETDATA_TRIGGER = 'GETDATA'


# Constants to easily refer to data points in a line
_ind = {HEADERS.split(',')[i]: i for i in range(len(HEADERS.split(',')))}
NAME = _ind['scout name']
MATCH = _ind['match #']
TEAM = _ind['team #']
NO_SHOW = _ind['no show']
STARTING_LEVEL = _ind['starting level']
PRELOAD = _ind['preload']
MOVED_FORWARD = _ind['moved forward']
AUTO_PLACE = _ind['auto piece placed']
L1RC = _ind['level 1 cargo']
L2RC = _ind['level 2 cargo']
L3RC = _ind['level 3 cargo']
L1RH = _ind['level 1 hatches']
L2RH = _ind['level 2 hatches']
L3RH = _ind['level 3 hatches']
CSC = _ind['ship cargo']
CSH = _ind['ship hatches']
DROP_HATCH = _ind['hatches dropped']
DROP_CARGO = _ind['cargo dropped']
HAB_ATTEMPT = _ind['hab attempt level']
HAB_SUCCESS = _ind['hab success']
HAB_REACHED = _ind['hab level reached']
CLIMB_TIME = _ind['climb time']
DEFENSE = _ind['defense']
COMMENTS = _ind['comments']

NO_DATA = 'No data has been collected for this team'


# Regenerates headers string
# Copy the google doc here
# (https://docs.google.com/document/d/e/2PACX-1vSp7j7vCPgH-OLdPKhMAEnKDSYsi99BufqXZlAtQ5-3uarYPo0ePbIv9WJOP2oC02fvnjt30iEE5z3C/pub)
# Alternatively, copy the return statement of the toString of Match and it will generate it off of the comments
def recalc_headers(code, docs=True):
    c = code.split('\n')
    if docs:
        q = list(map(lambda x: x.split('\t')[0].strip(), c))
    else:
        q = list(map(lambda x: x.split('//')[1].strip(), c))
    headers = ','.join(q)
    print(headers)
    return headers
