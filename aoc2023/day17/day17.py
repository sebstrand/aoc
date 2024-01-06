import itertools
import numpy as np
import sys

from aocl import *
from collections import defaultdict, deque


def solve(input_file, p1=True):
    lines = read_lines(input_file)
    rows, cols = len(lines), len(lines[0])

    np.set_printoptions(threshold=sys.maxsize, linewidth=1000)
    city = np.zeros((rows, cols), dtype=np.byte)
    for r, line in enumerate(lines):
        city[r] = [int(c) for c in line]

    start_pos = (0, 0)
    end_pos = (rows-1, cols-1)
    if p1:
        is_valid_move = is_valid_move_p1
        length_limit = 1
    else:
        is_valid_move = is_valid_move_p2
        length_limit = 4

    distances = dijkstra(city, start_pos, is_valid_move, length_limit)
    for move, distance in distances.items():
        if len(move) == length_limit:
            print(move, '\n', distance.clip(0, 999))
    distances_list = list(distances.values())
    d = distances_list[0]
    for x in distances_list[1:]:
        d = np.minimum(d, x)
    print('min dist:\n', d.clip(0, 999))

    heat_loss, path = construct_optimal_path_dfs(city, start_pos, end_pos, distances, is_valid_move)

    print('Path:')
    draw_path(city, path)
    return heat_loss


def path_to_moves(path):
    moves = []
    for i in range(len(path)-1):
        r1, c1 = path[i]
        r2, c2 = path[i+1]
        if r1 < r2:
            moves.append('S')
        elif r1 > r2:
            moves.append('N')
        elif c1 < c2:
            moves.append('E')
        elif c1 > c2:
            moves.append('W')
    return ''.join(moves)


def construct_optimal_path_dfs(city, start_pos, end_pos, distances, is_valid_move, min_solutions=999):
    rows, cols = city.shape

    q = deque()
    initial_path = deque()
    initial_path.append(end_pos)
    q.append((0 + city[end_pos], initial_path))

    max_path_len = 2 * (len(city) + len(city[0]))
    max_dist = 2**32 - 1
    best_heat_loss = 2**32 - 1

    found_paths = []
    i = 0
    while len(q) > 0:
        heat_loss, path = q.pop()
        path_moves = path_to_moves(path)
        # print('pos', path[0])

        if i % 1000 == 0 and False:
            print('qlen', len(q), 'plen', len(path), 'with heat loss', heat_loss, 'pos', path[0])
        i += 1
        # if i > 200:
        #     break

        next_hops = []
        for move, distance in distances.items():
            full_move = move + path_moves

            if is_valid_move(full_move, incomplete=False):
                pos = path[0]
                new_path = deque(path)
                new_heat_loss = heat_loss
                for direction in reversed(move):
                    pos = go_in_direction(pos, direction, reverse=True)
                    if not (0 <= pos[0] < rows and 0 <= pos[1] < cols):
                        pos = None
                        break
                    elif pos in new_path:
                        pos = None
                        break

                    new_path.appendleft(pos)
                    new_heat_loss += city[pos]

                if pos:
                    if new_heat_loss > best_heat_loss:
                        pass
                    elif pos == start_pos:
                        best_heat_loss = new_heat_loss
                        found_paths.append((new_heat_loss - city[start_pos], new_path))
                        print('found path', found_paths[-1])
                        # return found_paths[0]
                    elif len(new_path) >= max_path_len:
                        pass
                    elif city[pos] < max_dist and distance[path[0]] < max_dist:
                        # print('depth', len(new_path), new_heat_loss, abs(pos[0] - start_pos[0]) + abs(pos[1] - start_pos[1]))
                        # next_hops.append((distance[path[0]], new_heat_loss, new_path))
                        next_hops.append((distance[path[0]], len(next_hops), new_heat_loss, new_path))

        for hop in sorted(next_hops, reverse=True):
            # q.append(hop[1:])
            q.append(hop[2:])

        if len(found_paths) > min_solutions:
            break

    found_paths.sort()
    for path in found_paths:
        print('found path', path)
    return found_paths[0]


def construct_optimal_path_bfs(city, start_pos, end_pos, distances, is_valid_move):
    q = deque()
    initial_path = deque()
    initial_path.append(end_pos)
    q.append((end_pos, 0 + city[end_pos], initial_path))

    max_path_len = len(city) + len(city[0])
    max_dist = 2**32 - 1
    found_paths = []
    i = 0
    while len(q) > 0:
        if i > 0 and i % 5000 == 0:
            print('qlen', len(q))
        i += 1
        pos, heat_loss, path = q.popleft()
        # print('pp', pos, path)
        path_moves = path_to_moves(path)
        for move, distance in distances.items():
            full_move = move + path_moves
            if is_valid_move(full_move, incomplete=False):
                # print('  move', move)
                move_pos = pos
                new_path = deque(path)
                new_heat_loss = heat_loss
                for direction in reversed(move):
                    move_pos = go_in_direction(move_pos, direction, reverse=True)
                    if not (0 <= move_pos[0] < len(city) and 0 <= move_pos[1] < len(city[0])):
                        move_pos = None
                        break
                    elif move_pos in new_path:
                        move_pos = None
                        break

                    new_path.appendleft(move_pos)
                    new_heat_loss += city[move_pos]

                if move_pos:
                    if i > 0 and i % 5000 == 0:
                        print('nhl', new_heat_loss, '@pl', len(new_path))

                    if move_pos == start_pos:
                        found_paths.append((new_heat_loss - city[start_pos], new_path))
                    elif len(path) > max_path_len:
                        pass
                    elif new_heat_loss > 1000:
                        print('crucible too cold')
                        pass
                    elif city[move_pos] < max_dist:
                        q.append((move_pos, new_heat_loss, new_path))

    found_paths.sort()
    # for path in found_paths:
    #     print('found path', path)
    return found_paths[0]


def construct_optimal_path_old(city, start_pos, end_pos, distances, is_valid_move):
    pos = end_pos
    path = deque()
    path.append(pos)
    best_move = ''
    max_dist = 2**32 - 1
    while pos and pos != start_pos:
        print('pos', pos)
        min_dist = max_dist
        path_moves = path_to_moves(path)
        for move, distance in distances.items():
            combined = move + path_moves
            if is_valid_move(combined, incomplete=False) and distance[pos] < min_dist:
                min_dist = distance[pos]
                best_move = move
        if min_dist == max_dist:
            raise Exception('incomplete path')

        for direction in reversed(best_move):
            pos = go_in_direction(pos, direction, reverse=True)
            path.appendleft(pos)

    path = list(path)
    return sum(city[pos] for pos in path[1:]), path


def dijkstra(city, start_pos, is_valid_move, length_limit):
    distances = defaultdict(lambda: np.zeros(city.shape, dtype=np.uint32) - 1)
    distances['S'*length_limit][start_pos] = 0

    q = PriorityQueue()
    q.add(0, (start_pos, ''))
    while len(q) > 0:
        pos, pos_move = q.pop()
        for direction in 'NSWE':
            planned_move = pos_move + direction
            if not is_valid_move(planned_move):
                continue

            n_pos = go_in_direction(pos, direction)
            if n_pos == start_pos or not (0 <= n_pos[0] < len(city)) or not (0 <= n_pos[1] < len(city[0])):
                continue

            heat_loss = city[n_pos]
            limited_move = planned_move[-length_limit:]
            if pos_move in distances:
                distance_to_n = distances[pos_move][pos] + heat_loss
            else:
                distance_to_n = heat_loss

            if distance_to_n < distances[limited_move][n_pos]:
                distances[limited_move][n_pos] = distance_to_n
                q.add(distance_to_n, (n_pos, limited_move))

    return distances


def is_valid_move_p1(move, incomplete=True):
    if 'NNNN' in move or 'SSSS' in move or 'WWWW' in move or 'EEEE' in move:
        # invalid move: 4 straight
        return False
    elif 'NS' in move or 'SN' in move or 'EW' in move or 'WE' in move:
        # invalid move: immediate reverse
        return False
    return True


def is_valid_move_p2(move, incomplete=True):
    if len(move) == 1:
        return True
    elif 'NS' in move or 'SN' in move or 'EW' in move or 'WE' in move:
        return False
    elif len(move) >= 10 and ('N'*10 in move or 'S'*10 in move or 'W'*10 in move or 'E'*10 in move):
        return False

    if incomplete:
        if move[-1] == move[-2]:
            return True
        else:
            if len(move) < 5:
                return False
            preceding = move[-6:-2]
        return preceding == move[-2] * len(preceding)
    else:
        if len(move) < 5:
            return move == move[0] * len(move)
        else:
            groups = [len(list(g)) for _, g in itertools.groupby(move)]
            return min(groups) >= 4


def go_in_direction(pos, direction, reverse=False):
    r, c = pos
    sign = (1, -1)[reverse]

    if direction == 'N':
        r -= 1 * sign
    elif direction == 'S':
        r += 1 * sign
    elif direction == 'W':
        c -= 1 * sign
    elif direction == 'E':
        c += 1 * sign
    return r, c


def draw_path(city, path):
    path_set = set(path)
    rows, cols = city.shape
    for r in range(rows):
        for c in range(cols):
            if (r, c) in path_set:
                print(TermColors.CYAN, city[(r, c)], TermColors.ENDC, end='', sep='')
            else:
                print(city[r, c], end='')
        print()


def main():
    _input_file = 'example'
    expected = {
        'input': (686, None),  # 780 < p2 < 832,
        'example': (102, 94),
        'example2': (59, 71),
    }[_input_file]

    run(__file__, solve, _input_file, expected[0], p1=True)
    # run(__file__, solve, _input_file, expected[1], p1=False)


if __name__ == '__main__':
    main()
