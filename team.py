from abc import ABC, abstractmethod

from dataconstants import CSC, L2RC, L1RC, L1RH, CSH, L3RC, L3RH, L2RH, COMMENTS, NO_DATA


class Team(ABC):
    header = None
    form = None

    total, lowh, lowc, highc, highh = 0, 0, 0, 0, 0
    comments = ''

    def __init__(self, team):
        self.team = team

    def getteam(self):
        return self.team

    def getheader(self):
        return self.header

    def getcomments(self):
        return self.comments

    def addline(self, line):
        self.total += 1

        self.lowc += int(line[CSC]) + int(line[L1RC])
        self.lowh += int(line[CSH]) + int(line[L1RH])
        self.highc += int(line[L2RC]) + int(line[L3RC])
        self.highh += int(line[L2RH]) + int(line[L3RH])

        comment = line[COMMENTS]
        if comment:
            self.comments += comment + '\n\t'

    @abstractmethod
    def calcvalues(self):
        ...

    def tostring(self):
        if self.total:
            return self.form.format(**self.calcvalues())
        return self.team + ': ' + NO_DATA

    @staticmethod
    def percent(n):
        return int(n * 100)

    @staticmethod
    def avg(l):
        return int(sum(l) / (1 if len(l) == 0 else len(l)))
