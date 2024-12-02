from aocl import *


def solve(input_file, p1=True):
    lines = read_lines(input_file)

    reports = list(map(ints, lines))
    if p1:
        return sum(map(is_safe, reports))
    else:
        return sum(map(is_safe_with_modification, reports))


def is_safe(report):
    increasing = None

    for a, b in zip(*(iter(report[i:]) for i in (0, 1))):
        diff = b - a
        if 1 <= abs(diff) <= 3:
            if increasing is None:
                increasing = diff > 0
            elif (diff > 0) != increasing:
                return False
        else:
            return False
    return True


def is_safe_with_modification(report):
    if is_safe(report):
        return True

    return any(is_safe(report[:i] + report[i+1:]) for i in range(len(report)))


def main():
    _input_file = 'input'
    expected = {
        'input': (549, 589),
        'example': (2, 4),
    }[_input_file]

    run(__file__, solve, _input_file, expected[0], p1=True)
    run(__file__, solve, _input_file, expected[1], p1=False)


if __name__ == '__main__':
    main()
