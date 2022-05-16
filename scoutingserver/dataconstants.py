import json
import os

from enum import Enum

from scoutingserver.interface import printing

_LOCAL_CONSTANTS_FILE = "local_constants.json"
FIELD_NAMES_FILE = "fields.txt"
MAC_DICT_FILE = "mac.json"

JSON_FILE_NAME = "data.json"
CSV_FILE_NAME = "data.csv"
TBA_SAVE_FILE = "tba.json"

MESSAGE_SIZE = 1024


class DataConstants:
    def __init__(self, data_dir):
        self.abs_data_dir = os.path.abspath(data_dir)
        self.JSON_FILE_PATH = os.path.join(self.abs_data_dir, JSON_FILE_NAME)
        self.CSV_FILE_PATH = os.path.join(self.abs_data_dir, CSV_FILE_NAME)
        local_consts_path = os.path.join(self.abs_data_dir, _LOCAL_CONSTANTS_FILE)
        try:
            local_constants = json.load(open(local_consts_path))
        except FileNotFoundError:
            print("Please enter the following file names and directory locations:")
            local_constants = {"TEAM": input("Team number (e.g. 449) "),
                               "EVENT": input("TBA event id (e.g. '2020mdbet') "),
                               "ALLIANCE_SIZE": input("Alliance size (default 3)"),
                               "DRIVE": input("Flash drive location (e.g. 'D:') (default none) ")}
            local_constants["ALLIANCE_SIZE"] = int(local_constants["ALLIANCE_SIZE"] or 3)
            with open(local_consts_path, "w") as f:
                json.dump(local_constants, f)

        self.TEAM = local_constants["TEAM"]
        self.EVENT = local_constants["EVENT"]
        # The location of the removable device to copy data to
        self.DRIVE = local_constants["DRIVE"]
        self.ALLIANCE_SIZE = local_constants["ALLIANCE_SIZE"]

        # Load the field names from fields.txt
        field_names_file = os.path.join(self.abs_data_dir, FIELD_NAMES_FILE)
        if not os.path.exists(field_names_file):
            printing.printf(f"{field_names_file} does not exist",
                            style=printing.ERROR,
                            log=True,
                            logtag="dataconstants.load_fields")
        with open(field_names_file) as field_names:
            try:
                line = next(field_names)
            except StopIteration:
                printing.printf(
                    f"{field_names_file} is empty",
                    style=printing.ERROR,
                    log=True,
                    logtag="dataconstants.load_fields")
                raise
            column_names = [name.strip() for name in line.split()]
            # `name_dict` maps capitalized snake_case field names to camelCase field names (e.g. "TEAM_ID": "teamId")
            name_dict = {_snake_case(name): name for name in column_names}
            # add all the general fields too
            for gen_field in GeneralFields:
                name_dict[gen_field.name] = gen_field.value
            self.FIELD_NAMES = type("Enum", (), name_dict)()
            self.ORDER = list(name_dict.values())

        # Get MAC address of clients
        mac_file_path = os.path.join(self.abs_data_dir, MAC_DICT_FILE)
        if not os.path.exists(mac_file_path):
            printing.printf(f"{mac_file_path} does not exist",
                            style=printing.ERROR,
                            log=True,
                            logtag="dataconstants.load_mac_dict")
        with open(mac_file_path) as mac_file:
            self.MAC_DICT = json.load(mac_file)


class GeneralFields(Enum):
    """These fields will always be included in the app's messages regardless of the specific game."""
    TEAM_ID = "teamId"
    MATCH_ID = "matchId"
    ALLIANCE_COLOR = 'alliance'
    NO_SHOW = 'noShow'
    COMMENTS = 'comments'
    REVISION = 'revision'
    TIMESTAMP = 'timestamp'
    MATCH = 'match'
    TEAM = 'team'
    RECORDER_NAME = "recorderName"


def _snake_case(camel):
    """Turn a camelCase name into CAPITALIZED_SNAKE_CASE"""
    snake = ""
    prev = None
    for char in camel:
        if char.isupper() or (char.isnumeric() and prev and prev.islower()):
            # Only make new words for uppercase letters and numbers
            snake += "_" + char
        else:
            snake += char.upper()
        prev = char
        
    return snake
