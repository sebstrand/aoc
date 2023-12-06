from aocl import *


move_value = {
    'A': 1,
    'B': 2,
    'C': 3,

    'X': 1,
    'Y': 2,
    'Z': 3,
}


def mainp1():
    lines = read_lines('input')

    outcomes = {
        'AX': None,
        'AY': True,
        'AZ': False,

        'BX': False,
        'BY': None,
        'BZ': True,

        'CX': True,
        'CY': False,
        'CZ': None,
    }

    score = 0
    for line in lines:
        opponent, self = splits(line)
        outcome = outcomes[opponent + self]

        score += move_value[self]
        if outcome is None:
            score += 3
        elif outcome:
            score += 6

    print('score p1:', score)
    assert score == 13526


def mainp2():
    lines = read_lines('input')

    plays = {
        'AX': 'C',
        'AY': 'A',
        'AZ': 'B',

        'BX': 'A',
        'BY': 'B',
        'BZ': 'C',

        'CX': 'B',
        'CY': 'C',
        'CZ': 'A',
    }

    score = 0
    for line in lines:
        opponent, desired_outcome = splits(line)

        self = plays[opponent + desired_outcome]
        score += move_value[self]
        if desired_outcome == 'Y':
            score += 3
        elif desired_outcome == 'Z':
            score += 6

    print('score p2:', score)
    assert score == 14204


if __name__ == '__main__':
    mainp1()
    mainp2()
