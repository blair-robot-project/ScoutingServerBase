DATA_FILE = 'data.csv'
MEDIA_DIR = '/media/carter'

HEADERS = 'scout name,team #,match #,alliance color,starting level,preload,no show,moved forward,' \
          'placed piece in auto,placed location in auto,ship cargo,level 1 cargo,level 2 cargo,' \
          'level 3 cargo,ship hatches,level 1 hatches,level 2 hatches,level 3 hatches,hatches dropped,' \
          'cargo dropped,habitat attempt level,habitat success,habitat level reached,climb time,' \
          'achieved nothing,dead,defense,comments'

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
AUTO_PLACE = _ind['placed piece in auto']
AUTO_PLACE_LOC = _ind['placed location in auto']
L1RC = _ind['level 1 cargo']
L2RC = _ind['level 2 cargo']
L3RC = _ind['level 3 cargo']
L1RH = _ind['level 1 hatches']
L2RH = _ind['level 2 hatches']
L3RH = _ind['level 3 hatches']
CSC = _ind['ship cargo']
CSH = _ind['ship hatches']
HAB_ATTEMPT = _ind['habitat attempt level']
HAB_SUCCESS = _ind['habitat success']
HAB_REACHED = _ind['habitat level reached']
COMMENTS = _ind['comments']

PLACE_HOLDER = 'qual'
SEP = ' | '
NO_DATA = 'No data has been collected for this team'


# Regenerates headers string
# Copy the google doc here
# (https://docs.google.com/document/d/1o1PA9TC6kWBYI-BygvdmtlZ6l5LsLmh46P6CQnqiw8U/edit?usp=sharing)
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
