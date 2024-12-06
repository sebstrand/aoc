import numpy as np

from aocl import *


start_marker = 'S'
target_marker = 'E'
neighbor_to_direction = {'n': 's', 's': 'n', 'w': 'e', 'e': 'w'}


def solve(input_file, p1=True):
    lines = read_lines(input_file)

    rows, cols = len(lines), len(lines[0])
    dtype = np.uint8
    heights = np.zeros((rows, cols), dtype=dtype)
    costs = {d: np.zeros((rows, cols), dtype=dtype) + np.inf for d in 'nswe'}

    start = None
    target = None
    possible_starts = []
    for r, line in enumerate(lines):
        for c, chr in enumerate(line):
            pos = r, c
            if chr == start_marker:
                start = pos
                continue
            if chr == target_marker:
                target = pos
                continue
            heights[pos] = to_height(chr)
            if chr == 'a':
                possible_starts.append(pos)

    possible_starts.append(start)
    heights[start] = to_height('a')
    heights[target] = to_height('z')

    for r, row in enumerate(heights):
        for c, col in enumerate(row):
            height = heights[(r, c)]
            for n, (n_pos, n_height) in neighbors_2d(heights, (r, c), named=True, valid_only=True).items():
                if n_height < height - 1:
                    cost = np.inf
                elif n_height > height:
                    cost = 1
                else:
                    cost = max(0, height - n_height) + 1
                direction = neighbor_to_direction[n]
                costs[direction][(r, c)] = cost

    if p1:
        _, path = dijkstra_grid(costs, start, target)
        return len(path_from_prev(path, start, target)) - 1
    else:
        path_lengths = []
        for start in possible_starts:
            _, prev = dijkstra_grid(costs, start, target)
            path = path_from_prev(prev, start, target)
            if len(path) > 0:
                path_lengths.append(len(path) - 1)
        return min(path_lengths)


def to_height(c):
    return ord(c) - ord('a') + 1


def main():
    _input_file = 'input'
    expected = {
        'input': (520, 508),
        'example': (31, 29),
    }[_input_file]

    run(__file__, solve, _input_file, expected[0], p1=True)
    run(__file__, solve, _input_file, expected[1], p1=False)


if __name__ == '__main__':
    main()
