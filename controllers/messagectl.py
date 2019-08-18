import hashlib
import json
from enum import Enum

from interface import printing


class IncomingMsgTypes(Enum):
    DATA = 'DATA'
    SUMMARY = 'SUMMARY'


class OutgoingMsgTypes(Enum):
    DATA_REQUEST = 'DATA_REQUEST'


def check_checksum(deserialized_msg):
    md5 = hashlib.md5()
    md5.update(deserialized_msg['body'].encode())
    checksum = md5.hexdigest()
    return checksum == deserialized_msg['checksum']


def deserialize(msg, client_name):
    msg = json.loads(msg)
    if check_checksum(msg):
        body = json.loads(msg['body'])
        return {'type': IncomingMsgTypes(msg['type']), 'body': body, 'client_name': client_name}
    else:
        return None


def invalid_msg(msg, client):
    printing.printf('Invalid message from', client.name, ':', msg, style=printing.YELLOW,
                    log=True, logtag='messagectl.invalid_msg')


class MessageController:
    def __init__(self, datactl):
        self.datactl = datactl

    def handle_msg(self, msg, client):
        msg = deserialize(msg, client.name)
        if msg is None:
            # TODO: Handle failed messages
            pass
        else:
            if msg['type'] == IncomingMsgTypes.DATA:
                self.datactl.queue_data(msg['body'])
            else:
                invalid_msg(msg, client)
