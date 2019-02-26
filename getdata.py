from dataconstants import DATA_FILE, TEAM
from otheralliance import OtherAlliance
from ouralliance import OurAlliance


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
