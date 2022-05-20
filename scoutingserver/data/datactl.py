import csv
import json
import os
from queue import Queue
from typing import Any, Dict, List

from scoutingserver import dataconstants
import scoutingserver.interface.printing as printing
from scoutingserver.data import systemctl
from scoutingserver.dataconstants import (
    JSON_FILE_NAME,
    CSV_FILE_NAME,
    ALL_REVISIONS_CSV_FILE_NAME,
)
from scoutingserver.config import EventConfig, GeneralFields


class DataController:
    data_queue: Queue = Queue()

    match_records: List[Dict[str, Any]]

    data_changed = True

    def __init__(self, config: EventConfig, data_dir, drive):
        """
        Parameters:
        data_dir: Absolute path of directory where data is stored
        drive: Removable drive to copy data onto (e.g. D:)
        """
        self.config = config
        self.data_dir = data_dir
        self.match_records = load_json_file(data_dir)
        """
        A list of the currently received match records. Each record has data about
        only one team during only one match. It does not represent the data of all
        teams during that match.
        """
        self.drive = drive

    def on_receive(self, data: Dict[str, Any], source: str):
        """
        Callback to triggered by bluetoothctl when a peripheral gives new data
        Parameters:
        data: A dictionary of the field names and values
        source: The peripheral device name
        """
        self.data_queue.put((data, source))
        printing.printf(
            ("Data" if data[GeneralFields.Revision.name] == 0 else "Edit")
            + f" from {data[GeneralFields.RecorderName.name]}"
            + f" on {source}"
            + f" for team {data[GeneralFields.TeamNum.name]}"
            + f" in match {data[GeneralFields.MatchNum.name]}",
            style=printing.NEW_DATA,
            log=True,
            logtag="datactl.on_receive",
        )

    def update(self):
        # While there is data to add, parse it
        has_data = not self.data_queue.empty()
        while not self.data_queue.empty():
            new_data, source = self.data_queue.get()
            self.match_records.append(new_data)

        if has_data:
            with open(os.path.join(self.data_dir, JSON_FILE_NAME), "w") as f:
                json.dump(self.latest_revisions(), f)
            self._to_csv(self.latest_revisions(), CSV_FILE_NAME)
            self._to_csv(
                self.match_records, ALL_REVISIONS_CSV_FILE_NAME, suppress_errors=True
            )
            self.data_changed = True

        csv_file_path = os.path.join(self.data_dir, CSV_FILE_NAME)
        # If there is a flash drive and there is new data for it, upload the data
        if self.data_changed and os.path.exists(csv_file_path):
            if self.drive:
                systemctl.copy(
                    csv_file_path,
                    os.path.join(self.drive, os.path.sep + CSV_FILE_NAME),
                )
            elif systemctl.checkdev():
                self._update_drive()
            self.data_changed = False

    def _update_drive(self):
        """Writes data to a removable device (Linux-specific!)"""
        mount_point = systemctl.mount(self.drive)
        if mount_point:
            systemctl.copy(
                os.path.join(self.data_dir, CSV_FILE_NAME),
                os.path.join(mount_point, CSV_FILE_NAME),
            )
            systemctl.unmount()

    def _to_csv(self, match_records, file_name: str, suppress_errors=False):
        field_names = [field.name for field in self.config.field_configs]

        with open(os.path.join(self.data_dir, file_name), "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(field_names)
            for match_record in match_records:
                row = []
                for field_name in field_names:
                    if field_name in match_record:
                        row.append(match_record[field_name])
                    else:
                        row.append("ERROR")
                        if not suppress_errors:
                            timestamp = match_record[GeneralFields.Timestamp.name]
                            revision = match_record[GeneralFields.Revision.name]
                            printing.printf(
                                f"Missing field {field_name} from data entry {timestamp}.{revision}",
                                style=printing.ERROR,
                                log=True,
                                logtag="datactl.to_csv",
                            )
                writer.writerow(row)

    def latest_revisions(self):
        """
        Returns the data with only the latest revisions of every match.
        Matches are uniquely identified by their match name.
        """
        # Maps match names to the latest revision of that match
        latest = {}
        for match in self.match_records:
            match_name = match[GeneralFields.MatchNum.name]
            revision = match[GeneralFields.Revision.name]
            if match not in latest:
                latest[match_name] = match
            elif latest[match_name][GeneralFields.Revision.name] < revision:
                latest[match_name] = match

        return latest.values()

    def drive_update_request(self):
        self.data_changed = True

    def find_missing(self, schedule=None):
        # Maps match names to the teams in that match for whom we have data
        teams_by_match = dict()
        for match in self.latest_revisions():
            match_name = match[GeneralFields.MatchNum.name]
            if match_name not in teams_by_match:
                teams_by_match[match_name] = []
            teams_by_match[match_name].append(match[GeneralFields.TeamNum.name])

        max_match = max(teams_by_match.keys())
        for i in range(1, max_match):
            if i not in teams_by_match:
                teams_by_match[i] = []

        for match, teams in sorted(teams_by_match.items(), key=lambda x: x[0]):
            if schedule:
                expected = schedule[match]["red"] + schedule[match]["blue"]
                missing = []
                extra = []
                for e in expected:
                    if e not in teams:
                        missing.append(e)
                for t in teams:
                    if t not in expected:
                        extra.append(t)
                if missing:
                    printing.printf(
                        f'{match:2}: missing data for team{"s" if len(missing) > 1 else ""} {", ".join(missing)}',
                        style=printing.YELLOW,
                    )
                if extra:
                    printing.printf(
                        f'{match:2}: data for team{"s" if len(extra) > 1 else ""} not in match: {", ".join(extra)}',
                        style=printing.YELLOW,
                    )
            else:
                if len(set(teams)) < self.config.alliance_size * 2:
                    printing.printf(
                        f'{match:2}: missing data, only have team{"s" if len(set(teams)) > 1 else ""} {", ".join(teams)}',
                        style=printing.YELLOW,
                    )
                elif len(set(teams)) > self.config.alliance_size * 2:
                    printing.printf(
                        f'{match:2}: extra data, have teams {", ".join(teams)}',
                        style=printing.YELLOW,
                    )

            dups = set(team for team in teams if teams.count(team) > 1)
            if dups:
                printing.printf(
                    f'{match:2}: duplicate entries for {", ".join(dups)}',
                    style=printing.YELLOW,
                )
        printing.printf(f"Data found through match {max_match}", style=printing.TEAL)


def load_json_file(data_dir):
    """Load the latest revision of each match record"""
    path = os.path.join(data_dir, JSON_FILE_NAME)
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write("[]")
    with open(path) as f:
        return json.load(f)
