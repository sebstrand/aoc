from aocl import *
import numpy as np


def solve(input_file, smudge):
    lines = read_lines(input_file, skip_empty=False)

    patterns = []
    pattern = []
    for r, line in enumerate(lines):
        if line:
            pattern.append([(0, 1)[c == '#'] for c in line])
        else:
            patterns.append(np.array(pattern, dtype=np.byte))
            pattern = []

    patterns.append(np.array(pattern, dtype=np.byte))

    result = 0
    for pattern in patterns:
        row, col = process_pattern(pattern, smudge=smudge)
        result += row + 100 * col

    return result


def process_pattern(pattern, smudge=False):
    rows, cols = pattern.shape

    smudged = False

    for r in range(1, rows):
        for d in range(rows):
            rn = r - d - 1
            rs = r + d

            if rn < 0 or rs >= rows:
                if not smudge or smudged:
                    return 0, r
                break
            else:
                diff = pattern[rn] != pattern[rs]
                if np.any(diff):
                    if smudge and not smudged and np.count_nonzero(diff) == 1:
                        smudged = True
                    else:
                        smudged = False
                        break

    for c in range(1, cols):
        for d in range(cols):
            cw = c - d - 1
            ce = c + d

            if cw < 0 or ce >= cols:
                if not smudge or smudged:
                    return c, 0
                break
            else:
                diff = pattern[:, cw] != pattern[:, ce]
                if np.any(diff):
                    if smudge and not smudged and np.count_nonzero(diff) == 1:
                        smudged = True
                    else:
                        smudged = False
                        break

    print('failed pattern:\n', pattern)
    assert False


def main():
    _input_file = 'input'
    expected = {
        'input': (36448, 35799),
        'example': (405, 400),
    }[_input_file]

    run(__file__, solve, _input_file, expected[0], smudge=False)
    run(__file__, solve, _input_file, expected[1], smudge=True)


if __name__ == '__main__':
    main()
