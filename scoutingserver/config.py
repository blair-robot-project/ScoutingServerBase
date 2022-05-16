from enum import Enum


class EventConfig:
    def __init__(self, event_name, field_configs):
        self.event_name = event_name
        self.field_configs = field_configs

    def from_dict(dict):
        return EventConfig(
            dict["eventName"],
            list(map(FieldConfig.from_dict, dict["fields"])),
        )


class FieldConfig:
    def __init__(
        self,
        name: str,
        typ: FieldType,
        min=0,
        max=100,
        inc=1,
        choices=[],
        default_choice="",
    ):
        self.name = name
        self.typ = typ

        # Only if typ is NUM
        self.min = min
        self.max = max
        self.inc = inc

        # Only if typ is CHOICE
        self.choices = choices
        self.default_choice = default_choice

    def from_dict(dict):
        name = dict["name"]
        typ = Field[dict["type"]]
        if typ == FieldType.NUM:
            return FieldConfig(
                name,
                type,
                float(dict.get("min", 0)),
                float(dict["max"]),
                float(dict.get("inc", 0)),
            )

        elif typ == FieldType.BOOL:
            return FieldConfig(name, typ)
        elif typ == FieldType.CHOICE:
            return FieldConfig(
                name, typ, choices=dict["choices"], default_choice=dict["defaultChoice"]
            )
        else:
            return FieldConfig(name, typ)


class FieldType(Enum):
    NUM = 1
    BOOL = 2
    CHOICE = 3
    TEXT = 4
