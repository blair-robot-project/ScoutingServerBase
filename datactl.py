from queue import Queue

import system
from dataconstants import HEADERS, DATA_FILE, ABS_DATA_DIR, TEAM, MEDIA_DIR
from otheralliance import OtherAlliance
from ouralliance import OurAlliance

to_add = Queue()
datachange = True


def makefile():
    # Check if there is already a data file, if not, make one
    try:
        f = open(ABS_DATA_DIR)
        d = f.read()
        f.close()
        if not d:
            raise FileNotFoundError
    except FileNotFoundError:
        f = open(ABS_DATA_DIR, 'w')
        f.write(HEADERS + '\n')
        f.close()


def addtoqueue(match):
    to_add.put(match)


# Adds a match to the data file
def addtodatafile(match):
    global datachange
    datachange = True
    f = open(ABS_DATA_DIR)
    s = f.read()
    s += match[1]
    f.close()
    f = open(ABS_DATA_DIR, 'w')
    f.write(s)
    f.close()


def update():
    # While there is data to add, add it to the file
    while not to_add.empty():
        addtodatafile(to_add.get())
    if datachange and system.checkdev():
        updatedrive()


# Get the data string to return from the list of teams
def getdata(team_numbers):
    f = open(ABS_DATA_DIR)
    # noinspection PyTypeChecker
    teams = [OurAlliance(t) for t in team_numbers[:3]] + [OtherAlliance(t) for t in team_numbers[3:]]
    for line in f:
        splitline = line.split(',')
        t = splitline[TEAM]
        if t in team_numbers:
            teams[team_numbers.index(t)].addline(splitline)
    return '\n'.join(map(lambda x: x.tostring(), teams))


# Writes data to a removable device
def updatedrive():
    global datachange
    if system.mount():
        system.copy(ABS_DATA_DIR, MEDIA_DIR + DATA_FILE)
        datachange = False
        system.unmount()


def driveupdaterequest():
    global datachange
    datachange = True
