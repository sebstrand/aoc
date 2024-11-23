import numpy as np
from aocl import *


AIR = 0
ROCK = 1
SAND = 2
SAND_X = 500


def solve(input_file, p1=True):
    lines = read_lines(input_file)

    x_min = np.inf
    x_max = 0
    y_max = 0
    rock_lines = []
    for line in lines:
        previous = None
        for x, y in splits(line, sep=(' *-> *', ','), f=int):
            x_min = min(x_min, x)
            x_max = max(x_max, x)
            y_max = max(y_max, y)
            if previous is not None:
                rock_lines.append((previous, p2d(y, x)))
            previous = p2d(y, x)

    x_min = x_base = min(int(SAND_X - y_max * 1.5), x_min)
    x_max = max(int(SAND_X + y_max * 1.5), x_max)
    width = x_max - x_min
    height = y_max + 3
    grid = np.zeros((height, width), dtype=np.uint8) + AIR
    for pos1, pos2 in rock_lines:
        add_rock(grid, pos1, pos2, x_base)

    if not p1:
        add_rock(grid, p2d(height - 1, x_base), p2d(height - 1, x_base + width - 1), x_base)

    sand_count = 0
    while add_sand(grid, x_base):
        sand_count += 1
    # visualize(grid)
    return sand_count


def visualize(grid):
    tiles = {}
    cr = (255, 255, 255, 128)
    cs = (255, 255, 0, 255)
    tiles[ROCK] = ((cr, cr, cr), (cr, cr, cr), (cr, cr, cr))
    tiles[SAND] = ((cs, cs, cs), (cs, cs, cs), (cs, cs, cs))
    visualize_grid(grid, 'rocks.png', tiles, bg_color=(0, 0, 0, 255), show=True)


def add_rock(grid, pos1, pos2, x_base):
    ys, ye = min(pos1.y, pos2.y), max(pos1.y, pos2.y)
    xs, xe = min(pos1.x, pos2.x), max(pos1.x, pos2.x)
    # print(pos1, '->', pos2, (xs, xe), (ys, ye))
    for x in range(xs, xe + 1):
        for y in range(ys, ye + 1):
            grid[y, x - x_base] = ROCK


def add_sand(grid, x_base):
    bottom = grid.shape[0] - 1
    y, x = 0, SAND_X - x_base
    if grid[y, x] == SAND:
        return False

    while True:
        support = grid[y:bottom + 1, x].nonzero()[0]
        if len(support) == 0:
            # sand falling out the bottom
            return False

        y_hit = y + support[0]
        if grid[y_hit, x - 1] == AIR:
            x = x - 1
            y = y_hit
        elif grid[y_hit, x + 1] == AIR:
            x = x + 1
            y = y_hit
        else: # sand came to rest
            grid[y_hit - 1, x] = SAND
            return True


def main():
    _input_file = 'example'
    expected = {
        'input': (964, 32041),
        'example': (24, 93),
    }[_input_file]

    run(__file__, solve, _input_file, expected[0], p1=True)
    run(__file__, solve, _input_file, expected[1], p1=False)


if __name__ == '__main__':
    main()
