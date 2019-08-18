from queue import Queue

from controllers import systemctl
from dataconstants import HEADERS, DATA_FILE, ABS_DATA_DIR, TEAM, MEDIA_DIR, EDIT_TRIGGER, NAME, MATCH
from interface import printing


class DataController:
    data_queue = Queue()
    data_changed = True

    def __init__(self):
        ...

    def queue_data(self, data):
        self.data_queue.put(data)

    def update(self):
        # While there is data to add, parse it
        while not self.data_queue.empty():
            self.parsedata(self.data_queue.get())
        # If there is a flash drive and there is new data for it, upload the data
        if self.data_changed and systemctl.checkdev():
            _updatedrive()

    # Parse a string with lines of data
    def parsedata(self, data):
        print(data)
        # for line in data.split('\n'):
        #     line = line.strip()
        #     if line[:len(EDIT_TRIGGER)] == EDIT_TRIGGER:
        #         # If this is an edit, remove the old version
        #         trimmedline = line[len(EDIT_TRIGGER):]
        #         removefromdatafile(trimmedline)
        #         void.append(trimmedline)
        #
        #         _summarize(trimmedline, info, action='Edit')
        #
        #     elif line:
        #         # If this wasn't already edited (could happen if this is an upload not a submit)
        #         if line not in void:
        #             _addtodatafile(line)
        #             _summarize(line, info)

    def driveupdaterequest(self):
        self.data_changed = True


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


# Print a summary of the data received
def _summarize(line, info, action='Data'):
    try:
        match = line.split(',')
        printing.printf(action + ' from ' + match[NAME] + ' on ' + info + ' for team ' +
                        match[TEAM] + ' in match ' + match[MATCH],
                        style=printing.NEW_DATA if action == 'Data' else printing.EDIT,
                        log=True, logtag='datactl._summarize')
    except IndexError:
        printing.printf('Incomplete line:', line, style=printing.ERROR,
                        log=True, logtag='datactl._summarize.error')


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
    f = open(ABS_DATA_DIR, mode)
    f.write(s)
    f.close()


# Writes data to a removable device
def _updatedrive():
    if systemctl.mount():
        systemctl.copy(ABS_DATA_DIR, MEDIA_DIR + DATA_FILE)
        systemctl.unmount()




def findmissing():
    q = _readfile().strip().split('\n')
    w = list(map(lambda x: x.split(','), q))
    a = list(map(lambda x: (int(x[1]), int(x[0]), x[27 if len(x) > 27 else 0]), w[1:]))
    s = [set() for _ in range(max(map(lambda x: x[0], a)))]
    l = [list() for _ in range(max(map(lambda x: x[0], a)))]
    for p in a:
        l[p[0] - 1].append(p[1:])
        s[p[0] - 1].add(p[1:2])
    for i in range(len(l)):
        if len(l[i]) != 6 or len(s[i]) != 6:
            print(i + 1, ':', len(l[i]))
            print(' ', l[i])
            print()
