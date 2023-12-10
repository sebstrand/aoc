import math
import numpy as np
from aocl import *


valid_pipes = 'S|LJ7F-'


def main():
    lines = read_lines('input')

    grid = np.empty((len(lines), len(lines[0])), dtype=[('pipe', 'U1'), ('dist', 'i4')])
    print('grid size:', grid.shape)

    start = None
    for r, row in enumerate(lines):
        for c, pipe in enumerate(row):
            grid['pipe'][r, c] = pipe
            if pipe == 'S':
                start = (r, c)

    print('start:', start)
    start_directions = get_start_directions(grid, start)
    assert len(start_directions) == 2

    start_pipe = get_start_pipe(start, start_directions)
    grid['pipe'][*start] = start_pipe

    previous = start
    pos = start_directions[0]
    distance = 1
    grid['dist'][*start] = distance
    while True:
        distance += 1
        grid['dist'][*pos] = distance
        for d in get_directions(grid, pos):
            if d != previous:
                previous = pos
                pos = d
                break
        if pos == start:
            break

    loop_length = distance
    max_dist = math.ceil(loop_length / 2)
    print('loop length:', loop_length)
    print('max dist:', max_dist)
    print('distances:\n', grid['dist'])
    assert max_dist == 6867

    enclosed = find_enclosed(grid)
    print('enclosed:\n', enclosed)
    print()

    visualize(grid, 'grid.png', type='all')
    visualize(grid, 'grid_loop.png', type='loop')
    visualize(enclosed, 'grid_enclosed.png', type='enclosed')

    num_enclosed = (enclosed > 0).sum()
    print('num enclosed:', num_enclosed)
    assert num_enclosed == 595


def get_start_directions(grid, start_pos):
    start_directions = []
    for pos, _ in [n for n in neighbors_2d(grid, start_pos) if n]:
        n_dir = get_directions(grid, pos)
        if start_pos in n_dir:
            start_directions.append(pos)
    return start_directions


def get_directions(grid, pos):
    pipe = grid['pipe'][*pos]
    neighbors = neighbors_2d(grid, pos)

    if pipe == '|':
        neighbors = neighbors[0], neighbors[1]
    elif pipe == '-':
        neighbors = neighbors[2], neighbors[3]
    elif pipe == 'L':
        neighbors = neighbors[0], neighbors[3]
    elif pipe == 'J':
        neighbors = neighbors[0], neighbors[2]
    elif pipe == 'F':
        neighbors = neighbors[1], neighbors[3]
    elif pipe == '7':
        neighbors = neighbors[1], neighbors[2]

    return [n[0] for n in neighbors if n is not None]


def get_start_pipe(start_pos, start_directions):
    start_pipe = set(valid_pipes)
    start_pipe.discard('S')

    for row, col in start_directions:
        if row == start_pos[0]:
            start_pipe.discard('|')
            if col < start_pos[1]:
                start_pipe.discard('L')
                start_pipe.discard('F')
            else:
                start_pipe.discard('7')
                start_pipe.discard('J')
        elif col == start_pos[1]:
            start_pipe.discard('-')
            if row < start_pos[0]:
                start_pipe.discard('F')
                start_pipe.discard('7')
            else:
                start_pipe.discard('J')
                start_pipe.discard('L')

    return ''.join(start_pipe)


def find_enclosed(grid):
    enclosed = np.zeros(grid.shape, dtype=np.byte)
    rows, cols = grid.shape
    for r in range(rows):
        inside = False
        for c in range(cols):
            pipe, dist = grid[r, c]
            if dist > 0 and pipe in '|7F':
                # Counting vertical pipes and down connections as crossings. Counting up connections instead of down
                # connections would also work. Each crossing flips the inside/outside state.
                inside = not inside
            elif dist == 0:
                # Non-pipe location, update with current inside/outside state
                enclosed[r, c] = (-1, 1)[inside]

    return enclosed


def visualize(grid, filename, type='all'):
    tiles = {}

    if type == 'enclosed':
        c = (255, 255, 255, 128)
        tiles[1] = ((c, c, c), (c, c, c), (c, c, c))
        visualize_grid(grid, filename, tiles)
    else:
        for pipe in valid_pipes:
            c = (0, 255, 0)
            if pipe == 'S':
                continue
            if pipe == '|':
                tile = (
                    (0, c, 0),
                    (0, c, 0),
                    (0, c, 0),
                )
            elif pipe == '-':
                tile = (
                    (0, 0, 0),
                    (c, c, c),
                    (0, 0, 0),
                )
            elif pipe == 'F':
                tile = (
                    (0, 0, 0),
                    (0, c, c),
                    (0, c, 0),
                )
            elif pipe == '7':
                tile = (
                    (0, 0, 0),
                    (c, c, 0),
                    (0, c, 0),
                )
            elif pipe == 'L':
                tile = (
                    (0, c, 0),
                    (0, c, c),
                    (0, 0, 0),
                )
            elif pipe == 'J':
                tile = (
                    (0, c, 0),
                    (c, c, 0),
                    (0, 0, 0),
                )
            tiles[pipe] = tile

        if type != 'all':
            grid = grid.copy()
            grid['pipe'][grid['dist'] == 0] = '.'
        visualize_grid(grid['pipe'], filename, tiles, bg_color=(0, 0, 0))


if __name__ == '__main__':
    main()
