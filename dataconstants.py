DATA_FILE = 'data.csv'
MEDIA_DIR = '/media/carter'

HEADERS = 'scout name,team #,match #,alliance color,starting level,preload,no show,moved forward,' \
          'placed piece in auto,placed location in auto,ship cargo,level 1 cargo,level 2 cargo,' \
          'level 3 cargo,ship hatches,level 1 hatches,level 2 hatches,level 3 hatches,hatches dropped,' \
          'cargo dropped,habitat attempt level,habitat success,habitat level reached,climb time,' \
          'achieved nothing,dead,defense,comments'

GETDATA_TRIGGER = 'GETDATA'


# Constants to easily refer to data points in a line
ind = {HEADERS.split(',')[i]: i for i in range(len(HEADERS.split(',')))}
NAME = ind['scout name']
MATCH = ind['match #']
TEAM = ind['team #']
NO_SHOW = ind['no show']
STARTING_LEVEL = ind['starting level']
PRELOAD = ind['preload']
MOVED_FORWARD = ind['moved forward']
AUTO_PLACE = ind['placed piece in auto']
AUTO_PLACE_LOC = ind['placed location in auto']
L1RC = ind['level 1 cargo']
L2RC = ind['level 2 cargo']
L3RC = ind['level 3 cargo']
L1RH = ind['level 1 hatches']
L2RH = ind['level 2 hatches']
L3RH = ind['level 3 hatches']
CSC = ind['ship cargo']
CSH = ind['ship hatches']
HAB_ATTEMPT = ind['habitat attempt level']
HAB_SUCCESS = ind['habitat success']
HAB_REACHED = ind['habitat level reached']
COMMENTS = ind['comments']

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
