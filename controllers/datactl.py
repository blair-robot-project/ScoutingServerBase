import json
from queue import Queue

from dataconstants import Fields, ABS_DATA_DIR, JSON_FILE, CSV_FILE, ORDER
from controllers import systemctl


class DataController:
    data_queue = Queue()
    data = dict()
    data_changed = True

    def __init__(self):
        if False:  # TODO: Check for file
            self.data = load_json_file()

    def queue_data(self, data, source):
        self.data_queue.put((data, source))

    def update(self):
        # While there is data to add, parse it
        while not self.data_queue.empty():
            self.parse_data(*self.data_queue.get())
        # If there is a flash drive and there is new data for it, upload the data
        if self.data_changed and systemctl.checkdev():
            _update_drive()

    def parse_data(self, data, source):
        if source not in self.data:
            self.data[source] = dict()
        if str(data[Fields.TIMESTAMP]) not in self.data[source]:
            self.data[source][str(data[Fields.TIMESTAMP])] = dict()
        self.data[source][str(data[Fields.TIMESTAMP])][str(data[Fields.REVISION])] = data

        write_json(self.data)
        self.to_csv()
        self.data_changed = True

    def to_csv(self):
        s = ','.join(ORDER) + '\n'
        for v in self.data.values():
            for id in v.values():
                m = id[str(max(map(int, id.keys())))]
                s += ','.join([str(m[f]) for f in ORDER]) + '\n'
        write_file(CSV_FILE, s, mode='w')

    def drive_update_request(self):
        self.data_changed = True


def read_file(file):
    with open(ABS_DATA_DIR + file) as f:
        return f.read()


def write_file(file, s, mode='a'):
    with open(ABS_DATA_DIR + file, mode) as f:
        f.write(s)


def load_json_file():
    with open(ABS_DATA_DIR + JSON_FILE) as f:
        return json.load(f)


def write_json(o):
    with open(ABS_DATA_DIR + JSON_FILE, 'w') as f:
        json.dump(o, f)


# Writes data to a removable device
def _update_drive():
    # TODO: Implement
    ...


def find_missing():
    # TODO: Implement
    ...
