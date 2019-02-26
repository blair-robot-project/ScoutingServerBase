from abc import ABC, abstractmethod


class Alliance(ABC):

    def __init__(self, team):
        self.team = team

    @abstractmethod
    def addline(self, line):
        ...

    @abstractmethod
    def tostring(self):
        ...

    # Helper function to convert floats to percents and round
    @staticmethod
    def percent(n):
        return str(int(n * 100))
