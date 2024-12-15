
class Terminal:
    CLEAR = '\033[2J'

    NORMAL = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'
    BLINK_OFF = '\033[25m'
    INVERSE_OFF = '\033[27m'

    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'

    B_RED = '\033[91m'
    B_GREEN = '\033[92m'
    B_YELLOW = '\033[93m'
    B_BLUE = '\033[94m'
    B_MAGENTA = '\033[95m'
    B_CYAN = '\033[96m'
    B_WHITE = '\033[97m'


def term_effect(s, *effects):
    """Applies one or more terminal effects (e.g. color and underline) to string s, then resets to
    normal after.

    >>> term_effect('test', Terminal.UNDERLINE, Terminal.B_GREEN)
    '\\x1b[4m\\x1b[92mtest\\x1b[0m'
    """
    return ''.join(effects) + s + Terminal.NORMAL


class BoxDraw:
    STYLE_LIGHT = 'light'
    STYLE_HEAVY = 'heavy'
    STYLE_DOUBLE = 'double'

    BOX_CHARS = {
        STYLE_HEAVY: {
            'ud': '┃', 'lr': '━', 'udlr': '╋',
            'dr': '┏', 'dl': '┓', 'ur': '┗', 'ul': '┛',
            'dlr': '┳', 'ulr': '┻', 'udl': '┫', 'udr': '┣',
        },
        STYLE_LIGHT: {
            'ud': '│', 'lr': '─', 'udlr': '┼',
            'dr': '┌', 'dl': '┐', 'ur': '└', 'ul': '┘',
            'dlr': '┬', 'ulr': '┴', 'udl': '┤', 'udr': '├',
        },
        STYLE_DOUBLE: {
            'ud': '║', 'lr': '═', 'udlr': '╬',
            'dr': '╔', 'dl': '╗', 'ur': '╚', 'ul': '╝',
            'dlr': '╦', 'ulr': '╩', 'udl': '╣', 'udr': '╠',
        }
    }

    BLOCK = {
        'solid': '█',
        'dark': '▓',
        'medium': '▒',
        'light': '░',
    }


def box_char(directions, style='light', default='?'):
    """Gets a box drawing character which connects in the given directions. Directions should be a
    collection of characters from the set 'udlr' (up, down, left, right). Style selects the style of
    character from the BoxDraw.STYLE_* values.

    >>> b = box_char
    >>> print(b('dr'),b('lr'),b('dl'),'\\n',b('ud'),' ',b('ud'),'\\n',b('ur'),b('lr'),b('ul'), sep='')
    ┌─┐
    │ │
    └─┘
    """
    cid = []
    if 'u' in directions: cid.append('u')
    if 'd' in directions: cid.append('d')
    if 'l' in directions: cid.append('l')
    if 'r' in directions: cid.append('r')
    return BoxDraw.BOX_CHARS[style].get(''.join(cid), default)
