import json
import os

from enum import Enum

from scoutingserver.interface import printing
from scoutingserver.config import event_config_hook

JSON_FILE_NAME = "data.json"
CSV_FILE_NAME = "data.csv"
TBA_SAVE_FILE = "tba.json"

MESSAGE_SIZE = 1024


class DataConstants:
    def __init__(self, data_dir):
        self.abs_data_dir = os.path.abspath(data_dir)
        self.JSON_FILE_PATH = os.path.join(self.abs_data_dir, JSON_FILE_NAME)
        self.CSV_FILE_PATH = os.path.join(self.abs_data_dir, CSV_FILE_NAME)

