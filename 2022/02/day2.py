from aocl import *


move_value = {
    'A': 1,
    'B': 2,
    'C': 3,

    'X': 1,
    'Y': 2,
    'Z': 3,
}


def solve(input_file, p1=True):
    lines = read_lines(input_file)

    if p1:
        return solve_p1(lines)
    else:
        return solve_p2(lines)


def solve_p1(lines):
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
    return score


def solve_p2(lines):
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
    return score


def main():
    _input_file = 'input'
    expected = {
        'input': (13526, 14204),
        'example': (15, 12),
    }[_input_file]

    run(__file__, solve, _input_file, expected[0], p1=True)
    run(__file__, solve, _input_file, expected[1], p1=False)


if __name__ == '__main__':
    main()
