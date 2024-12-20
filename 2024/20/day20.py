from collections import defaultdict
from aocl import *


def solve(input_file, cheat_target, cheat_max_duration):
    lines = read_lines(input_file)

    racetrack = {}
    start_pos = end_pos = None
    for y, line in enumerate(lines):
        if 'S' in line:
            start_pos = (y, line.index('S'))
            line = line.replace('S', '.')
        if 'E' in line:
            end_pos = (y, line.index('E'))
            line = line.replace('E', '.')
        racetrack.update({(y, x): True for x, char in enumerate(line) if char == '.'})

    # Find no-cheat path with Dijkstra
    _, prev = dijkstra(racetrack, start_pos, end_pos)
    normal_path = list(path_from_prev(prev, start_pos, end_pos))

    time_saved = defaultdict(int)
    positions = {p: i for i, p in enumerate(normal_path)}

    # For each position in no-cheat path, find how much time would be saved by taking a shortcut to
    # all reachable positions further along on the path
    for i, cheat_start in enumerate(normal_path):
        for cheat_end in positions_in_range(cheat_start, cheat_max_duration, positions):
            cheat_length = manhattan(cheat_start, cheat_end)
            if cheat_length > cheat_max_duration: continue

            savings = positions[cheat_end] - i - cheat_length
            time_saved[savings] += 1

    return sum({k: v for k, v in time_saved.items() if k >= cheat_target}.values())


def positions_in_range(p1, distance, positions):
    for y in range(p1[0] - distance, p1[0] + distance + 1):
        distance_available = distance - abs(p1[0] - y)
        for x in range(p1[1] - distance_available, p1[1] + distance_available + 1):
            p2 = (y, x)
            if p2 in positions and manhattan(p1, p2) <= distance:
                yield p2


def dijkstra(grid, start_pos, end_pos):
    costs = {start_pos: 0}
    prev = {}

    q = PriorityQueue()
    q.add(0, start_pos)
    while len(q) > 0:
        pos = q.pop()
        if pos == end_pos:
            break

        for d in 'nswe':
            n_pos = move(pos, d)
            if not grid.get(n_pos, False):
                continue

            cost_to_n = costs[pos] + 1

            old_cost = costs.get(n_pos, 2 ** 64)
            if cost_to_n < old_cost:
                costs[n_pos] = cost_to_n
                prev[n_pos] = pos
                q.add(cost_to_n, n_pos)

    return costs, prev


def move(pos, direction, distance=1):
    match direction:
        case 'n':
            return pos[0] - distance, pos[1]
        case 's':
            return pos[0] + distance, pos[1]
        case 'w':
            return pos[0], pos[1] - distance
        case 'e':
            return pos[0], pos[1] + distance


def main():
    _input_file = 'input'
    expected = {
        'input': (1323, 983905),
        'example': (10, 285),
    }[_input_file]
    cheat_target = {
        'input': (100, 100),
        'example': (10, 50),
    }[_input_file]

    run(__file__, solve, _input_file, expected[0], cheat_target=cheat_target[0], cheat_max_duration=2)
    run(__file__, solve, _input_file, expected[1], cheat_target=cheat_target[1], cheat_max_duration=20)


if __name__ == '__main__':
    main()
