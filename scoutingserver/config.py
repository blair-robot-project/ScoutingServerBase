from enum import Enum
from typing import List


class FieldType(Enum):
    NUM = 1
    BOOL = 2
    CHOICE = 3
    TEXT = 4


class GeneralFields:
    """Fields that will be sent each year"""
    TEAM_NUMBER = "teamNumber"
    ALLIANCE = "alliance"
    STATION = "station"
    COMMENTS = "comments"


class FieldConfig:
    def __init__(
        self,
        name: str,
        typ: FieldType,
        characId: str,
        min=0.0,
        max=100.0,
        inc=1.0,
        choices=[],
        default_choice="",
    ):
        self.name = name
        self.typ = typ
        self.characId = characId

        # Only if typ is NUM
        self.min = min
        self.max = max
        self.inc = inc

        # Only if typ is CHOICE
        self.choices = choices
        self.default_choice = default_choice


class EventConfig:
    def __init__(
        self,
        event_name: str,
        our_team: int,
        alliance_size: int,
        field_configs: List[FieldConfig],
    ):
        self.event_name = event_name
        self.our_team = our_team
        self.alliance_size = alliance_size
        self.field_configs = field_configs


def event_config_hook(dict):
    if "eventName" in dict:
        # Must be an event
        return EventConfig(
            dict["eventName"],
            int(dict.get("ourTeam", 449)),
            int(dict.get("alliance_size", 3)),
            dict["fields"],
        )
    else:
        # Must be a field
        name = dict["name"]
        typ = FieldType[dict["type"].upper()]
        charac = dict["characId"]
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
                name, typ, charac, choices=dict["choices"], default_choice=dict["defaultChoice"]
            )
        else:
            return FieldConfig(name, typ, charac)
