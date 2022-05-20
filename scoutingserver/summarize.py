from typing import List

from scoutingserver.interface import printing
from scoutingserver.config import EventConfig, GeneralFields
from scoutingserver.data.datactl import load_json_file
from scoutingserver.interface.logger import log
from scoutingserver.team import Team


# Get the data string to return from the list of teams
def strategy(alliances, config: EventConfig, data_dir: str, side=None):
    all_size = config.alliance_size
    if type(alliances) != dict:
        alliances = {"red": alliances[:all_size], "blue": alliances[all_size:]}
    if not side:
        side = "blue" if config.our_team in alliances["blue"] else "red"

    teams_joined = alliances[side] + alliances["blue" if side == "red" else "red"]

    log("datactl.getdata", "Strategy data request for " + ", ".join(teams_joined))

    teams = _maketeams(teams_joined, config, data_dir)

    summaries = [t.summary(quick=True) for t in teams]
    log("datactl.getdata", "/".join(summaries))
    return "\n".join[
        " | ".join(summaries[0].keys()),
        "\n".join(summaries[:all_size].values()),
        "---",
        " | ".join(summaries[all_size].keys()),
        "\n".join(summaries[all_size:].values()),
        "===",
        "\n".join([t.num + ": " + "\n\t".join(t.comments) for t in teams]),
    ]


def _maketeams(
    team_numbers,
    config: EventConfig,
    data_dir: str,
) -> List[Team]:
    match_records = load_json_file(data_dir)

    teams: List[Team] = [Team(num, config) for num in team_numbers]

    for match_record in match_records:
        team_num = match_record[GeneralFields.TeamNum.name]
        if team_num in team_numbers:
            team = [team for team in teams if team.num == team_num]
            if not team:
                printing.printf(
                    "Incomplete match record: ",
                    style=printing.ERROR,
                    log=True,
                    logtag="Team.addline.error",
                )
                printing.printf(
                    match_record,
                    style=printing.YELLOW,
                    log=True,
                    logtag="Team.addline.error",
                )
            try:
                team[0].add_match(match_record)
            except Exception as e:
                printing.printf(
                    "Unknown error in strategy request: ",
                    style=printing.ERROR,
                    log=True,
                    logtag="Team.addline.error",
                )
                printing.printf(
                    str(e),
                    style=printing.ERROR,
                    log=True,
                    logtag="Team.addline.error",
                )
                printing.printf(
                    "For match: " + str(match_record),
                    style=printing.YELLOW,
                    log=True,
                    logtag="Team.addline.error",
                )
    return teams
