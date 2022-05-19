from enum import Enum

from scoutingserver import dataconstants
from scoutingserver.config import EventConfig, FieldType
from scoutingserver import scoring


# Stores and calculates data about a team, and outputs it in the format of the match strategy sheets
class Team:
    partner = True

    NO_DATA = "No data avalible"

    def __init__(self, team, config: EventConfig, partner=True):
        self.total = 0
        self.config = config

        self.team = team
        self.stats = {}
        self.comments = []

        self.set_partner(partner)

    def set_partner(self, partner):
        self.partner = partner
        if partner:
            self.strat_header, self.strat_form = self.ally_header, self.ally_form
        else:
            self.strat_header, self.strat_form = self.opp_header, self.opp_form

    def get_team(self):
        return self.team

    def get_header(self):
        return self.strat_header

    def get_comments(self):
        return "\n\t".join(self.comments)

    def add_match(self, match):
        self.total += 1

        for field in self.config.field_configs:
            if field.typ == FieldType.NUM:
                if field.name not in self.stats:
                    self.stats[field.name] = 0
                self.stats[field.name] += match[field.name]
            elif field.typ == FieldType.BOOL:
                if field.name not in self.stats:
                    self.stats[field.name] = 0
                if match[field.name]:
                    self.stats[field.name] += 1
            elif field.typ == FieldType.CHOICE:
                if field.name not in self.stats:
                    self.stats[field.name] = {choice: 0 for choice in field.choices}
                self.stats[field.name][match[field.name]] += 1
            elif field.typ == FieldType.TEXT:
                if field.name not in self.stats:
                    self.stats[field.name] = []
                if match[field.name]:
                    self.stats[field.name].append(match[field.name])

        self.comments.append(match["comments"])

    def calc_values(self):
        res = {"team": self.team}

        field_configs = self.config.field_configs
        for field in field_configs:
            stat = self.stats[field.name]
            if field.typ == FieldType.NUM:
                res[field.name] = stat / self.total if stat != 0 else 0
            elif field.typ == FieldType.BOOL:
                avg = stat / self.total if stat != 0 else 0
                # Convert to percent
                res[field.name] = int(avg * 100)
            elif field.typ == FieldType.CHOICE:
                # Make a new column for every choice
                for choice in field.choices:
                    res[f"{field.name}_{choice}"] = stat[choice]

        return res

    def summary(self, quick=True):
        """
        Summarize the stats, augmented with year-specific calculations from
        scoring.py

        Parameters:
        quick: Whether the quick version should be given instead of the more detailed one.
        """
        if self.total == 0:
            return "{0:>4s}: ".format(self.team) + self.NO_DATA

        stats = self.calc_values()
        get_extra_stats = (
            scoring.calc_quick_stats if quick else scoring.calc_detailed_stats
        )
        stats.update(get_extra_stats())

        field_names = sorted(stats.keys())
        return "\n".join(stats[field] for field in field_names)
