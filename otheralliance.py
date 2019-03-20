import dataconstants
from alliance import Alliance


# Calculates data we want for teams on the other alliance
class OtherAlliance(Alliance):
    total, lowh, lowc, highc, highh, droph, dropc = 0, 0, 0, 0, 0, 0, 0
    comments = ''

    header = 'team: l h | l c | h c | h h | drop(h:c) | climb '
    form = '{team:4s}: {lowh:3.1f} | {lowc:3.1f} | {highc:3.1f} | {highh:3.1f} |  ' \
           '{droph:3.1f}:{dropc:3.1f}  | {climb2:3d}:{climb3:3d}'

    def __init__(self, team):
        super().__init__(team)
        self.climb = [0, 0]

    def addline(self, line):
        self.total += 1

        self.lowc += int(line[dataconstants.CSC]) + int(line[dataconstants.L1RC])
        self.lowh += int(line[dataconstants.CSH]) + int(line[dataconstants.L1RH])
        self.highc += int(line[dataconstants.L2RC]) + int(line[dataconstants.L3RC])
        self.highh += int(line[dataconstants.L2RH]) + int(line[dataconstants.L3RH])

        self.droph += int(line[dataconstants.DROP_HATCH])
        self.dropc += int(line[dataconstants.DROP_CARGO])

        if int(line[dataconstants.HAB_REACHED]) > 1:
            self.climb[int(line[dataconstants.HAB_REACHED]) - 2] += 1

        comment = line[dataconstants.COMMENTS]
        if comment:
            self.comments += comment + ';'

    def tostring(self):
        if self.total:
            values = {
                'team': self.team,

                'lowc': self.lowc / self.total,
                'lowh': self.lowh / self.total,
                'highc': self.highc / self.total,
                'highh': self.highh / self.total,

                'droph': self.droph / self.total,
                'dropc': self.dropc / self.total,

                'climb2': self.percent(self.climb[0] / self.total),
                'climb3': self.percent(self.climb[1] / self.total),
            }
            return self.form.format(**values)
        return self.team + ': ' + dataconstants.NO_DATA
