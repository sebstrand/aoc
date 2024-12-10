import string
import numpy as np
from aocl import *


def solve(input_file, p1=True):
    lines = read_lines(input_file)

    # Build height map
    heights = gridify(lines, int, valid=string.digits, default=-1, dtype=np.int8)
    rows, cols = heights.shape

    # Build cost maps
    costs = {
        'n': np.vstack([heights[:-1, :] - heights[1:, :], np.full((1, cols), np.inf)]),
        'w': np.hstack([heights[:, :-1] - heights[:, 1:], np.full((rows, 1), np.inf)]),
        's': np.vstack([np.full((1, cols), np.inf), heights[1:, :] - heights[:-1, :]]),
        'e': np.hstack([np.full((rows, 1), np.inf), heights[:, 1:] - heights[:, :-1]])
    }
    for d_costs in costs.values():
        # Only height diffs != 1 are usable
        d_costs[d_costs != 1] = -1

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
