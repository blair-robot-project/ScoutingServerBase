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

    @staticmethod
    def percent(n):
        return int(n * 100)

    @staticmethod
    def avg(l):
        return int(sum(l) / (1 if len(l) == 0 else len(l)))
