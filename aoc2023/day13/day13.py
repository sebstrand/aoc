from aocl import *
import numpy as np


def main():
    lines = read_lines('input', skip_empty=False)

    patterns = []
    pattern = []
    for r, line in enumerate(lines):
        if line:
            pattern.append([(0, 1)[c == '#'] for c in line])
        else:
            patterns.append(np.array(pattern, dtype=np.byte))
            pattern = []

    patterns.append(np.array(pattern, dtype=np.byte))

    smudge = True
    result = 0
    for pattern in patterns:
        row, col = process_pattern(pattern, smudge=smudge)
        result += row + 100 * col

    print('result:', result)
    if smudge:
        assert result == 35799
    else:
        assert result == 36448


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


if __name__ == '__main__':
    main()
