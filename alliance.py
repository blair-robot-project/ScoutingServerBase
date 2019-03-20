from abc import ABC, abstractmethod


class Alliance(ABC):
    header = None
    comments = ''

    def __init__(self, team):
        self.team = team

    def getteam(self):
        return self.team

    def getheader(self):
        return self.header

    def getcomments(self):
        return self.comments

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
