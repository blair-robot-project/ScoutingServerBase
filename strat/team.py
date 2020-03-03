from enum import Enum

# from dataconstants import Fields

def enum(**enums):
    return type('Enum', (), enums)

FieldsEnum = enum(TEAM_ID='teamId',
                  MATCH_ID='matchId',
                  ALLIANCE_COLOR='alliance',
                  NO_SHOW='noShow',
                  PRELOAD='preload',
                  AUTO_MOVE='autoMove',
                  HIT_PARTNER='hitPartner',
                  AUTO_INTAKE='autoIntake',
                  AUTO_CENTER='autoCenter',
                  AUTO_LOW='autoLow',
                  AUTO_MISS='autoMiss',
                  HIGH='high',
                  CENTER='center',
                  LOW='low',
                  MISS='miss',
                  SPINNER_ROT='spinnerRot',
                  SPINNER_POS='spinnerPos',
                  ATTEMPTED_CLIMB='attemptedClimb',
                  PARK='park',
                  SOLO_CLIMB='soloClimb',
                  DOUBLE_CLIMB='doubleClimb',
                  WAS_LIFTED='wasLifted',
                  CLIMB_TIME='climbTime',
                  ENDGAME_SCORE='endgameScore',
                  LEVEL='level',
                  DEAD='dead',
                  DEFENSE='defense',
                  COMMENTS='comments',
                  SCOUT_NAME='scoutName',
                  REVISION='revision',
                  TIMESTAMP='timestamp',
                  MATCH='match',
                  TEAM='team',
                  SOLO_CLIMB_NYF='soloClimbNYF',
                  DOUBLE_CLIMB_NYF='doubleClimbNYF',
                  WAS_LIFTED_NYF='wasLiftedNYF')

Fields = FieldsEnum()

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

    quick_form = '\033[7m\033[95m{team:4s}\033[0m SS:{autoh:3d}:{autoc:3d} H:{allhatch:2.1f} C:{allcargo:2.1f} ' \
                 'HI:{height:2s} EG:{success2:3d}:{success3:3d}'

    detail_form = '\033[7m\033[95m{team:4s}\033[0m\n'

    NO_DATA = 'No data avalible'

    Forms = Enum('Forms', 'strat quick detail')


    def __init__(self, team, partner=True):
        self.total = 0

        self.team = team
        self.auto_move, self.hit_partner, self.auto_intake, self.auto_low, self.auto_high, self.auto_center, self.auto_miss = 0, 0, 0, 0, 0, 0, 0
        self.low, self.high, self.center, self.miss = 0, 0, 0, 0
        self.spinner2, self.spinner3 = False, False
        self.climb_attempts, self.climb_success = 0, 0
        self.climb_time = []
        self.dead = []
        self.defense = []
        self.comments = []

        if not partner:
            self.partner = False
            self.strat_header, self.strat_form = self.opp_header, self.opp_form

    def get_team(self):
        return self.team

    def get_header(self):
        return self.strat_header

    def get_comments(self):
        return '\n\t'.join(self.comments)

    def add_match(self, match):
        self.total += 1

        self.auto_move += match[Fields.AUTO_MOVE]
        self.hit_partner += match[Fields.HIT_PARTNER]
        self.auto_intake += match[Fields.AUTO_INTAKE]
        self.auto_low += match[Fields.AUTO_LOW]
        self.auto_high += match[Fields.AUTO_HIGH]
        self.auto_center += match[Fields.AUTO_CENTER]
        self.auto_miss += match[Fields.AUTO_MISS]

        self.low += match[Fields.LOW]
        self.high += match[Fields.HIGH]
        self.center += match[Fields.CENTER]
        self.miss += match[Fields.MISS]
        self.spinner2 = self.spinner2 or match[Fields.SPINNER_ROT]
        self.spinner3 = self.spinner2 or match[Fields.SPINNER_POS]

        self.climb_attempts += match[Fields.ATTEMPTED_CLIMB] in (1, 2)
        self.climb_success += match[Fields.SOLO_CLIMB_NYF] == 1 or match[Fields.DOUBLE_CLIMB_NYF] ==1

        #self.dead
        #self.defense

        comment = match[Fields.COMMENTS]
        if comment:
            self.comments.append(comment)

    def calc_values(self):
        return {
                'team': self.team,
               }

    def summary(self, form=Forms.strat):
        forms = {self.Forms.strat: self.strat_form, self.Forms.quick: self.quick_form,
                 self.Forms.detail: self.detail_form}
        if self.total:
            return forms[form].format(**self.calc_values())
        return '{0:4s}: '.format(self.team) + self.NO_DATA

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


def percent(n):
    return int(n * 100)
