BASE = '\033[9'
BASE_END = 'm'

ENDC = '\033[0m'

NORMAL = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
HIGHLIGHT = '\033[7m'


def makecolor(i):
    return BASE + str(i) + BASE_END


DARKGRAY, RED, GREEN, YELLOW, BLUE, PURPLE, TEAL, LIGHTGRAY, DEFAULT = [makecolor(i) for i in range(9)]

CONNECTED = GREEN
DISCONNECTED = RED
STATUS = YELLOW
NEW_DATA = BLUE
DATA_OUTPUT = PURPLE
FLASH_DRIVE = TEAL
ERROR = (RED, BOLD)
QUIT = (RED, HIGHLIGHT)

LOGO = (RED, BOLD)
HEADER = RED
TITLE = (DEFAULT, BOLD)
INSTRUCTIONS = DEFAULT


def printf(*args, style=(DEFAULT, NORMAL), **kwargs):
    endc = ENDC
    if type(style) == tuple:
        endc *= len(style)
        style = ''.join(style)
    elif not type(style) == str:
        print(*args, **kwargs)
    end = endc + kwargs.pop('end', '\n')
    print(style, end='')
    print(*args, **kwargs, end=end)
