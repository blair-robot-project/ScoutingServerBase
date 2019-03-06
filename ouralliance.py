import dataconstants
from alliance import Alliance


# Calculates data we want for teams on our alliance
class OurAlliance(Alliance):
    header = 'team: cross | start lvl | accuracy(c:h) | pre (c:h) |#| low h | low c | low r | high c | high h | defense |#| ' \
             'attempt | success | time '

    form = '{team:4s}: {cross:4d}% | {start1:3d}:{start2:3d} | {autoc:3d}:{autoh:3d} | {preloadc:3d}:{preloadh:3d} ' \
           '|#| {lowh:2.1f} | {lowc:2.1f} | {lowr:2s} | {highc:2.1f} | {highh:2.1f} | {defense:3d}% |#| ' \
           '{attempt1:3d}:{attempt2:3d}:{attempt3:3d}% | {success2:3d}:{success3:3d}% | {time2:2d}:{time3:2d}'

    total, autocross, start1, start2, prec, preh, autoc, autoh, lowh, lowc, highc, highh, defense = \
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    lowr = False
    habattempt, habsuccess, climbtime = [0, 0, 0, 0], [0, 0, 0, 0], [[], []]
    comments = ''

    def addline(self, line):
        self.total += 1

        self.autocross += int(line[dataconstants.MOVED_FORWARD])
        self.start1 += line[dataconstants.STARTING_LEVEL] == '1'
        self.start2 += line[dataconstants.STARTING_LEVEL] == '2'
        if line[dataconstants.PRELOAD] == '2':
            self.prec += 1
            self.autoc += line[dataconstants.AUTO_PLACE] == '2'
        elif line[dataconstants.PRELOAD] == '3':
            self.preh += 1
            self.autoh += line[dataconstants.AUTO_PLACE] == '3'

        self.lowc += int(line[dataconstants.CSC]) + int(line[dataconstants.L1RC])
        self.lowh += int(line[dataconstants.CSH]) + int(line[dataconstants.L1RH])
        self.highc += int(line[dataconstants.L2RC]) + int(line[dataconstants.L3RC])
        self.highh += int(line[dataconstants.L2RH]) + int(line[dataconstants.L3RH])

        if int(line[dataconstants.L1RH]) + int(line[dataconstants.L3RH]) + int(line[dataconstants.L1RH]):
            self.lowr = True

        self.habattempt[int(line[dataconstants.HAB_ATTEMPT])] += 1
        self.habsuccess[int(line[dataconstants.HAB_ATTEMPT])] += line[dataconstants.HAB_SUCCESS] == '3'

        if int(line[dataconstants.HAB_SUCCESS]) > 1:
            self.climbtime[int(line[dataconstants.HAB_SUCCESS]) - 2].append(int(line[dataconstants.CLIMB_TIME]))

        self.defense += int(line[dataconstants.DEFENSE])

        comment = line[dataconstants.COMMENTS]
        if comment:
            self.comments += comment + '\n'

    def tostring(self):
        if self.total:
            values = {
                'team': self.team,
                'cross': self.percent(self.autocross / self.total),
                'start1': self.percent(self.start1 / self.total),
                'start2': self.percent(self.start2 / self.total),
                'preloadc': self.percent(self.prec / self.total),
                'preloadh': self.percent(self.preh / self.total),
                'autoc': self.percent(0 if not self.prec else self.autoc / self.prec),
                'autoh': self.percent(0 if not self.preh else self.autoh / self.preh),
                'lowc': self.lowc / self.total,
                'lowh': self.lowh / self.total,
                'lowr': 'y' if self.lowr else 'n',
                'highc': self.highc / self.total,
                'highh': self.highh / self.total,
                'attempt1': self.percent(self.habattempt[1] / self.total),
                'attempt2': self.percent(self.habattempt[2] / self.total),
                'attempt3': self.percent(self.habattempt[3] / self.total),
                'success2': self.percent(0 if not self.habattempt[2] else self.habsuccess[2] / self.habattempt[2]),
                'success3': self.percent(0 if not self.habattempt[3] else self.habsuccess[3] / self.habattempt[3]),
                'time2': self.avg(self.climbtime[0]),
                'time3': self.avg(self.climbtime[1]),
                'defense': self.percent(self.defense / self.total),
            }

            # order = [self.team, autocross, start_str, accuracy, preload, lowh, lowc,
            #          dataconstants.PLACE_HOLDER, highc, highh, dataconstants.PLACE_HOLDER, attempt, success,
            #          dataconstants.PLACE_HOLDER]
            # return self.form.format(*order)
            return self.form.format(**values)
        return self.team + ': ' + dataconstants.NO_DATA


    def getcomments(self):
        return self.comments