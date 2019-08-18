from threading import Thread

from interface import printing
from interface.logger import log

SIZE = 1024


class Connection:
    listening = False

    def __init__(self, socket, name, on_recieve, on_closed):
        self.socket = socket
        self.name = name
        self.on_recieve = on_recieve
        self.on_closed = on_closed
        printing.printf('Accepted connection from', name, style=printing.CONNECTED,
                        log=True, logtag='Connection.init')

    def start_listening(self):
        self.listening = True
        Thread(target=self._listen).start()

    def _listen(self):
        while self.listening:
            try:
                self._read(self.socket.recv(SIZE))
            except Exception as e:
                self._closed(e)

    def _read(self, data):
        str_data = data.decode()
        if str_data.strip():
            log('Connection._read.raw', str_data)
            self.on_recieve(str_data)

    def send(self, msg):
        # TODO: Make safe and handle partial sends
        self.socket.send(msg.encode())

    def _closed(self, error):
        self._close()
        printing.printf('Disconnected from', self.name, style=printing.DISCONNECTED,
                        log=True, logtag='Connection.closed')
        if type(error) not in (ConnectionResetError, TimeoutError, OSError):
            print(error)
            try:
                printing.printf('Unexpected disconnect error:', str(error), style=printing.ERROR,
                                log=True, logtag='Con.closed.error')
            except TypeError:
                printing.printf('Unknown disconnect error', style=printing.ERROR,
                                log=True, logtag='Con.closed.error')
        self.on_closed()

    def close(self):
        self._close()
        printing.printf('Closed connection with', self.name, style=printing.STATUS,
                        log=True, logtag='Connection.close')

    def _close(self):
        self.listening = False
        self.socket.close()
