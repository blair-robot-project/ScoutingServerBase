from queue import Queue

import printing
import system
from dataconstants import HEADERS, DATA_FILE, ABS_DATA_DIR, TEAM, MEDIA_DIR, EDIT_TRIGGER, NAME, MATCH
from opponent import Opponent
from partner import Partner

to_add = Queue()
datachange = True

void = []


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


def _parsedata(data, info):
    t = 'Data'
    for line in data.split('\n'):
        line = line.strip()
        if line[:len(EDIT_TRIGGER)] == EDIT_TRIGGER:
            removefromdatafile(line[len(EDIT_TRIGGER):])
            void.append(line[len(EDIT_TRIGGER):])
            t = 'Edit'
        elif line:
            if line not in void:
                try:
                    match = line.split(',')
                    printing.printf(t + ' from ' + match[NAME] + ' on ' + info + ' for team ' +
                                    match[TEAM] + ' in match ' + match[MATCH], style=printing.NEW_DATA)
                    _addtodatafile(line)
                except IndexError:
                    printing.printf('Incomplete line:', line, style=printing.ERROR)
            t = 'Data'


def addtoqueue(match, info):
    to_add.put((match, info))


def _addtodatafile(match):
    _writefile(_readfile() + match + '\n')


def removefromdatafile(match):
    _writefile(_readfile().replace(match + '\n', ''))


def _readfile():
    global datachange
    datachange = True
    f = open(ABS_DATA_DIR)
    s = f.read()
    f.close()
    return s


def _writefile(s):
    f = open(ABS_DATA_DIR, 'w')
    f.write(s)
    f.close()


def update():
    # While there is data to add, parse it
    while not to_add.empty():
        _parsedata(*to_add.get())
    if datachange and system.checkdev():
        _updatedrive()


# Get the data string to return from the list of teams
def getdata(team_numbers):
    f = open(ABS_DATA_DIR)
    # noinspection PyTypeChecker
    teams = [Partner(t) for t in team_numbers[:3]] + [Opponent(t) for t in team_numbers[3:]]
    for line in f:
        splitline = line.split(',')
        t = splitline[TEAM]
        if t in team_numbers:
            teams[team_numbers.index(t)].addline(splitline)
    d = list(map(lambda t: t.tostring(), teams))
    return teams[0].getheader() + '\n' + '\n'.join(d[:3]) + '\n---\n' + teams[3].getheader() + '\n' + '\n'.join(
        d[3:]) + '\n===\n' + '\n'.join([t.getteam() + ': ' + t.getcomments() for t in teams])


# Writes data to a removable device
def _updatedrive():
    global datachange
    if system.mount():
        system.copy(ABS_DATA_DIR, MEDIA_DIR + DATA_FILE)
        datachange = False
        system.unmount()


def driveupdaterequest():
    global datachange
    datachange = True
