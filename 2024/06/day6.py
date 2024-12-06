import numpy as np
from aocl import *


direction_to_steps = {
    1: (-1, +0),
    2: (+0, +1),
    3: (+1, +0),
    4: (+0, -1),
}


VISITED = 9


def solve(input_file, p1=True):
    lines = read_lines(input_file)

    area = np.zeros((len(lines), len(lines[0])), dtype=np.uint8)
    guard_pos = None
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if char == '^':
                guard_pos = row, col
            elif char == '#':
                area[row, col] = 1

    visited_locations, is_loop = patrol(area, guard_pos)
    assert not is_loop

    if p1:
        return np.count_nonzero(visited_locations == VISITED)
    else:
        # Count positions in the guard path where an obstacle causes a loop
        count = 0
        for row, col in zip(*np.nonzero(visited_locations == VISITED)):
            if (row, col) == guard_pos: continue
            area[row, col] = 1
            if patrol(area, guard_pos)[1]:
                count += 1
            area[row, col] = 0
        return count


def patrol(area, starting_pos):
    direction = 1
    is_loop = False
    visited_locations = np.zeros(area.shape, dtype=np.uint8)
    row, col = starting_pos
    while True:
        r_step, c_step = direction_to_steps[direction]
        if r_step != 0:
            slices = np.s_[row::r_step, col]
        else:
            slices = np.s_[row, col::c_step]

        obstacles = np.nonzero(area[slices])[0]
        if len(obstacles) == 0:
            # Guard left area
            visited_locations[slices] = VISITED
            break

        obstacle_row = row + r_step * obstacles[0]
        obstacle_col = col + c_step * obstacles[0]
        if visited_locations[obstacle_row, obstacle_col] == direction:
            is_loop = True
            break

        visited_locations[obstacle_row, obstacle_col] = direction
        turning_point = obstacle_row - r_step, obstacle_col - c_step
        visited_locations[slices][:obstacles[0]] = VISITED
        row, col = turning_point
        direction = rotate_right(direction)

    return visited_locations, is_loop


def rotate_right(direction):
    return 1 if direction == 4 else direction + 1


def main():
    _input_file = 'input'
    expected = {
        'input': (4778, 1618),
        'example': (41, 6),
    }[_input_file]

    run(__file__, solve, _input_file, expected[0], p1=True)
    run(__file__, solve, _input_file, expected[1], p1=False)


if __name__ == '__main__':
    main()
