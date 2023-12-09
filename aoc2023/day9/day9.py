from aocl import *
import numpy as np


def main():
    lines = read_lines('input')

    history = []
    for line in lines:
        history.append(np.array(ints(line)))

    extrapolated = [extrapolate(h) for h in history]

    last_sum = sum(x[-1] for x in extrapolated)
    print('last sum:', last_sum)
    assert last_sum == 1884768153

    first_sum = sum(x[0] for x in extrapolated)
    print('first sum:', first_sum)
    assert first_sum == 1031


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


if __name__ == '__main__':
    main()
