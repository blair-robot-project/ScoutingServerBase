from dataconstants import CSC, L2RC, L1RC, L1RH, CSH, L3RC, L3RH, L2RH, COMMENTS, NO_DATA


# Abstract
# Stores and calculates data about a team, and outputs it in the format of the match strategy sheets
class Team:
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

    def calcvalues(self):
        return {'team': self.team,
                'lowc':  self.avg(self.lowc),
                'lowh':  self.avg(self.lowh),
                'highc': self.avg(self.highc),
                'highh': self.avg(self.highh)}

    def tostring(self):
        if self.total:
            return self.form.format(**self.calcvalues())
        return self.team + ': ' + NO_DATA

    def avg(self, x, perc=False, itint=True):
        if type(x) in (int, float):
            # Sum average
            r = 0 if not self.total else x / self.total
        else:
            # Iterable average
            r = sum(x) / (1 if len(x) == 0 else len(x))
            if itint:
                r = int(r)
        return r if not perc else self.percent(r)

    @staticmethod
    def percent(n):
        return int(n * 100)
