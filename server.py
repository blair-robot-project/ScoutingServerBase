import socket
from threading import Thread
from queue import Queue
from os import lsitdir
from subprocess import run
from textwrap import TextWrapper
from shutil import get_terminal_size

# This should be the MAC address of your Bluetooth adapter
# Carter's desktop (essuomelpmap)
#HOST_MAC = '00:1A:7D:DA:71:13'

# Nate's laptop (DESKTOP-9HL0MM7)
#HOST_MAC = 'E4:F8:9C:BC:93:0E'

# Carter's laptop (gallium)
HOST_MAC = 'A4:C4:94:4F:6F:63'

PORT = 1
BACKLOG = 1
SIZE = 1024

DATA_FILE = 'data.csv'
HEADERS = 'scout name,team #,match #,alliance color,starting level,preload,no show,moved forward,'\
          'placed piece in auto,placed location in auto,ship cargo,level 1 cargo,level 2 cargo,'\
          'level 3 cargo,ship hatches,level 1 hatches,level 2 hatches,level 3 hatches,hatches dropped,'\
          'cargo dropped,habitat attempt level,habitat success,habitat level reached,climb time,'\
          'achieved nothing,dead,defense,comments'
GETDATA_TRIGGER = 'GETDATA'

MEDIA_DIR = '/media/carter'

MAC_DICT = {'78:E1:03:A4:F7:70': 'Poseidon', '44:65:0D:E0:D6:3A': 'Strategy Tablet'}

# Setup server socket
server_sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
server_sock.bind((HOST_MAC, PORT))
server_sock.listen(BACKLOG)

clients = []

to_add = Queue()


# Read loop to continually read data from a client
def read(sock, info):
    try:
        # Receive data
        data = sock.recv(SIZE)
        str_data = data.decode()
        if str_data[:7] == GETDATA_TRIGGER:
            # If it is a strategy request, return the data
            print('Data request ' + str_data)
            # sock.send(bytes(get_data(data.split(':')[1]), 'UTF-8'))
            print(get_data(str_data.split()[1:]))
        else:
            # Add it to the data file
            to_add.put((info, str_data))
        # Wait for the next match
        read(sock, info)
    except ConnectionResetError:
        print('Disconnected from', info)
        sock.close()
        clients.remove((sock, info))


# Waits for a device to try to connect, then starts a thread to read that device, and stays open for connections
def connect():
    # Wait for connection
    client_sock, client_info = server_sock.accept()
    # Connect to device
    print('Accepted connection from', MAC_DICT.get(client_info[0], client_info[0]))
    clients.append((client_sock, client_info[0]))

    # Start reading it
    Thread(target=lambda: read(client_sock, client_info[0])).start()

    # Stay open for connections
    connect()


# Adds a match to the data file
def add_to_data_file(match):
    f = open(DATA_FILE, 'r')
    s = f.read()
    f.close()
    f = open(DATA_FILE, 'w')
    s += match[1] + '\n'
    f.write(s)
    f.close()
    split_match = match[1].split(',')
    print('Data from ' + split_match[0] + ' on ' + MAC_DICT.get(match[0], match[0]) + ' for team ' +
          split_match[2] + ' in match ' + split_match[1])


# Writes data to a removable device
def write_usb():
	ls = listdir(MEDIA_DIR)
	if ls:
		dataf = open(DATA_FILE)
		data = dataf.read()
		dataf.close()
		usb = open(MEDIA_DIR+'/'+ls[0]+'/'+DATA_FILE,'w')
		usb.write(data)
		usb.close()
		
		

def main():
    # Print instructions to fill width of screen
    width = get_terminal_size(fallback=(100, 24))[0]
    print_header(width)

    # Check if there is already a data file, if not, make one
    try:
        f = open(DATA_FILE, 'r')
        d = f.read()
        f.close()
        if not d:
            raise FileNotFoundError
    except FileNotFoundError:
        f = open(DATA_FILE, 'w')
        f.write(HEADERS + '\n')
        f.close()

    print('Waiting for connections')

    Thread(target=connect).start()

    while True:
        try:
            # If there is data to add, add it to the file
            if not to_add.empty():
                add_to_data_file(to_add.get())
            elif listdir(MEDIA_DIR):
            	write_usb()
        except KeyboardInterrupt:
            q = input('Are you sure you want to quit? (y/n) ')
            if q == 'y':
                # Finish adding data
                while not to_add.empty():
                    add_to_data_file(to_add.get())
                for sock in clients:
                    sock[0].close()
                    print('Closed connection with', sock[1])
                server_sock.close()
                print('Closed server')
                break


##########################
# Strategy data processing

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


# Get the data string to return from the list of teams
def get_data(team_numbers):
    f = open(DATA_FILE, 'r')
    # noinspection PyTypeChecker
    teams = [OurAlliance(t) for t in team_numbers[:3]] + [OtherAlliance(t) for t in team_numbers[3:]]
    for line in f:
        splitline = line.split(',')
        t = splitline[TEAM]
        if t in team_numbers:
            teams[team_numbers.index(t)].add_line(splitline)
    return '\n'.join(map(lambda x: x.tostring(), teams))


# Helper function to convert floats to percents and round
def percent(n):
    return str(int(n * 100))


# Calculates data we want for teams on our alliance
class OurAlliance:
    total, autocross, start1, prec, preh, autoc, autoh, lowh, lowc, highc, highh = [0] * 11
    habattempt, habsuccess = [0] * 4, [0] * 4

    def __init__(self, team):
        self.team = team

    def add_line(self, line):
        self.total += 1

        self.autocross += int(line[MOVED_FORWARD])
        self.start1 += line[STARTING_LEVEL] == '1'
        if line[PRELOAD] == '2':
            self.prec += 1
            self.autoc += line[AUTO_PLACE] == '2'
        elif line[PRELOAD] == '3':
            self.preh += 1
            self.autoh += line[AUTO_PLACE] == '3'

        self.lowc += int(line[CSC]) + int(line[L1RC])
        self.lowh += int(line[CSH]) + int(line[L1RH])
        self.highc += int(line[L2RC]) + int(line[L3RC])
        self.highh += int(line[L2RH]) + int(line[L3RH])

        self.habattempt[int(line[HAB_ATTEMPT])] += 1
        self.habsuccess[int(line[HAB_ATTEMPT])] += line[HAB_SUCCESS] == '3'

    def tostring(self):
        if self.total:
            autocross = percent(self.autocross / self.total)
            start = self.start1 / self.total
            start_str = percent(start) + ':' + percent(1 - start)
            preload = percent(self.prec / self.total) + ':' + percent(self.preh / self.total)
            accuracy = percent(0 if not self.prec else self.autoc / self.prec) + ':' + percent(
                0 if not self.preh else self.autoh / self.preh)

            lowc = str(self.lowc / self.total)
            lowh = str(self.lowh / self.total)
            highc = str(self.highc / self.total)
            highh = str(self.highh / self.total)

            attempt = percent(self.habattempt[1] / self.total) + ':' + percent(
                self.habattempt[2] / self.total) + ':' + percent(self.habattempt[3] / self.total)
            success = percent(0 if not self.habattempt[2] else self.habsuccess[2] / self.habattempt[2]) + ':' + percent(
                0 if not self.habattempt[3] else self.habsuccess[3] / self.habattempt[3])

            order = [self.team, '', autocross, start_str, accuracy, preload, '#', lowh, lowc, PLACE_HOLDER, highc,
                     highh, PLACE_HOLDER, '#', attempt, success, PLACE_HOLDER]
            return SEP.join(order)
        return self.team + ': ' + NO_DATA


# Calculates data we want for teams on the other alliance
class OtherAlliance:
    total, lowh, lowc, highc, highh = [0] * 5
    habsuccess = [0, 0, 0, 0]

    def __init__(self, team):
        self.team = team

    def add_line(self, line):
        self.total += 1

        self.lowc += int(line[CSC]) + int(line[L1RC])
        self.lowh += int(line[CSH]) + int(line[L1RH])
        self.highc += int(line[L2RC]) + int(line[L3RC])
        self.highh += int(line[L2RH]) + int(line[L3RH])

        self.habsuccess[int(line[HAB_ATTEMPT])] += line[HAB_SUCCESS] == '3'

    def tostring(self):
        if self.total:
            lowc = str(self.lowc / self.total)
            lowh = str(self.lowh / self.total)
            highc = str(self.highc / self.total)
            highh = str(self.highh / self.total)

            success = percent(self.habsuccess[2] / self.total) + ':' + percent(self.habsuccess[3] / self.total)

            order = [self.team, '', lowh, lowc, highc, highh, PLACE_HOLDER, success, PLACE_HOLDER]
            return SEP.join(order)
        return self.team + ': ' + NO_DATA


def print_header(width):
    logo = '''
                     ,:++:,                      
                   :++++++++:                    
            _     :++++  ++++:     _              
          ,++++:  '++++  ++++' ,:++++;           
         :++  '+:  :++++++++:  +++  ++'          
  ,++,    + THE +'   ':++:'    :+++++:     ,,:,,    
:++++++++++++++++++++++++++++++++++++++++++++-++, 
    +++++ BLAIR ++++ ROBOT +++ PROJECT ++++:   ++'
'+,++++++++++++++++++++++++++++++++++++++++++-++'
 '++++'        '++++++    ++++++'          '':'' 
                '++++++  ++++++'                 
                 '++++++++++++'                  
                  '++++++++++'                    
                   '++++++++'                     
                   :++++++++:                    
                  .++++++++++.                   
                 ++++++''++++++                 
               .++++++'  '++++++.                
              .++++++      ++ 4 +.               
             ;+++++:        '+ 4 +.              
          ;+++++++,          ,+ / +++'           
         '++++++++:          :++ 9 +++'          
         '++' '+++'          '++++'+++'          
          ';   +'              '+'  ;'           
                                 '              
    '''
    logo = logo.replace('\n', '\n' + ' ' * int((width - 50) / 2))
    print(logo)

    print(('{:^' + str(width) + '}').format('FRC Team 449, The Blair Robot Project'))
    print(('{:^' + str(width) + '}').format('Bluetooth Scouting Server'))
    print('-' * width)
    print(('{:^' + str(width) + '}').format('Runs with Python3 on Linux'))
    print(('{:^' + str(width) + '}').format('Writen by Carter Wilson, 2019'))
    print('=' * width + '\n')

    print('Instructions for use:')
    tw = TextWrapper(width=width)
    print(tw.fill(
        'This server is intended for use with the Team 449 scouting app (and strategy app) for android.') + '\n' +
          tw.fill('On each scouting tablet, please launch the scouting app, select your device name from the ' +
                  'popup, and press connect. If there is no popup, press the Bluetooth icon in the top right ' +
                  'corner of the app.') + '\n' +
          tw.fill('When connected, you should receive a popup in the app informing you that a connection was ' +
                  'made, as well as output from this server with the MAC of the device.') + '\n' +
          tw.fill('To quit the server, press Ctrl-C, confirm that you want to quit, wait for the server to close, ' +
                  'and press Ctrl-C again.'))
    print('_' * width + '\n\n')


if __name__ == '__main__':
    main()


# Regenerates headers string
# Copy the return statement of the toString of Match and it will generate it off of the comments
# Alternatively, copy the google doc here (https://docs.google.com/document/d/1o1PA9TC6kWBYI-BygvdmtlZ6l5LsLmh46P6CQnqiw8U/edit?usp=sharing) and set docs to True
def recalc_headers(code, docs=False):
    global HEADERS
    c=code.split('\n')
    if docs:
	    q=list(map(lambda x: x.split('\t')[0].strip(),c))
	else:
	    q=list(map(lambda x: x.split('//')[1].strip(),c))
    HEADERS = ','.join(q)
    return HEADERS
