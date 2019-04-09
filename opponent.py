import dataconstants
from team import Team


# Calculates data we want for teams on the other alliance
class Opponent(Team):
    droph, dropc = 0, 0

    header = 'team: l h | l c | h h | h c | drop(h:c) | climb | defense'
    form = '{team:4s}: {lowh:3.1f} | {lowc:3.1f} | {highh:3.1f} | {highc:3.1f} |  ' \
           '{droph:3.1f}:{dropc:3.1f}  | {climb2:3d}:{climb3:3d} | {defensep:3d}:{defenses:1.1f}'

    def __init__(self, team):
        super().__init__(team)
        self.climb, self.defense = [0, 0], []

    def addline(self, line):
        super().addline(line)

        self.droph += int(line[dataconstants.DROP_HATCH])
        self.dropc += int(line[dataconstants.DROP_CARGO])

        if int(line[dataconstants.HAB_REACHED]) > 1:
            self.climb[int(line[dataconstants.HAB_REACHED]) - 2] += 1

        d = int(line[dataconstants.DEFENSE])
        if d:
            self.defense.append(d)

    def calcvalues(self):
        v = super().calcvalues()
        v.update({'droph': self.avg(self.droph),
                  'dropc': self.avg(self.dropc),
                  'climb2': self.avg(self.climb[0], perc=True),
                  'climb3': self.avg(self.climb[1], perc=True),
                  'defensep': self.avg(len(self.defense), perc=True),
                  'defenses': self.avg(self.defense, itint=False)})
        return v
