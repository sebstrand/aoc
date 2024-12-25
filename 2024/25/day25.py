from itertools import product
from aocl import *


LOCK_WIDTH = 5
LOCK_HEIGHT = 7


def solve(input_file):
    lines = read_lines(input_file)

    locks = []
    keys = []
    for i in range(0, len(lines), LOCK_HEIGHT):
        current = [0] * LOCK_WIDTH
        if lines[i] == '#' * LOCK_WIDTH:
            locks.append(current)
            item_slice = slice(i + 1, i + LOCK_HEIGHT)
        else:
            keys.append(current)
            item_slice = slice(i, i + LOCK_HEIGHT - 1)

        for row in lines[item_slice]:
            for col, char in enumerate(row):
                if char == '#':
                    current[col] += 1

    return sum(fit(lock, key) for lock, key in product(locks, keys))


def fit(lock, key):
    return all(l + k <= LOCK_HEIGHT - 2 for l, k in zip(lock, key))


def main():
    _input_file = 'input'
    expected = {
        'input': 2854,
        'example': 3,
    }[_input_file]

    run(__file__, solve, _input_file, expected)


if __name__ == '__main__':
    main()
