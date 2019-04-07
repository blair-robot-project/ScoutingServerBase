import dataconstants
from team import Team


# Calculates data we want for teams on our alliance
class Partner(Team):
    header = 'team: cross | srt lvl | auto(h:c) | pre(h:c) |#| l h | l c | l r | h h | h c |  d  |#| ' \
             '  attempt   | success | time '

    form = '{team:4s}:  {cross:3d}% | {start1:3d}:{start2:3d} | {autoh:4d}:{autoc:4d} |  {preloadh:3d}:{preloadc:3d} ' \
           '|#| {lowh:3.1f} | {lowc:3.1f} |  {lowr:1s}  | {highh:3.1f} | {highc:3.1f} | {defense:3d} |#| ' \
           '{attempt1:3d}:{attempt2:3d}:{attempt3:3d} | {success2:3d}:{success3:3d} | {time2:2d}:{time3:2d}'

    autocross, start1, start2, prec, preh, autoc, autoh, defense = 0, 0, 0, 0, 0, 0, 0, 0
    lowr = False

    def __init__(self, team):
        super().__init__(team)
        self.habattempt, self.habsuccess, self.climbtime = [0, 0, 0, 0], [0, 0, 0, 0], [[], []]

    def addline(self, line):
        super().addline(line)

        self.autocross += int(line[dataconstants.MOVED_FORWARD])
        self.start1 += line[dataconstants.STARTING_LEVEL] == '1'
        self.start2 += line[dataconstants.STARTING_LEVEL] == '2'
        if line[dataconstants.PRELOAD] == '1':
            self.preh += 1
            self.autoh += line[dataconstants.AUTO_PLACE] == '1'
        elif line[dataconstants.PRELOAD] == '2':
            self.prec += 1
            self.autoc += line[dataconstants.AUTO_PLACE] == '1'

        if int(line[dataconstants.L1RH]) + int(line[dataconstants.L3RH]) + int(line[dataconstants.L1RH]):
            self.lowr = True

        attempt = int(line[dataconstants.HAB_ATTEMPT])
        self.habattempt[attempt] += 1
        self.habsuccess[attempt] += attempt == int(line[dataconstants.HAB_REACHED])

        if int(line[dataconstants.HAB_SUCCESS]) > 1:
            self.climbtime[int(line[dataconstants.HAB_REACHED]) - 2].append(int(line[dataconstants.CLIMB_TIME]))

        self.defense += int(line[dataconstants.DEFENSE])

    def calcvalues(self):
        v = super().calcvalues()
        v.update({'cross': self.avg(self.autocross, perc=True),
                  'start1': self.avg(self.start1, perc=True),
                  'start2': self.avg(self.start2, perc=True),
                  'preloadc': self.avg(self.prec, perc=True),
                  'preloadh': self.avg(self.preh, perc=True),
                  'autoc': self.percent(0 if not self.prec else self.autoc / self.prec),
                  'autoh': self.percent(0 if not self.preh else self.autoh / self.preh),
                  'lowr': 'y' if self.lowr else 'n',
                  'attempt1': self.avg(self.habattempt[1], perc=True),
                  'attempt2': self.avg(self.habattempt[2], perc=True),
                  'attempt3': self.avg(self.habattempt[3], perc=True),
                  'success2': self.percent(0 if not self.habattempt[2] else self.habsuccess[2] / self.habattempt[2]),
                  'success3': self.percent(0 if not self.habattempt[3] else self.habsuccess[3] / self.habattempt[3]),
                  'time2': self.avg(self.climbtime[0]),
                  'time3': self.avg(self.climbtime[1]),
                  'defense': self.avg(self.defense, perc=True)})
        return v
