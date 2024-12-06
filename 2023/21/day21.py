import sys
import math

import numpy as np
from aocl import *


def solve(input_file, p1=True, steps=0):
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

    # show(garden, locations, start_pos)

    if p1:
        locations = potentially_reachable(garden, start_pos, steps)
        locations, unreachable_locations = check_reachable(garden, locations, start_pos, steps)
        return len(locations)
    else:
        steppable = (
            np.count_nonzero(garden[0::2, 0::2] == 1) + np.count_nonzero(garden[1::2, 1::2] == 1),
            np.count_nonzero(garden[0::2, 1::2] == 1) + np.count_nonzero(garden[1::2, 0::2] == 1),
        )
        print('steppable', steppable)

        reachable = 0
        remainder = steps % 2
        for tr, tc, range_v, range_h in partially_reachable_tiles(garden, steps, start_pos):
            print('tr, tc', tr, tc)
            tile_reachable = 0
            for steps_r in range_v:
                for steps_c in range_h:
                    num_steps = abs(steps_r)+abs(steps_c)
                    if num_steps <= steps and num_steps % 2 == remainder:
                        loc_r = (start_pos[0] + steps_r) % rows
                        loc_c = (start_pos[1] + steps_c) % cols
                        if garden[loc_r, loc_c] == 1:
                            # print('  steps', steps_r, steps_c, num_steps, num_steps % 2)
                            tile_reachable += 1
            # print('  tile reachable:', tile_reachable)
            reachable += tile_reachable

        # # Entire tile reachable
        # # print('fully reachable', gr, gc)
        # row_rem = abs(start_pos[0]%2 - gr%2)
        # col_rem = abs(start_pos[1]%2 - gc%2)
        # if row_rem == col_rem:
        #     tile_reachable = steppable[0]
        # else:
        #     tile_reachable = steppable[1]
        # # print('  tile reachable:', tile_reachable)
        # reachable += tile_reachable

        return reachable


def partially_reachable_tiles(garden, steps, start_pos):
    rows, cols = garden.shape

    steps_to_next = (rows-start_pos[0], cols-start_pos[1])
    gardens_v = max(0, math.ceil((steps - steps_to_next[0] + 1) / rows))
    gardens_h = max(0, math.ceil((steps - steps_to_next[1] + 1) / cols))
    print('gv, gh', gardens_v, gardens_h)
    assert gardens_v == gardens_h
    reach = gardens_v

    for tr in range(-reach, reach + 1):
        remain = reach - abs(tr)
        if remain == 0:
            remain_set = (remain,)
        else:
            remain_set = (-remain, remain)

        for tc in remain_set:
            if tr == 0:
                tv = (-steps_to_next[0]+1, steps_to_next[0])
            elif tr < 0:
                tv = (
                    tr * rows - steps_to_next[0] + 1,
                    (tr+1) * rows - steps_to_next[0] + 1,
                )
            else:
                tv = (
                    (tr-1) * rows + steps_to_next[0],
                    tr * rows + steps_to_next[0],
                )

            if tc == 0:
                th = (-steps_to_next[1]+1, steps_to_next[1])
            elif tc < 0:
                th = (
                    tc * cols - steps_to_next[1] + 1,
                    (tc+1) * cols - steps_to_next[1] + 1,
                )
            else:
                th = (
                    (tc-1) * cols + steps_to_next[1],
                    tc * cols + steps_to_next[1],
                )
            inc_v = int(math.copysign(1, tv[1]-tv[0]))
            inc_h = int(math.copysign(1, th[1]-th[0]))
            yield tr, tc, range(tv[0], tv[1], inc_v), range(th[0], th[1], inc_h)


def show(garden, locations, start_pos):
    rows, cols = garden.shape
    print('Locations:')
    for r in range(rows):
        for c in range(cols):
            if (r, c) == start_pos:
                print('S', end='')
            elif (r, c) in locations:
                print('O', end='')
            elif garden[r, c] > 0:
                print('.', end='')
            else:
                print('#', end='')
        print()


def potentially_reachable(garden, start_pos, max_steps):
    remainder = max_steps % 2
    seen = {start_pos}
    rows, cols = garden.shape
    for r in range(rows):
        for c in range(cols):
            if garden[r, c] == 1:
                m = manhattan((r, c), start_pos)
                if m <= max_steps and m % 2 == remainder:
                    seen.add((r, c))
    return seen


def check_reachable(garden, potentially_reachable, start_pos, max_steps):
    not_reachable = set()
    for location in potentially_reachable:
        actual_steps = a_star(garden, start_pos, location)
        if actual_steps > max_steps:
            not_reachable.add(location)
    return potentially_reachable.difference(not_reachable), not_reachable


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


def manhattan(pos1, pos2):
    if pos1 == pos2:
        return 0
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


def main():
    _input_file = 'input'
    steps = {
        'input': (64, 26501365),
        'example': (6, 10),
    }[_input_file]
    expected = {
        'input': (3795, None),
        'example': (16, 50),
    }[_input_file]

    run(__file__, solve, _input_file, expected[0], p1=True, steps=steps[0])
    # run(__file__, solve, _input_file, expected[1], p1=False, steps=steps[1])


if __name__ == '__main__':
    main()
