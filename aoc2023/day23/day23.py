import numpy as np
from aocl import *
from collections import deque


def solve(input_file, p1=True):
    lines = read_lines(input_file)
    rows, cols = len(lines), len(lines[0])

    trails = np.zeros((rows, cols), dtype=np.byte)
    for r, line in enumerate(lines):
        trails[r] = [char_to_num(c, p1) for c in line]

    # print(np.count_nonzero(trails!=1))

    start_pos = (0, 1)
    end_pos = (rows-1, cols-2)
    if p1:
        return a_star(trails, start_pos, end_pos)
    else:
        return bfs(trails, start_pos, end_pos)


def bfs(trails, start_pos, end_pos):
    p = Path(start_pos)
    q = deque([p])
    valid_paths = []
    max_path = 0
    rows, cols = trails.shape
    v_line = set((r, cols//2) for r in range(rows) if trails[r, cols//2] != 1)
    h_line = set((rows//2, c) for c in range(cols) if trails[rows//2, c] != 1)
    while len(q) > 0:
        path = q.popleft()
        for n_pos, n_value in neighbors_2d(trails, path.last_pos, valid_only=True):
            if n_value != 1 and not n_pos in path.positions:
                new_path = path.extend(n_pos)
                path_len = len(path.positions)
                if path_len > max_path:
                    max_path = path_len
                    # print('path len', len(new_path.positions), 'q', len(q))
                if n_pos == end_pos:
                    # print('valid path found')
                    valid_paths.append(new_path)
                elif n_pos[0] < rows//2 - 1 and new_path.positions.issuperset(h_line):
                    # print('no paths to goal possible, discarding')
                    pass
                elif n_pos[1] < cols//2 - 1 and new_path.positions.issuperset(v_line):
                    # print('no paths to goal possible, discarding')
                    pass
                else:
                    q.append(new_path)
    return max(len(p) - 1 for p in valid_paths)


class Path:
    def __init__(self, initial_pos) -> None:
        self.positions = set()
        self.add(initial_pos)
    
    def extend(self, next_pos):
        path = Path(next_pos)
        path.positions.update(self.positions)
        return path

    def add(self, pos):
        self.last_pos = pos
        self.positions.add(pos)

    def __len__(self):
        return len(self.positions)


def char_to_num(c, slippery):
    if c == '#':
        return 1
    elif c == '^':
        return (0, 2)[slippery]
    elif c == 'v':
        return (0, 3)[slippery]
    elif c == '<':
        return (0, 4)[slippery]
    elif c == '>':
        return (0, 5)[slippery]
    return 0


def a_star(trails, start_pos, end_pos):
    distance = np.zeros(trails.shape, dtype=np.float32)
    distance.fill(np.inf)
    distance[start_pos] = 0

    came_from = {}
    frontier = PriorityQueue()
    frontier.add(estimate_distance(start_pos, end_pos), start_pos)

    while len(frontier) > 0:
        current_pos = frontier.pop()

        for n_pos, n_value in neighbors_2d(trails, current_pos, valid_only=True):
            n_dist = 1
            slope_pos = None
            if n_value == 1 or n_pos == current_pos:
                continue
            elif is_on_path(came_from, current_pos, n_pos):
                continue
            elif n_value > 1:
                r, c = n_pos
                slope_pos = n_pos
                if n_value == 2:
                    n_pos = (r-1, c)
                elif n_value == 3:
                    n_pos = (r+1, c)
                elif n_value == 4:
                    n_pos = (r, c-1)
                elif n_value == 5:
                    n_pos = (r, c+1)
                else:
                    assert False
                if n_pos == current_pos:
                    # uphill slope
                    continue
                else:
                    n_dist = 2

            tentative_distance = distance[current_pos] - n_dist
            if tentative_distance < distance[n_pos]:
                distance[n_pos] = tentative_distance
                if slope_pos:
                    distance[slope_pos] = tentative_distance + 1
                    came_from[slope_pos] = current_pos
                    came_from[n_pos] = slope_pos
                else:
                    came_from[n_pos] = current_pos
                frontier.add(-(tentative_distance + estimate_distance(n_pos, end_pos)), n_pos)

        # print('Distance:\n', np.abs(distance))
    return abs(distance[end_pos])


def is_on_path(came_from, current_pos, test_pos):
    pos = current_pos
    seen = set()
    while True:
        pos = came_from.get(pos)
        if not pos:
            break
        elif pos in seen:
            print('error: cycle', pos, seen)
            assert False
        if pos == test_pos:
            return True
        seen.add(pos)
    return False


def estimate_distance(pos1, pos2):
    if pos1 == pos2:
        return 0
    # return -(abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1]))
    return -99999


def main():
    _input_file = 'input'
    expected = {
        'input': (2166, None), # p2 > 3600, theoretical max 9411 (9412 steppable tiles)
        'example': (94, 154),
    }[_input_file]

    run(__file__, solve, _input_file, expected[0], p1=True)
    # run(__file__, solve, _input_file, expected[1], p1=False)


if __name__ == '__main__':
    main()
