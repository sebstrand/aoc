import sys
import heapq as hq
import itertools
import numpy as np
from aocl import *


def solve(input_file, p1=True):
    lines = read_lines(input_file)
    rows, cols = len(lines), len(lines[0])

    np.set_printoptions(threshold=sys.maxsize)
    city = np.zeros((rows, cols), dtype=np.byte)
    for r, line in enumerate(lines):
        city[r] = [int(c) for c in line]

    end_pos = (rows-1, cols-1)
    distance, reached_with_move = a_star2(city, (0, 0), end_pos)

    print('City:')
    draw_path2(city, {}, end_pos)
    print('Path:')
    draw_path2(city, reached_with_move, end_pos)
    # print('Path:\n', path)
    # print('Visited:\n', visited)
    # print('Distance:\n', distance.clip(0, 9999))

    if p1:
        return distance[end_pos]


def a_star2(city, start_pos, end_pos):
    distance = np.zeros(city.shape, dtype=np.uint32) - 1
    distance[start_pos] = 0

    reached_with_move = {}
    frontier = PriorityQueue()
    frontier.add(estimate_distance(city, start_pos, end_pos), start_pos)

    while len(frontier) > 0:
        current_pos = frontier.pop()
        if current_pos == end_pos:
            break

        for move, move_cost, target_pos in possible_moves(city, reached_with_move, current_pos):
            tentative_distance = distance[current_pos] + move_cost
            if tentative_distance < distance[target_pos]:
                # print('yes', move, target_pos, move_cost)
                reached_with_move[target_pos] = move, current_pos
                distance[target_pos] = tentative_distance
                frontier.add(tentative_distance + estimate_distance(city, target_pos, end_pos), target_pos)

    return distance, reached_with_move


def possible_moves(city, reached_with_move, current_pos):
    rows, cols = city.shape

    previous_moves = ''
    pos = current_pos
    while True:
        previous_move, pos = reached_with_move.get(pos, (None, None))
        if not pos:
            break
        previous_moves = previous_move + previous_moves
        if len(previous_moves) >= 4:
            break

    moves = (
        list(itertools.product('NSWE', repeat=3)) +
        list(itertools.product('NSWE', repeat=2)) +
        list('NSWE')
    )
    for move in moves:
        move = ''.join(move)
        combined = (previous_moves + move)
        if 'NNNN' in combined or 'SSSS' in combined or 'WWWW' in combined or 'EEEE' in combined:
            # invalid move (4 straight)
            continue
        elif 'NS' in combined or 'SN' in combined or 'EW' in combined or 'WE' in combined:
            # invalid move (immediate reverse)
            continue
        else:
            move_cost = 0
            r, c = current_pos
            for m in move:
                if m == 'N':
                    r -= 1
                elif m == 'S':
                    r += 1
                elif m == 'W':
                    c -= 1
                elif m == 'E':
                    c += 1
                if r < 0 or r >= rows or c < 0 or c >= cols:
                    move = None
                    break
                move_cost += city[r, c]
            if move:
                yield move, move_cost, (r, c)


def a_star(city, start_pos, end_pos):
    distance = np.zeros(city.shape, dtype=np.uint32) - 1
    distance[start_pos] = 0

    came_from = {}
    frontier = PriorityQueue()
    frontier.add(estimate_distance(city, start_pos, end_pos), start_pos)

    while len(frontier) > 0:
        current_pos = frontier.pop()
        if current_pos == end_pos:
            break
        for n_pos, heat_loss in neighbors_2d(city, current_pos, valid_only=True):
            p1 = came_from.get(current_pos)
            p2 = came_from.get(p1)
            p3 = came_from.get(p2)
            # if p1 and p2 and p3:
            #     if n_pos[0] == current_pos[0] == p1[0] == p2[0] == p3[0]:
            #         # n on same row
            #         continue
            #     elif n_pos[1] == current_pos[1] == p1[1] == p2[1] == p3[1]:
            #         # n in same col
            #         continue
            if n_pos == p1:
                print('=> block reverse ?', current_pos, n_pos)
                continue

            tentative_distance = distance[current_pos] + heat_loss
            if tentative_distance < distance[n_pos]:
                came_from[n_pos] = current_pos
                distance[n_pos] = tentative_distance
                frontier.add(tentative_distance + estimate_distance(city, n_pos, end_pos), n_pos)

    return distance, came_from


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


def estimate_distance(city, pos1, pos2):
    if pos1 == pos2:
        return 0
    # n = neighbors_2d(city, pos1)
    # south = n[1]
    # east = n[3]
    # if south and east:
    #     m = min((south[1], east[1]))
    # elif not east:
    #     m = south[1]
    # else:
    #     m = east[1]
    # return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1]) + m - 1
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


def draw_path(city, came_from, pos):
    path = set()
    while pos:
        path.add(pos)
        pos = came_from.get(pos)
    rows, cols = city.shape
    for r in range(rows):
        for c in range(cols):
            on_path = (r, c) in path and (r, c) != (0, 0)
            print((city[r, c], '.')[on_path], end='')
        print()


def draw_path2(city, reached_with_move, pos):
    path = {}
    while True:
        move, _ = reached_with_move.get(pos, (None, None))
        if not move:
            break

        r, c = pos
        for m in reversed(move):
            if m == 'N':
                path[(r, c)] = '^'
                r += 1
            elif m == 'S':
                path[(r, c)] = 'v'
                r -= 1
            elif m == 'W':
                path[(r, c)] = '<'
                c += 1
            elif m == 'E':
                path[(r, c)] = '>'
                c -= 1
        pos = (r, c)

    rows, cols = city.shape
    for r in range(rows):
        for c in range(cols):
            move = path.get((r, c))
            if move:
                print(path[(r, c)], end='')
            else:
                print(city[r, c], end='')
        print()


def main():
    _input_file = 'example'
    expected = {
        'input': (None, None),  # less than 692 for p1
        'example': (102, None),
    }[_input_file]

    run(__file__, solve, _input_file, expected[0], p1=True)
    # run(__file__, solve, _input_file, expected[1], p1=False)


if __name__ == '__main__':
    main()
