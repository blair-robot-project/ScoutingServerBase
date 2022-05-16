import json
import os

from enum import Enum

from scoutingserver.interface import printing
from scoutingserver.config import EventConfig

JSON_FILE_NAME = "data.json"
CSV_FILE_NAME = "data.csv"
TBA_SAVE_FILE = "tba.json"

MESSAGE_SIZE = 1024

class DataConstants:
    def __init__(self, data_dir):
        self.abs_data_dir = os.path.abspath(data_dir)
        self.JSON_FILE_PATH = os.path.join(self.abs_data_dir, JSON_FILE_NAME)
        self.CSV_FILE_PATH = os.path.join(self.abs_data_dir, CSV_FILE_NAME)

        config_path = input("Config file: ")
        config = json.loads(open(config_path), object_hook=EventConfig.from_dict)

        # The location of the removable device to copy data to
        self.DRIVE = input("Flash drive location (e.g. 'D:') (default none) ")
