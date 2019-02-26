from queue import Queue
from os import listdir
from subprocess import run

import dataconstants
from ouralliance import OurAlliance
from otheralliance import OtherAlliance

to_add = Queue()


def makefile():
    # Check if there is already a data file, if not, make one
    try:
        f = open(dataconstants.DATA_FILE)
        d = f.read()
        f.close()
        if not d:
            raise FileNotFoundError
    except FileNotFoundError:
        f = open(dataconstants.DATA_FILE, 'w')
        f.write(dataconstants.HEADERS + '\n')
        f.close()


def addtoqueue(match):
    to_add.put(match)


# Adds a match to the data file
def addtodatafile(match):
    f = open(dataconstants.DATA_FILE)
    s = f.read()
    f.close()
    f = open(dataconstants.DATA_FILE, 'w')
    s += match[1] + '\n'
    f.write(s)
    f.close()


def update():
    # While there is data to add, add it to the file
    while not to_add.empty():
        addtodatafile(to_add.get())
    # if listdir(dataconstants.MEDIA_DIR):
    #     updatedrive()


# Get the data string to return from the list of teams
def getdata(team_numbers):
    f = open(dataconstants.DATA_FILE)
    # noinspection PyTypeChecker
    teams = [OurAlliance(t) for t in team_numbers[:3]] + [OtherAlliance(t) for t in team_numbers[3:]]
    for line in f:
        splitline = line.split(',')
        t = splitline[dataconstants.TEAM]
        if t in team_numbers:
            teams[team_numbers.index(t)].addline(splitline)
    return '\n'.join(map(lambda x: x.tostring(), teams))


# Writes data to a removable device
def updatedrive():
    ...

# 	ls = listdir(MEDIA_DIR)
# 	if ls:
# 		dataf = open(DATA_FILE)
# 		data = dataf.read()
# 		dataf.close()
# 		usb = open(MEDIA_DIR+'/'+ls[0]+'/'+DATA_FILE,'w')
# 		usb.write(data)
# 		usb.close()
