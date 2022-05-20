import json
from enum import Enum
from typing import List


class FieldType(Enum):
    NUM = 1
    BOOL = 2
    CHOICE = 3
    TEXT = 4


class FieldConfig:
    """Configuration for a field"""

    name: str
    type: FieldType
    #: UUID for corresponding GATT characteristic
    char_id: str

    min: float
    max: float
    inc: float

    choices: List[str]
    default_choice: str

    def __init__(
        self,
        name: str,
        type: FieldType,
        char_id: str,
        min=0.0,
        max=100.0,
        inc=1.0,
        choices: List[str] = [],
        default_choice="",
    ):
        self.name = name
        self.type = type
        self.char_id = char_id

        # Only if typ is NUM
        self.min = min
        self.max = max
        self.inc = inc

        # Only if typ is CHOICE
        self.choices = choices
        self.default_choice = default_choice

    def from_dict(dict):
        name = dict["name"]
        typ = FieldType[dict["type"].upper()]
        charac = dict["charId"]
        if typ == FieldType.NUM:
            return FieldConfig(
                name,
                type,
                float(dict.get("min", 0)),
                float(dict["max"]),
                float(dict.get("inc", 0)),
            )

        elif typ == FieldType.BOOL:
            return FieldConfig(name, typ, charac)
        elif typ == FieldType.CHOICE:
            return FieldConfig(
                name,
                typ,
                charac,
                choices=dict["choices"],
                default_choice=dict["defaultChoice"],
            )
        else:
            return FieldConfig(name, typ, charac)


class GeneralFields:
    """Configs for fields that will be sent each year"""

    all = []
    """Holds all the general field configs"""

    def _gen_field_config(*args, **kwargs) -> FieldConfig:
        cfg = FieldConfig(*args, **kwargs)
        all.append(cfg)
        return cfg

    MatchNum = _gen_field_config(
        "MatchNum",
        FieldType.NUM,
        "a3c1723b-b439-43f0-a2b0-acb724c64528",
        min=1,
        max=300,
        inc=1,
    )
    RecorderName = _gen_field_config(
        "recorderName", FieldType.TEXT, "63b525ee-5c90-4775-b9d8-2b2de19d43c3"
    )
    TeamNum = _gen_field_config(
        "TeamNum",
        FieldType.NUM,
        "dce8aaf2-12e3-43c2-a915-fdf6750981fa",
        min=0,
        max=1000000,
        inc=1,
    )
    Alliance = _gen_field_config(
        "alliance",
        FieldType.CHOICE,
        "aa0c3c5e-4f0f-46d7-828c-ec7f7518f41e",
        choices=["Blue", "Red"],
    )
    Station = _gen_field_config(
        "station",
        FieldType.NUM,
        "3474f023-5a13-4b90-bb01-89eab3a8d58e",
        min=1,
        max=3,
        inc=1,
    )
    Timestamp = _gen_field_config(
        "timestamp", FieldType.TEXT, "e6343506-5225-44bf-853f-ffe51b20985e"
    )
    Revision = _gen_field_config(
        "revision",
        FieldType.NUM,
        "147da5b9-864c-41ec-a231-b2a45ac96afd",
        min=0,
        max=100,
        inc=1,
    )
    Comments = _gen_field_config(
        "comments", FieldType.TEXT, "6592806f-553e-47f6-bde4-6d29555227c8"
    )


class EventConfig:
    def __init__(
        self,
        event_name: str,
        our_team: int,
        alliance_size: int,
        service_id: str,
        spec_field_configs: List[FieldConfig],
    ):
        self.event_name = event_name
        self.our_team = our_team
        self.alliance_size = alliance_size
        self.service_id = service_id
        self.spec_field_configs = spec_field_configs
        """The field configs specific to that year"""
        self.field_configs = GeneralFields.all + spec_field_configs

    def from_dict(dict):
        return EventConfig(
            dict["eventName"],
            int(dict.get("ourTeam", 449)),
            int(dict.get("allianceSize", 3)),
            dict["serviceId"],
            dict["fields"],
        )


def _event_config_hook(dict):
    if "eventName" in dict:
        # Must be an event
        return EventConfig.from_dict(dict)
    else:
        # Must be a field
        return FieldConfig.from_dict(dict)


def load_config(config_path) -> EventConfig:
    """Load a config given the config's path"""
    return json.load(open(config_path), object_hook=_event_config_hook)
