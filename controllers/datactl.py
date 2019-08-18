import json
from queue import Queue

from controllers import systemctl
from dataconstants import DATA_FILE, ABS_DATA_DIR, MEDIA_DIR, Fields
from interface import printing


class DataController:
    data_queue = Queue()
    data = []
    data_changed = True

    def __init__(self):
        # TODO: load existing data
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

    def parsedata(self, data):
        print(data)
        self.data.append(data)


    def driveupdaterequest(self):
        self.data_changed = True


def read_file():
    with open(ABS_DATA_DIR) as f:
        return f.read()


def write_file(s, mode='a'):
    with open(ABS_DATA_DIR, mode) as f:
        f.write(s)


def load_json_fil():
    with open(ABS_DATA_DIR) as f:
        return json.load(f)

# Writes data to a removable device
def _updatedrive():
    # TODO: Implement
    ...


def findmissing():
    # TODO: Implement
    ...
