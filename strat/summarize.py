from interface import printing
from dataconstants import ABS_DATA_DIR, TEAM
from interface.logger import log
from strat.team import Team


# Get the data string to return from the list of teams
def strategy(team_numbers):
    log('datactl.getdata', 'Strategy data request for ' + ', '.join(team_numbers))

    teams = _maketeams(team_numbers)

    d = list(map(lambda t: t.summary(), teams))
    log('datactl.getdata', '/'.join(d))
    return teams[0].getheader() + '\n' + '\n'.join(d[:3]) + '\n---\n' + teams[3].getheader() + '\n' + \
           '\n'.join(d[3:]) + '\n===\n' + '\n'.join([t.getteam() + ': ' + t.getcomments() for t in teams])


def _maketeams(team_numbers):
    f = open(ABS_DATA_DIR)

    teams = [Team(t, partner=i < 3) for i, t in enumerate(team_numbers)]

    for line in f:
        splitline = line.split(',')
        t = splitline[TEAM]
        if t in team_numbers:
            try:
                teams[team_numbers.index(t)].addline(splitline)
            except IndexError as e:
                printing.printf('Incomplete line in data: ', style=printing.ERROR, log=True,
                                logtag='Team.addline.error')
                printing.printf(line, style=printing.YELLOW, log=True, logtag='Team.addline.error')
                log('Team.addline.error', str(e))
            except Exception as e:
                printing.printf('Unknown error in strategy request: ', style=printing.ERROR, log=True,
                                logtag='Team.addline.error')
                printing.printf(str(e), style=printing.ERROR, log=True, logtag='Team.addline.error')
                printing.printf('On line: ' + line, style=printing.YELLOW, log=True, logtag='Team.addline.error')
    return teams


def detailed_summary(team_numbers):
    teams = _maketeams(team_numbers)
    return list(map(lambda x: x.summary(form=Team.Forms.detail), teams))


def quick_summary(team_numbers):
    teams = _maketeams(team_numbers)
    return list(map(lambda x: x.summary(form=Team.Forms.quick), teams))
