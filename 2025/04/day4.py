from aocl import *
import numpy as np


def solve(input_file, p1=True):
    grid = gridify(read_lines(input_file), lambda x: 1 if x == '@' else 0)

    if p1:
        return find_all_accessible(grid)
    else:
        removed = 0
        while True:
            removed_now = find_all_accessible(grid, True)
            if removed_now == 0:
                break
            removed += removed_now
        return removed


def find_all_accessible(grid, remove=False):
    accessible = 0
    rows, cols = grid.shape
    for y in range(rows):
        for x in range(cols):
            if grid[y][x] == 0: continue
            if is_accessible(grid, y, x, remove):
                accessible += 1
    return accessible


def is_accessible(grid, y, x, remove=False):
    subgrid = grid[max(0, y-1):y+2, max(0, x-1):x+2]
    rolls = np.sum(subgrid)
    if rolls <= 4:  # center roll + max 3 surrounding
        if remove:
            grid[y][x] = 0
        return True
    return False


def main():
    _input_file = 'input'
    expected = {
        'input': (1395, 8451),
        'example': (13, 43),
    }[_input_file]

    run(__file__, solve, _input_file, expected[0], p1=True)
    run(__file__, solve, _input_file, expected[1], p1=False)


if __name__ == '__main__':
    main()
