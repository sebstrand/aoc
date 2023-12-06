from aocl import *
from collections import namedtuple


Pos = namedtuple('pos', ['x', 'y'])
rope_length = 10


def main():
    lines = read_lines('input')

    start_pos = Pos(0, 0)
    knot_positions = [start_pos] * rope_length

    visited = set()
    visited.add(start_pos)

    # print('start')
    # visualize(knot_positions)

    for line in lines:
        direction, count = splits(line)
        count = int(count)
        # print('move', direction, count)

        for _ in range(count):
            for i, knot_pos in enumerate(knot_positions):
                if i == 0:
                    knot_pos = move(knot_pos, direction)
                else:
                    x_diff = leader_pos.x - knot_pos.x
                    y_diff = leader_pos.y - knot_pos.y

                    if x_diff >= 2:
                        knot_pos = move(knot_pos, 'R')
                        if abs(y_diff) == 1:
                            knot_pos = Pos(knot_pos.x, leader_pos.y)
                    elif x_diff <= -2:
                        knot_pos = move(knot_pos, 'L')
                        if abs(y_diff) == 1:
                            knot_pos = Pos(knot_pos.x, leader_pos.y)

                    if y_diff >= 2:
                        knot_pos = move(knot_pos, 'D')
                        if abs(x_diff) == 1:
                            knot_pos = Pos(leader_pos.x, knot_pos.y)
                    elif y_diff <= -2:
                        knot_pos = move(knot_pos, 'U')
                        if abs(x_diff) == 1:
                            knot_pos = Pos(leader_pos.x, knot_pos.y)
                knot_positions[i] = knot_pos
                leader_pos = knot_pos
            visited.add(knot_positions[-1])
        # visualize(knot_positions)

    # print('visited', visited)
    visited_count = len(visited)
    print('visited location count:', visited_count)
    if rope_length == 2:
        assert visited_count == 6243
    else:
        assert visited_count == 2630


def move(pos, direction=None):
    if direction == 'U':
        return Pos(pos.x, pos.y-1)
    elif direction == 'D':
        return Pos(pos.x, pos.y+1)
    elif direction == 'L':
        return Pos(pos.x-1, pos.y)
    elif direction == 'R':
        return Pos(pos.x+1, pos.y)


def visualize(knot_positions):
    for y in range(-17, 8):
        for x in range(-13, 17):
            found = False
            for i, p in enumerate(knot_positions):
                if p.x == x and p.y == y:
                    found = True
                    if i == 0:
                        print('H', end='')
                    else:
                        print(str(i), end='')
                    break
            if not found:
                print('.', end='')
        print()
    print()


if __name__ == '__main__':
    main()
