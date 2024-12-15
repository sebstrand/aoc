import sys
import math

import numpy as np
from aocl import *


def solve(input_file, p1=True, steps=0):
    lines = read_lines(input_file)
    rows, cols = len(lines), len(lines[0])

    np.set_printoptions(sys.maxsize)

    garden = gridify(lines, '#.S'.index)
    start_pos = tuple(np.argwhere(garden == 2)[0])
    garden[start_pos] = 0

    if p1:
        locations = potentially_reachable(garden, start_pos, steps)
        locations, unreachable_locations = check_reachable(garden, locations, start_pos, steps)
        show(garden, locations, start_pos)
        # print('unreachable locations:', unreachable_locations)
        return len(locations)
    else:
        # example-small:
        # .......
        # .......
        # ...#...
        # .#.S.#.
        # ...#...
        # .......
        # .......
        # with 9 steps 84 reachable, expands to:
        # .......  .......  .......
        # .......  .......  .......
        # ...#...  ..O#O..  ...#...
        # .#...#.  .#.O.#.  .#...#.
        # ...#...  O.O#O.O  ...#...
        # ......O  .O.O.O.  O......
        # .....O.  O.O.O.O  .O.....
        #
        # ....O.O  .O.O.O.  O.O....
        # ...O.O.  O.O.O.O  .O.O...
        # ...#O.O  .O.#.O.  O.O#...
        # .#.O.#.  O#OSO#O  .#.O.#.
        # ...#O.O  .O.#.O.  O.O#...
        # ...O.O.  O.O.O.O  .O.O...
        # ....O.O  .O.O.O.  O.O....
        #
        # .....O.  O.O.O.O  .O.....
        # ......O  .O.O.O.  O......
        # ...#...  O.O#O.O  ...#...
        # .#...#.  .#.O.#.  .#...#.
        # ...#...  ..O#O..  ...#...
        # .......  .......  .......
        # .......  .......  .......

        steppable = (
            np.count_nonzero(garden[0::2, 0::2] == 1) + np.count_nonzero(garden[1::2, 1::2] == 1),
            np.count_nonzero(garden[0::2, 1::2] == 1) + np.count_nonzero(garden[1::2, 0::2] == 1),
        )
        print('steppable', steppable)

        reachable = 0
        remainder = steps % 2
        for tr, tc, range_v, range_h in partially_reachable_tiles(garden, steps, start_pos):
            # print('tr, tc', tr, tc, 'rv, rh', range_v, range_h)
            tile_reachable = 0
            continue
            for steps_r in range_v:
                for steps_c in range_h:
                    num_steps = abs(steps_r) + abs(steps_c)
                    if num_steps <= steps and num_steps % 2 == remainder:
                        loc_r = (start_pos[0] + steps_r) % rows
                        loc_c = (start_pos[1] + steps_c) % cols
                        # print('  loc_r, loc_c', loc_r, loc_c)
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
    print()
    assert gardens_v == gardens_h
    reach = gardens_v

    for tr in range(-reach, reach + 1):
        for tc in range(-reach, reach + 1):
            print('tr, tc', tr, tc, 'stn', steps_to_next)
            full_coverage = abs(tr) * rows + steps_to_next[0] - 1 + abs(tc) * cols + steps_to_next[1] - 1
            if steps < full_coverage:
                partial_coverage = max(0, abs(tr) - 1) * rows + steps_to_next[0] + max(0, abs(tc) - 1) * cols + steps_to_next[1]
                print('  partial:', steps >= partial_coverage, partial_coverage)
            else:
                print('  full:', full_coverage)

            if steps_to_next[0] + abs(tr) * rows <= steps and steps_to_next[1] + abs(tc) * cols <= steps:
                # Full coverage
                # continue
                pass
            yield tr, tc, None, None
    # for tr in range(-reach, reach + 1):
    #     for tc in range(-reach, reach + 1):
    #         if tr == 0:
    #             tv = (-steps_to_next[0]+1, steps_to_next[0])
    #         elif tr < 0:
    #             tv = (
    #                 tr * rows - steps_to_next[0] + 1,
    #                 (tr+1) * rows - steps_to_next[0] + 1,
    #             )
    #         else:
    #             tv = (
    #                 (tr-1) * rows + steps_to_next[0],
    #                 tr * rows + steps_to_next[0],
    #             )
    #
    #         if tc == 0:
    #             th = (-steps_to_next[1]+1, steps_to_next[1])
    #         elif tc < 0:
    #             th = (
    #                 tc * cols - steps_to_next[1] + 1,
    #                 (tc+1) * cols - steps_to_next[1] + 1,
    #             )
    #         else:
    #             th = (
    #                 (tc-1) * cols + steps_to_next[1],
    #                 tc * cols + steps_to_next[1],
    #             )
    #         inc_v = int(math.copysign(1, tv[1]-tv[0]))
    #         inc_h = int(math.copysign(1, th[1]-th[0]))
    #         yield tr, tc, range(tv[0], tv[1], inc_v), range(th[0], th[1], inc_h)


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
        if actual_steps > max_steps or actual_steps % 2 != max_steps % 2:
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
    _input_file = 'example-small'
    steps = {
        'input': (64, 26501365),
        'example': (6, 10),
        'example-small': (3, 5),
    }[_input_file]
    expected = {
        'input': (3795, None),
        'example': (16, 50),
        'example-small': (10, 84),
    }[_input_file]

    # run(__file__, solve, _input_file, expected[0], p1=True, steps=steps[0])
    run(__file__, solve, _input_file, expected[1], p1=False, steps=steps[1])


if __name__ == '__main__':
    main()
