from aocl import *
import numpy as np


def solve(input_file, p1=True):
    lines = read_lines(input_file)

    history = []
    for line in lines:
        history.append(np.array(ints(line)))

    extrapolated = [extrapolate(h) for h in history]

    if p1:
        return sum(x[-1] for x in extrapolated)
    else:
        return sum(x[0] for x in extrapolated)


def extrapolate(h):
    prev_ex = (0, 0)
    for values in reversed(with_diffs(h)):
        first = values[0] - prev_ex[0]
        last = values[-1] + prev_ex[1]
        prev_ex = (first, last)
    return prev_ex


def with_diffs(h):
    diffs = [h]
    while True:
        diff = diffs[-1][1:] - diffs[-1][:-1]
        if not diff.any():
            break
        diffs.append(diff)
    return diffs


def main():
    _input_file = 'input'
    expected = {
        'input': (1884768153, 1031),
        'example': (114, 2),
    }[_input_file]

    run(__file__, solve, _input_file, expected[0], p1=True)
    run(__file__, solve, _input_file, expected[1], p1=False)


if __name__ == '__main__':
    main()
