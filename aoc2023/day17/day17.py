from aocl import *
import numpy as np
import sys


def solve(input_file, p1=True):
    lines = read_lines(input_file)
    rows, cols = len(lines), len(lines[0])

    np.set_printoptions(threshold=sys.maxsize)
    city = np.zeros((rows, cols), dtype=np.byte)
    for r, line in enumerate(lines):
        city[r] = [int(c) for c in line]

    distance = np.zeros(city.shape, dtype=np.uint32) - 1
    visited = np.zeros(city.shape, dtype=np.byte)

    pos = (0, 0)
    target_pos = (rows - 1, cols - 1)
    distance[pos] = 0

    previous = {}
    while pos:
        visited[pos] = True
        if pos == target_pos:
            break

        path_to_pos = [pos]
        prev_pos = previous.get(pos)
        if prev_pos:
            path_to_pos.append(prev_pos)

        unvisited_neighbors = [n for n in neighbors_2d(city, pos, valid_only=True) if not visited[n[0]]]

        for n_pos, heat_loss in unvisited_neighbors:
            if len(path_to_pos) == 2:
                rows_3 = [n_pos[0]] + [r for r, _ in path_to_pos]
                cols_3 = [n_pos[1]] + [c for _, c in path_to_pos]
                if min(rows_3) == max(rows_3) or min(cols_3) == max(cols_3):
                    print('blocking 4 straight')
                    continue
            n_dist = distance[pos] + heat_loss
            distance[n_pos] = min(distance[n_pos], n_dist)
            previous[n_pos] = pos

        next_pos = None
        unvisited = list(zip(*np.where(visited == 0)))
        for unvisited_pos in unvisited:
            if not next_pos or distance[unvisited_pos] < distance[next_pos]:
                next_pos = unvisited_pos

        pos = next_pos

    print('City:\n', city)
    print('Visited:\n', visited)
    print('Distances+1:\n', distance + 1)

    if p1:
        return distance[-1, -1]


def main():
    _input_file = 'example'
    expected = {
        'input': (None, None),
        'example': (102, None),
    }[_input_file]

    run(__file__, solve, _input_file, expected[0], p1=True)
    # run(__file__, solve, _input_file, expected[1], p1=False)


if __name__ == '__main__':
    main()
