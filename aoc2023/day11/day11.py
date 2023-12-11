from aocl import *
import numpy as np


galaxy = 0
# expansion = 2  # p1
expansion = 1000000


def main():
    lines = read_lines('input')
    rows, cols = len(lines), len(lines[0])

    space = np.zeros((rows, cols), dtype=np.byte)

    for r, line in enumerate(lines):
        space[r] = tuple((0, 1)[c != '.'] for c in line)

    expanded_rows = []
    for r in range(rows):
        if not space[r].any():
            expanded_rows.append(r)

    expanded_cols = []
    for c in range(cols):
        if not space[:, c].any():
            expanded_cols.append(c)

    print('expanded space:\n', expanded_rows, expanded_cols)
    print()

    locations = []
    for r in range(rows):
        for c in range(cols):
            if space[r, c]:
                ra = adjust(r, expanded_rows)
                ca = adjust(c, expanded_cols)
                locations.append((ra, ca))

    distances = []
    for i in range(len(locations)):
        for j in range(i + 1, len(locations)):
            distances.append(calc_distance(locations[i], locations[j]))

    distance_sum = sum(distances)
    print('distance sum:', distance_sum)

    if expansion == 2:
        assert distance_sum == 9563821
    else:
        assert distance_sum == 827009909817


def calc_distance(p1, p2):
    r1, c1 = p1
    r2, c2 = p2
    return abs(r2 - r1) + abs(c2 - c1)


def adjust(value, expansions):
    return value + (expansion-1) * len(tuple(x for x in expansions if x < value))


if __name__ == '__main__':
    main()
