import socket
from threading import Thread

import printing
from connection import Connection
from datactl import addtoqueue
from system import gethostMAC

PORT = 1
BACKLOG = 1
# Max message size
SIZE = 1024

# Associates MAC addresses of the kindles with their user friendly names
MAC_DICT = {'00:FC:8B:3B:42:46': 'R1 Demeter',
            '00:FC:8B:39:C1:09': 'R2 Hestia',
            '78:E1:03:A3:18:78': 'R3 Hera',
            '78:E1:03:A1:E2:F2': 'B1 Hades',
            '78:E1:03:A4:F7:70': 'B2 Poseidon',
            '00:FC:8B:3F:E4:EF': 'B3 Zeus',
            '00:FC:8B:3F:28:28': 'Backup 1',
            '44:65:0D:E0:D6:3A': 'Strategy Tablet'}


def recieve_msg(msg, name):
    addtoqueue(msg, name)


class SocketCtl:
    clients = set()
    connecting = False

    def __init__(self):
        self.host_mac = gethostMAC()

        # Setup server socket
        self.server_sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        self.server_sock.bind((self.host_mac, PORT))
        self.server_sock.listen(BACKLOG)
        self.server_sock.settimeout(None)

    def start_connecting(self):
        self.connecting = True
        Thread(target=self.connect).start()

    def connect(self):
        while self.connecting:
            # Wait for connection
            client_sock, client_info = self.server_sock.accept()

            # Setup connection
            connection = Connection(client_sock, MAC_DICT.get(client_info[0], client_info[0]),
                                    lambda msg: recieve_msg(msg, connection.name),
                                    lambda: self.clients.remove(connection))
            self.clients.add(connection)

            # Listen for data
            connection.start_listening()

    def blanket_send(self, msg):
        for connection in self.clients:
            connection.send(msg)

    # Closes all connections and the server
    def close(self):
        self.connecting = False
        for connection in self.clients:
            connection.close()
        self.clients.clear()
        self.server_sock.close()
        printing.printf('Closed server', style=printing.STATUS, log=True, logtag='socketctl.close')
