from aocl import *
import numpy as np


def solve(input_file, cycles):
    lines = read_lines(input_file)
    rows, cols = len(lines), len(lines[0])

    platform = np.zeros((rows, cols), dtype=np.byte)
    for r, line in enumerate(lines):
        platform[r] = [(0, 1, 2)[(c != '.') + (c == 'O')] for c in line]

    if cycles == 0:
        roll_north(platform)
    else:
        seen = dict()
        cycle = 0
        while cycle < cycles:
            cycle += 1
            for _ in range(4):
                roll_north(platform)
                platform = np.rot90(platform, k=1, axes=(1, 0))

            platform_hash = hash(platform.dumps())
            if platform_hash in seen:
                seen_on = seen[platform_hash]
                repeat_interval = cycle - seen_on
                # print('\nrepeating with cycle', repeat_interval, '- previously seen in cycle', seen_on)
                remaining = (cycles - cycle)
                cycle = cycles - (remaining % repeat_interval) + 0
                # print('jumped to cycle', cycle)
                seen = dict()
            else:
                seen[platform_hash] = cycle
                # print('.', end='')
                # if cycle > 0 and cycle % 50 == 0:
                #     print()

    # print()
    # display(platform)

    load = calc_load(platform)
    return load


def roll_north(platform):
    rows, _ = platform.shape

    for col in platform.transpose():
        fixed_rocks = [r for r in np.nonzero(col == 1)[0]]
        fixed_rocks.append(rows)
        r = 0
        for r2 in fixed_rocks:
            rolling_rocks = np.count_nonzero(col[r:r2])
            col[r:r+rolling_rocks] = 2
            col[r+rolling_rocks:r2] = 0
            r = r2 + 1


def display(platform):
    rows, cols = platform.shape
    for r in range(rows):
        for c in range(cols):
            char = '.'
            if platform[r, c] == 1:
                char = '#'
            elif platform[r, c] == 2:
                char = 'O'
            print(char, end='')
        print()
    print()


def calc_load(platform):
    rows, cols = platform.shape
    load = 0
    for r in range(rows):
        row = platform[r]
        row_rolling_count = np.count_nonzero(row[row == 2])
        row_load_factor = rows - r
        load += row_rolling_count * row_load_factor
    return load


def main():
    _input_file = 'input'
    expected = {
        'input': (111979, 102055),
        'example': (None, None),
    }[_input_file]

    run(__file__, solve, _input_file, expected[0], cycles=0)
    run(__file__, solve, _input_file, expected[1], cycles=1000000000)

if __name__ == '__main__':
    main()
