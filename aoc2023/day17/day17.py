import itertools
import numpy as np
import sys

from aocl import *
from collections import defaultdict, deque


def solve(input_file, p1=True):
    lines = read_lines(input_file)
    rows, cols = len(lines), len(lines[0])

    np.set_printoptions(threshold=sys.maxsize)
    city = np.zeros((rows, cols), dtype=np.byte)
    for r, line in enumerate(lines):
        city[r] = [int(c) for c in line]

    end_pos = (rows-1, cols-1)
    # distance, reached_with_move = a_star(city, (0, 0), end_pos)
    heat_loss, path = dijkstra(city, (0, 0), end_pos)
    # for move, distance in distances.items():
    #     print('move', move, '\n', distance.clip(0, 999))

    # print('City:')
    # draw_path(city, {}, end_pos)
    # print('Path:')
    # draw_path(city, path)
    # draw_path(city, reached_with_move, end_pos)
    # print('moves', moves)
    # print('Path:\n', path)
    # print('Visited:\n', visited)
    # print('Distance:\n', distance.clip(0, 9999))

    if p1:
        return heat_loss


def find_first_illegal_move(moves):
    for i in range(len(moves)):
        last4 = moves[i-4:i]
        if 'NNNN' in last4 or 'SSSS' in last4 or 'WWWW' in last4 or 'EEEE' in last4:
            # invalid move (4 straight)
            return i
        elif 'NS' in last4 or 'SN' in last4 or 'EW' in last4 or 'WE' in last4:
            # invalid move (immediate reverse)
            return i
    return -1


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


def dijkstra(city, start_pos, end_pos):
    moves = (
            [''.join(m) for m in itertools.product('NSWE', repeat=3)]
            + [''.join(m) for m in itertools.product('NSWE', repeat=2)]
            + ['N', 'S', 'W', 'E']
    )
    valid_moves = [
        m for m
        in moves
        if 'NS' not in m and 'SN' not in m and 'WE' not in m and 'EW' not in m
    ]

    distances = {}
    for move in valid_moves:
        distances[move] = np.zeros(city.shape, dtype=np.uint32) - 1
    max_dist = distances['NNN'][0, 0]

    q = PriorityQueue()
    q.add(0, (start_pos, ''))
    while len(q) > 0:
        pos, pos_move = q.pop()
        for direction in 'NSWE':
            move4 = (pos_move + direction)[-4:]
            if not is_valid_move(move4):
                continue

            n_pos = go_in_direction(pos, direction)
            if not (0 <= n_pos[0] < len(city)) or not (0 <= n_pos[1] < len(city[0])):
                continue

            heat_loss = city[n_pos]
            move3 = move4[-3:]
            if pos_move in distances:
                distance_to_n = distances[pos_move][pos] + heat_loss
            else:
                distance_to_n = heat_loss

            if distance_to_n < distances[move3][n_pos]:
                distances[move3][n_pos] = distance_to_n
                q.add(distance_to_n, (n_pos, move3))

    pos = end_pos
    path = deque()
    path.append(pos)
    best_move = ''
    while pos and pos != start_pos:
        move_after = best_move
        min_dist = max_dist
        for move, distance in distances.items():
            if is_valid_move(move + move_after) and distance[pos] < min_dist:
                min_dist = distance[pos]
                best_move = move
        if min_dist == max_dist:
            raise 'path broken'

        for direction in reversed(best_move):
            pos = go_in_direction(pos, direction, reverse=True)
            path.appendleft(pos)

    path = list(path)
    return sum(city[pos] for pos in path[1:]), path


def is_valid_move(move):
    if 'NNNN' in move or 'SSSS' in move or 'WWWW' in move or 'EEEE' in move:
        # invalid move: 4 straight
        return False
    elif 'NS' in move or 'SN' in move or 'EW' in move or 'WE' in move:
        # invalid move: immediate reverse
        return False
    return True


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


def possible_moves_d(city, previous, current_pos, allow_illegal=False):
    rows, cols = city.shape

    previous_moves = deque()
    pos = current_pos
    pos_after = None
    while pos and len(previous_moves) < 4:
        if pos_after:
            r1, c1 = pos
            r2, c2 = pos_after
            if r1 < r2:
                previous_moves.append('S')
            elif r1 > r2:
                previous_moves.append('N')
            elif c1 < c2:
                previous_moves.append('E')
            elif c1 > c2:
                previous_moves.append('W')

        pos_after = pos
        pos = previous.get(pos)

    previous_moves = ''.join(previous_moves)
    print('  previous moves', previous_moves)

    moves = (
        list(itertools.product('NSWE', repeat=3))
        # list(itertools.product('NSWE', repeat=2)) +
        # list('NSWE')
    )
    for move in moves:
        move = ''.join(move)
        combined = (previous_moves + move)
        if not allow_illegal and ('NNNN' in combined or 'SSSS' in combined or 'WWWW' in combined or 'EEEE' in combined):
            # invalid move (4 straight)
            continue
        elif not allow_illegal and ('NS' in combined or 'SN' in combined or 'EW' in combined or 'WE' in combined):
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
                yield (r, c), move_cost


def a_star(city, start_pos, end_pos):
    distance = np.zeros(city.shape, dtype=np.uint32) - 1
    distance[start_pos] = 0

    reached_with_move = defaultdict(list)
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
                reached_with_move[target_pos].append((move, current_pos))
                distance[target_pos] = tentative_distance
                frontier.add(tentative_distance + estimate_distance(city, target_pos, end_pos), target_pos)
            elif tentative_distance == distance[target_pos]:
                reached_with_move[target_pos].append((move, current_pos))

    return distance, reached_with_move


def possible_moves(city, reached_with_move, current_pos, allow_illegal=False):
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
        # list(itertools.product('NSWE', repeat=3)) +
        # list(itertools.product('NSWE', repeat=2)) +
        list('NSWE')
    )
    for move in moves:
        move = ''.join(move)
        combined = (previous_moves + move)
        if not allow_illegal and ('NNNN' in combined or 'SSSS' in combined or 'WWWW' in combined or 'EEEE' in combined):
            # invalid move (4 straight)
            continue
        elif not allow_illegal and ('NS' in combined or 'SN' in combined or 'EW' in combined or 'WE' in combined):
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


def draw_path_astar(city, reached_with_move, pos):
    path = {}
    prev = None
    lc = ' '
    while True:
        move, _ = reached_with_move.get(pos, (None, None))
        if not move:
            break

        r, c = pos
        for m in reversed(move):
            cur_c, cur_r = c, r
            if m == 'N':
                if prev == 'E':
                    lc = '┌'
                elif prev == 'W':
                    lc = '┐'
                else:
                    lc = '│'
                r += 1
            elif m == 'S':
                if prev == 'E':
                    lc = '└'
                elif prev == 'W':
                    lc = '┘'
                else:
                    lc = '│'
                r -= 1
            elif m == 'W':
                if prev == 'N':
                    lc = '└'
                elif prev == 'S':
                    lc = '┌'
                else:
                    lc = '─'
                c += 1
            elif m == 'E':
                if prev == 'N':
                    lc = '┘'
                elif prev == 'S':
                    lc = '┐'
                else:
                    lc = '─'
                c -= 1
            if prev is not None:
                path[(cur_r, cur_c)] = lc

            prev = m
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
    _input_file = 'input'
    expected = {
        'input': (686, None),  # less than 692 for p1, A* gives 569 with no move restrictions (too low)
        'example': (102, None),
    }[_input_file]

    run(__file__, solve, _input_file, expected[0], p1=True)
    # run(__file__, solve, _input_file, expected[1], p1=False)


if __name__ == '__main__':
    main()
