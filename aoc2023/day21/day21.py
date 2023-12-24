import sys

import numpy as np
import heapq as hq
from aocl import *
from collections import deque


def solve(input_file, p1=True):
    lines = read_lines(input_file)
    rows, cols = len(lines), len(lines[0])

    np.set_printoptions(sys.maxsize)

    start_pos = None
    garden = np.zeros((rows, cols), dtype=np.byte)
    for r, line in enumerate(lines):
        if 'S' in line:
            start_pos = (r, line.index('S'))
            line = line.replace('S', '.')
        garden[r] = [(1, 0)[c == '#'] for c in line]

    locations = no_step(garden, start_pos, 64)
    bad_locations = set()
    for location in locations:
        # print('A*', location)
        steps = a_star(garden, start_pos, location)
        if steps > 64:
            # print('bad location', location, 'steps', steps, 'manhattan', manhattan(start_pos, location))
            bad_locations.add(location)

    locations = locations.difference(bad_locations)

    print('Locations:')
    for r, row in enumerate(garden):
        for c, col in enumerate(row):
            if (r, c) == start_pos:
                print('S', end='')
            elif (r, c) in locations:
                print('O', end='')
            elif garden[r, c] > 0:
                print('.', end='')
            else:
                print('#', end='')
        print()
    return len(locations)


def no_step(garden, start_pos, max_steps):
    seen = {start_pos}
    rows, cols = garden.shape
    for r in range(rows):
        for c in range(cols):
            if garden[r, c] == 1:
                m = manhattan((r, c), start_pos)
                if m <= max_steps and m % 2 == 0:
                    seen.add((r, c))
    return seen


def a_star(garden, start_pos, end_pos):
    distance = np.zeros(garden.shape, dtype=np.uint32) - 1
    distance[start_pos] = 0

    came_from = {}
    frontier = PriorityQueue()
    frontier.add(manhattan(start_pos, end_pos), start_pos)

    while len(frontier) > 0:
        current_pos = frontier.pop()
        if current_pos == end_pos:
            break

        for n_pos, n_value in neighbors_2d(garden, current_pos, valid_only=True):
            if n_value == 0:
                continue
            tentative_distance = distance[current_pos] + 1
            if tentative_distance < distance[n_pos]:
                came_from[n_pos] = current_pos
                distance[n_pos] = tentative_distance
                frontier.add(tentative_distance + manhattan(n_pos, end_pos), n_pos)

    return distance[end_pos]


def estimate_distance(pos1, pos2):
    return manhattan(pos1, pos2)


def manhattan(pos1, pos2):
    if pos1 == pos2:
        return 0
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


class PriorityQueue:
    def __init__(self):
        self.entries = {}
        self.pq = []

    def __len__(self):
        return len(self.entries)

    def add(self, priority, item):
        if item in self.entries:
            entry = self.entries.pop(item)
            entry[-1] = ()
        entry = [priority, item]
        self.entries[item] = entry
        hq.heappush(self.pq, entry)

    def pop(self):
        while self.pq:
            priority, item = hq.heappop(self.pq)
            if item:
                del self.entries[item]
                return item
        raise KeyError('priority queue is empty')


def main():
    _input_file = 'input'
    expected = {
        'input': (3795, None),
        'example': (None, None),
    }[_input_file]

    run(__file__, solve, _input_file, expected[0], p1=True)
    # run(__file__, solve, _input_file, expected[1], p1=False)


if __name__ == '__main__':
    main()
