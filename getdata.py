from dataconstants import DATA_FILE, TEAM
from ouralliance import OurAlliance
from otheralliance import OtherAlliance


# Get the data string to return from the list of teams
def getdata(team_numbers):
    f = open(DATA_FILE, 'r')
    # noinspection PyTypeChecker
    teams = [OurAlliance(t) for t in team_numbers[:3]] + [OtherAlliance(t) for t in team_numbers[3:]]
    for line in f:
        splitline = line.split(',')
        t = splitline[TEAM]
        if t in team_numbers:
            teams[team_numbers.index(t)].addline(splitline)
    return '\n'.join(map(lambda x: x.tostring(), teams))


# Regenerates headers string
# Copy the google doc here
# (https://docs.google.com/document/d/1o1PA9TC6kWBYI-BygvdmtlZ6l5LsLmh46P6CQnqiw8U/edit?usp=sharing)
# Alternatively, copy the return statement of the toString of Match and it will generate it off of the comments
def recalc_headers(code, docs=True):
    global HEADERS
    c = code.split('\n')
    if docs:
        q = list(map(lambda x: x.split('\t')[0].strip(), c))
    else:
        q = list(map(lambda x: x.split('//')[1].strip(), c))
    HEADERS = ','.join(q)
    return HEADERS
