import numpy as np
import heapq as hq
from aocl import *


def solve(input_file, p1=True):
    lines = read_lines(input_file)
    rows, cols = len(lines), len(lines[0])

    trails = np.zeros((rows, cols), dtype=np.byte)
    for r, line in enumerate(lines):
        trails[r] = [char_to_num(c) for c in line]
    print('Trails:\n', trails)

    start_pos = (0, 1)
    end_pos = (rows-1, cols-1)
    a_star(trails, start_pos, end_pos)


def char_to_num(c):
    if c == '#':
        return 1
    elif c == '^':
        return 2
    elif c == 'v':
        return 3
    elif c == '<':
        return 4
    elif c == '>':
        return 5
    return 0


def a_star(trails, start_pos, end_pos):
    distance = np.zeros(trails.shape, dtype=np.uint32) - 1
    distance[start_pos] = 0

    came_from = {}
    frontier = PriorityQueue()
    frontier.add(estimate_distance(start_pos, end_pos), start_pos)

    while len(frontier) > 0:
        current_pos = frontier.pop()
        if current_pos == end_pos:
            break

        for n_pos, n_value in neighbors_2d(trails, current_pos, valid_only=True):
            if n_value == 1:
                continue
            tentative_distance = distance[current_pos] + 1
            if tentative_distance < distance[n_pos]:
                came_from[n_pos] = current_pos
                distance[n_pos] = tentative_distance
                frontier.add(+(tentative_distance + estimate_distance(n_pos, end_pos)), n_pos)

        print('Distance:\n', distance.clip(0, 99))
    return distance[end_pos]


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


def estimate_distance(pos1, pos2):
    if pos1 == pos2:
        return 0
    return -(abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1]))


def main():
    _input_file = 'example'
    expected = {
        'input': (None, None),
        'example': (None, None),
    }[_input_file]

    run(__file__, solve, _input_file, expected[0], p1=True)
    # run(__file__, solve, _input_file, expected[1], p1=False)


if __name__ == '__main__':
    main()
