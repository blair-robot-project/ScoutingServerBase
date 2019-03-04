from abc import ABC, abstractmethod


class Alliance(ABC):
    header = None

    def __init__(self, team):
        self.team = team

    def getheader(self):
        return self.header

    @abstractmethod
    def addline(self, line):
        ...

    @abstractmethod
    def tostring(self):
        ...

    # Helper function to convert floats to percents and round
    @staticmethod
    def percent(n):
        return int(n * 100)
