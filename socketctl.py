import socket
from threading import Thread

import printing
from dataconstants import GETDATA_TRIGGER, NAME, TEAM, MATCH
from datactl import addtoqueue
from getdata import getdata
from system import gethostMAC

# This should be the MAC address of your Bluetooth adapter
# Carter's desktop (essuomelpmap)
# HOST_MAC = '00:1A:7D:DA:71:13'
# Nate's laptop (DESKTOP-9HL0MM7)
# HOST_MAC = 'E4:F8:9C:BC:93:0E'
# Carter's laptop (gallium)
# HOST_MAC = 'A4:C4:94:4F:6F:63'


PORT = 1
BACKLOG = 1
SIZE = 1024

MAC_DICT = {'78:E1:03:A4:F7:70': 'Poseidon',
            '00:FC:8B:3B:42:46': 'Demeter',
            '00:FC:8B:39:C1:09': 'Hestia',
            '78:E1:03:A1:E2:F2': 'Hades',
            '78:E1:03:A3:18:78': 'Hera',
            '???': '???',
            '00:FC:8B:3F:28:28': 'Backup 1',
            '00:FC:8B:3F:E4:EF': 'Zeus',#'Backup 2',
            '44:65:0D:E0:D6:3A': 'Strategy Tablet'}
            
            
def init():
	global server_sock, clients
	
	HOST_MAC = gethostMAC()
	
	# Setup server socket
	server_sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
	server_sock.bind((HOST_MAC, PORT))
	server_sock.listen(BACKLOG)
	server_sock.settimeout(None)

	clients = []
	

# Read loop to continually read data from a client
def read(sock, info):
    try:
        # Receive data
        data = sock.recv(SIZE)
   
        str_data = data.decode()
        if str_data[:len(GETDATA_TRIGGER)] == GETDATA_TRIGGER:
            # If it is a strategy request, return the data
            printing.printf('Data request ' + str_data[len(GETDATA_TRIGGER) + 1:], style=printing.NEW_DATA)
            # sock.send(bytes(getdata(data.split(':')[1]), 'UTF-8'))
            printing.printf(getdata(str_data.split()[1:]), style=printing.DATA_OUTPUT)
        elif str_data.strip():
            # Add it to the data file
            addtoqueue((info, str_data.strip()))
            # printing.printf summary to server
            match = str_data.split(',')
            printing.printf('Data from ' + match[NAME] + ' on ' + MAC_DICT.get(info, info) + ' for team ' +
                  match[TEAM] + ' in match ' + match[MATCH], style=printing.NEW_DATA)
        # Wait for the next match
        read(sock, info)
    except ConnectionResetError:
        printing.printf('Disconnected from', MAC_DICT.get(info, info), style=printing.DISCONNECTED)
        sock.close()
        clients.remove((sock, info))  
    except TimeoutError:
        printing.printf('Timeout, restarting sock.recv (this is probably fine, though it shouldn\'t be happening)')
        read(sock, info)


# Waits for a device to try to connect, then starts a thread to read that device, and stays open for connections
def connect():
    # Wait for connection
    client_sock, client_info = server_sock.accept()
    # Connect to device
    printing.printf('Accepted connection from', MAC_DICT.get(client_info[0], client_info[0]), style=printing.CONNECTED)
    clients.append((client_sock, client_info[0]))

    # Start reading it
    Thread(target=lambda: read(client_sock, client_info[0])).start()

    # Stay open for connections
    connect()


# Closes all connections and the server
def close():
    for sock in clients:
        sock[0].close()
        printing.printf('Closed connection with', MAC_DICT.get(sock[1],sock[1]), style=printing.STATUS)
    clients.clear()
    server_sock.close()
    printing.printf('Closed server', style=printing.STATUS)
