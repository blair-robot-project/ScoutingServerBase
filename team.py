from enum import Enum

import dataconstants


# Stores and calculates data about a team, and outputs it in the format of the match strategy sheets
class Team:
    partner = True
    strat_header = 'team: cross | srt lvl | auto(h:c) | pre(h:c) |#| l h | l c | l r | h h | h c | defense |#| ' \
                   '  attempt   | success | time '

    strat_form = '{team:4s}:  {cross:3d}% | {start1:3d}:{start2:3d} | {autoh:4d}:{autoc:4d} |  {preloadh:3d}:{' \
                 'preloadc:3d} |#| {lowh:3.1f} | {lowc:3.1f} |  {lowr:1s}  | {highh:3.1f} | {highc:3.1f} | {' \
                 'defensep:3d}:{defenses:1.1f} |#| {attempt1:3d}:{attempt2:3d}:{attempt3:3d} | {success2:3d}:{' \
                 'success3:3d} | {time2:2d}:{time3:2d} '

    opp_header = 'team: l h | l c | h h | h c | drop(h:c) |  climb  | defense'
    opp_form = '{team:4s}: {lowh:3.1f} | {lowc:3.1f} | {highh:3.1f} | {highc:3.1f} |  ' \
               '{droph:3.1f}:{dropc:3.1f}  | {climb2:3d}:{climb3:3d} | {defensep:3d}:{defenses:1.1f}'

    quick_form = '\033[7m\033[95m{team:s}\033[0m'

    detail_form = '\033[7m\033[95m{team:s}\033[0m\n'

    # noinspection PyArgumentList
    Forms = Enum('Forms', 'strat quick detail')

    total, lowh, lowc, highc, highh = 0, 0, 0, 0, 0
    autocross, start1, start2, prec, preh, autoc, autoh = 0, 0, 0, 0, 0, 0, 0
    droph, dropc = 0, 0
    lowr = False

    comments = ''

    def __init__(self, team, partner=True):
        self.team = team
        self.defense = []
        self.habattempt, self.habsuccess, self.climbtime = [0, 0, 0, 0], [0, 0, 0, 0], [[], []]
        self.climb = [0, 0]
        if not partner:
            self.partner = False
            self.strat_header, self.strat_form = self.opp_header, self.opp_form

    def getteam(self):
        return self.team

    def getheader(self):
        return self.strat_header

    def getcomments(self):
        return self.comments

    def addline(self, line):
        self.total += 1

        self.autocross += int(line[dataconstants.MOVED_FORWARD])
        self.start1 += line[dataconstants.STARTING_LEVEL] == '1'
        self.start2 += line[dataconstants.STARTING_LEVEL] == '2'
        if line[dataconstants.PRELOAD] == '1':
            self.preh += 1
            self.autoh += line[dataconstants.AUTO_PLACE] == '1'
        elif line[dataconstants.PRELOAD] == '2':
            self.prec += 1
            self.autoc += line[dataconstants.AUTO_PLACE] == '1'

        self.lowc += int(line[dataconstants.CSC]) + int(line[dataconstants.L1RC])
        self.lowh += int(line[dataconstants.CSH]) + int(line[dataconstants.L1RH])
        self.highc += int(line[dataconstants.L2RC]) + int(line[dataconstants.L3RC])
        self.highh += int(line[dataconstants.L2RH]) + int(line[dataconstants.L3RH])

        self.droph += int(line[dataconstants.DROP_HATCH])
        self.dropc += int(line[dataconstants.DROP_CARGO])

        if int(line[dataconstants.L1RH]) + int(line[dataconstants.L3RH]) + int(line[dataconstants.L1RH]):
            self.lowr = True

        attempt = int(line[dataconstants.HAB_ATTEMPT])
        self.habattempt[attempt] += 1
        self.habsuccess[attempt] += attempt == int(line[dataconstants.HAB_REACHED])

        if int(line[dataconstants.HAB_SUCCESS]) > 1:
            self.climbtime[int(line[dataconstants.HAB_REACHED]) - 2].append(int(line[dataconstants.CLIMB_TIME]))
            self.climb[int(line[dataconstants.HAB_REACHED]) - 2] += 1

        d = int(line[dataconstants.DEFENSE])
        if d:
            self.defense.append(d)

        comment = line[dataconstants.COMMENTS]
        if comment:
            self.comments += comment + '\n\t'

    def calcvalues(self):
        return {'team': self.team,
                'lowc': self.avg(self.lowc),
                'lowh': self.avg(self.lowh),
                'highc': self.avg(self.highc),
                'highh': self.avg(self.highh),
                'defensep': self.avg(len(self.defense), perc=True),
                'defenses': self.avg(self.defense, itint=False),

                'cross': self.avg(self.autocross, perc=True),
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

                'droph': self.avg(self.droph),
                'dropc': self.avg(self.dropc),
                'climb2': self.avg(self.climb[0], perc=True),
                'climb3': self.avg(self.climb[1], perc=True), }

    def summary(self, form=Forms.strat):
        forms = {self.Forms.strat: self.strat_form, self.Forms.quick: self.quick_form,
                 self.Forms.detail: self.detail_form}
        if self.total:
            return forms[form].format(**self.calcvalues())
        return '{0:4s}: '.format(self.team) + dataconstants.NO_DATA

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
