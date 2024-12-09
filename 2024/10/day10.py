import string
import numpy as np
from aocl import *


inverse_direction = {'n': 's', 's': 'n', 'w': 'e', 'e': 'w'}


def solve(input_file, p1=True):
    lines = read_lines(input_file)

    rows, cols = len(lines), len(lines[0])
    dtype = np.int8

    # Build height map
    heights = np.zeros((rows, cols), dtype=dtype)
    for r, line in enumerate(lines):
        for c, char in enumerate(line):
            if char not in string.digits: continue
            heights[(r, c)] = int(char)

    # Build cost maps
    costs = {d: np.zeros((rows, cols), dtype=dtype) + np.inf for d in 'nswe'}
    for r, row in enumerate(heights):
        for c, col in enumerate(row):
            height = heights[(r, c)]
            for n, (n_pos, n_height) in neighbors_2d(heights, (r, c), named=True, valid_only=True).items():
                if n_height == height - 1:
                    cost = 1
                else:
                    cost = np.inf
                direction = inverse_direction[n]
                costs[direction][(r, c)] = cost

    result = 0
    for trailhead in zip(*np.where(heights == 0)):
        distances, _ = dijkstra_grid(costs, trailhead)
        if p1:
            reachable_peaks = np.count_nonzero(distances == 9)
            result += reachable_peaks
        else:
            # Rating is number of unique trails from trailhead to any peak
            result += rating(distances, trailhead)
    return result


def rating(distances, start):
    start_distance = distances[start]
    if start_distance == 9:
        return 1

    neighbors = neighbors_2d(distances, start, valid_only=True)
    return sum(
        rating(distances, n_pos)
        for n_pos, n_dist in neighbors
        if n_dist == start_distance + 1)


def main():
    _input_file = 'input'
    expected = {
        'input': (496, 1120),
        'example': (36, 81),
        'example2': (2, 227),
    }[_input_file]

    run(__file__, solve, _input_file, expected[0], p1=True)
    run(__file__, solve, _input_file, expected[1], p1=False)


if __name__ == '__main__':
    main()
