from queue import Queue

import printing
import system
from dataconstants import HEADERS, DATA_FILE, ABS_DATA_DIR, TEAM, MEDIA_DIR, EDIT_TRIGGER, NAME, MATCH
from logger import log
from opponent import Opponent
from partner import Partner

# Thread-safe queue to add lines to the file without concurrent modification
to_add = Queue()

# Keeps track of data changes since the flash drive was updated
datachange = True

# Keeps track of lines that have been removed
# Important for when a match is submitted without connection, then edited with connection, then 'newdata' is uploaded
void = []


# Check if there is already a data file, if not, make one
def makefile():
    try:
        d = _readfile()
        if not d:
            raise FileNotFoundError
    except FileNotFoundError:
        _writefile(HEADERS + '\n')


# Parse a string with lines of data
def _parsedata(data, info):
    for line in data.split('\n'):
        line = line.strip()
        if line[:len(EDIT_TRIGGER)] == EDIT_TRIGGER:
            # If this is an edit, remove the old version
            trimmedline = line[len(EDIT_TRIGGER):]
            removefromdatafile(trimmedline)
            void.append(trimmedline)

            _summarize(trimmedline, info, action='Edit')

        elif line:
            # If this wasn't already edited (could happen if this is an upload not a submit)
            if line not in void:
                _addtodatafile(line)
                _summarize(line, info)


# Print a summary of the data received
def _summarize(line, info, action='Data'):
    try:
        match = line.split(',')
        printing.printf(action + ' from ' + match[NAME] + ' on ' + info + ' for team ' +
                        match[TEAM] + ' in match ' + match[MATCH],
                        style=printing.NEW_DATA if action == 'Data' else printing.EDIT,
                        log=True, logtag='datactl._parsedata')
    except IndexError:
        printing.printf('Incomplete line:', line, style=printing.ERROR,
                        log=True, logtag='datactl._parsedata')


def addtoqueue(match, info):
    to_add.put((match, info))


def _addtodatafile(match):
    _writefile(match + '\n')


def removefromdatafile(match):
    _writefile(_readfile().replace(match + '\n', ''), mode='w')


def _readfile():
    f = open(ABS_DATA_DIR)
    s = f.read()
    f.close()
    return s


def _writefile(s, mode='a'):
    global datachange
    datachange = True
    f = open(ABS_DATA_DIR, mode)
    f.write(s)
    f.close()


def update():
    # While there is data to add, parse it
    while not to_add.empty():
        _parsedata(*to_add.get())
    # If there is a flash drive and there is new data for it, upload the data
    if datachange and system.checkdev():
        _updatedrive()


# Get the data string to return from the list of teams
def getdata(team_numbers):
    log('datactl.getdata', 'Strategy data request for ' + ', '.join(team_numbers))

    f = open(ABS_DATA_DIR)
    # noinspection PyTypeChecker
    teams = [Partner(t) for t in team_numbers[:3]] + [Opponent(t) for t in team_numbers[3:]]
    for line in f:
        splitline = line.split(',')
        t = splitline[TEAM]
        if t in team_numbers:
            teams[team_numbers.index(t)].addline(splitline)

    d = list(map(lambda t: t.tostring(), teams))
    return teams[0].getheader() + '\n' + '\n'.join(d[:3]) + '\n---\n' + teams[3].getheader() + '\n' + \
           '\n'.join(d[3:]) + '\n===\n' + '\n'.join([t.getteam() + ': ' + t.getcomments() for t in teams])


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
