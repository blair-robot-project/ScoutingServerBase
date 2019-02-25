import dataconstants
# from getdata import percent


# Helper function to convert floats to percents and round
def percent(n):
    return str(int(n * 100))


# Calculates data we want for teams on our alliance
class OurAlliance:
    total, autocross, start1, prec, preh, autoc, autoh, lowh, lowc, highc, highh = [0] * 11
    habattempt, habsuccess = [0] * 4, [0] * 4

    def __init__(self, team):
        self.team = team

    def add_line(self, line):
        self.total += 1

        self.autocross += int(line[dataconstants.MOVED_FORWARD])
        self.start1 += line[dataconstants.STARTING_LEVEL] == '1'
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

        self.habattempt[int(line[dataconstants.HAB_ATTEMPT])] += 1
        self.habsuccess[int(line[dataconstants.HAB_ATTEMPT])] += line[dataconstants.HAB_SUCCESS] == '3'

    def tostring(self):
        if self.total:
            autocross = percent(self.autocross / self.total)
            start = self.start1 / self.total
            start_str = percent(start) + ':' + percent(1 - start)
            preload = percent(self.prec / self.total) + ':' + percent(self.preh / self.total)
            accuracy = percent(0 if not self.prec else self.autoc / self.prec) + ':' + percent(
                0 if not self.preh else self.autoh / self.preh)

            lowc = str(self.lowc / self.total)
            lowh = str(self.lowh / self.total)
            highc = str(self.highc / self.total)
            highh = str(self.highh / self.total)

            attempt = percent(self.habattempt[1] / self.total) + ':' + percent(
                self.habattempt[2] / self.total) + ':' + percent(self.habattempt[3] / self.total)
            success = percent(
                0 if not self.habattempt[2] else self.habsuccess[2] / self.habattempt[2]) + ':' + percent(
                0 if not self.habattempt[3] else self.habsuccess[3] / self.habattempt[3])

            order = [self.team, '', autocross, start_str, accuracy, preload, '#', lowh, lowc,
                     dataconstants.PLACE_HOLDER, highc, highh, dataconstants.PLACE_HOLDER, '#', attempt, success,
                     dataconstants.PLACE_HOLDER]
            return dataconstants.SEP.join(order)
        return self.team + ': ' + dataconstants.NO_DATA
