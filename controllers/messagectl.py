import hashlib
import json
from enum import Enum

from dataconstants import Fields
from interface import printing


class IncomingMsgTypes(Enum):
    DATA = 'DATA'
    SUMMARY = 'SUMMARY'
    ERROR = 'ERROR'


class OutgoingMsgTypes(Enum):
    DATA_REQUEST = 'DATA_REQUEST'


def check_checksum(deserialized_msg):
    md5 = hashlib.md5()
    md5.update(deserialized_msg['body'].encode())
    checksum = md5.hexdigest()
    return checksum == deserialized_msg['checksum']


def deserialize(msg):
    if msg:
        msg = json.loads(msg)
        if check_checksum(msg):
            try:
                body = json.loads(msg['body'])
            except json.decoder.JSONDecodeError:
                body = msg['body']
            return {'type': IncomingMsgTypes(msg['type']), 'body': body}
    return None


def invalid_msg(msg, client):
    printing.printf('Invalid message from', client.name, ':', str(msg), style=printing.YELLOW,
                    log=True, logtag='messagectl.invalid_msg')


def summarize_data(data, client_name):
    printing.printf('Data from ' + data[Fields.SCOUT_NAME.value] + ' on ' + client_name + ' for team ' +
                    str(data[Fields.TEAM_ID.value]) + ' in match ' + str(data[Fields.MATCH_ID.value]),
                    style=printing.NEW_DATA, log=True, logtag='msgctl.handle_msg')


class MessageController:
    def __init__(self, datactl):
        self.datactl = datactl

    def handle_msg(self, msg, client):
        msg = deserialize(msg)
        if msg is None:
            invalid_msg(msg, client)
        else:
            if msg['type'] == IncomingMsgTypes.DATA:
                self.datactl.queue_data(msg['body'])
                summarize_data(msg['body'], client.name)
            else:
                invalid_msg(msg, client)
