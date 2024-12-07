from collections import defaultdict
from itertools import permutations

from aocl import *


def solve(input_file, p1=True):
    lines = read_lines(input_file)

    antennas = defaultdict(list)
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == '.': continue
            antennas[char].append(p2d(y, x))

    return len(find_antinodes(antennas, (len(lines), len(lines[0])), resonance=not p1))


def find_antinodes(antennas, bounds, resonance=False):
    antinodes = set()
    for frequency_locations in antennas.values():
        for loc1, loc2 in permutations(frequency_locations, 2):
            x_diff = loc2.x - loc1.x
            y_diff = loc2.y - loc1.y

            mult = start_mult = 0 if resonance else 1
            while resonance or mult == start_mult:
                an = p2d(loc2.y + mult * y_diff, loc2.x + mult * x_diff)
                if within_bounds(an, bounds):
                    antinodes.add(an)
                    mult += 1
                else:
                    break
    return antinodes


def within_bounds(loc, bounds):
    return 0 <= loc.y < bounds[0] and 0 <= loc.x < bounds[1]


def main():
    _input_file = 'input'
    expected = {
        'input': (357, 1266),
        'example': (14, 34),
    }[_input_file]

    run(__file__, solve, _input_file, expected[0], p1=True)
    run(__file__, solve, _input_file, expected[1], p1=False)


if __name__ == '__main__':
    main()
