from collections import deque
from aocl import *


def solve(input_file, p1=True):
    lines = read_lines(input_file)

    plots = {}
    for r, line in enumerate(lines):
        for c, char in enumerate(line):
            plots[r, c] = char

    modifiable_plots = plots.copy()
    regions = [floodfill(modifiable_plots, pos) for pos in plots.keys()]

    fence_cost_metric = perimeter_length if p1 else count_sides
    return sum(fence_cost_metric(plots, region) * len(region) for region in regions if len(region))


def floodfill(plots, start):
    plant = plots.get(start)
    q = deque()
    q.append(start)

    region = {}
    while len(q):
        pos = q.popleft()

        plant_here = plots.get(pos)
        if plant_here is None:
            continue
        elif plant_here == plant:
            plots[pos] = None
            region[pos] = plant_here

        for n_pos in iter_neighbors(pos):
            if n_pos not in region and plots.get(n_pos) == plant:
                q.appendleft(n_pos)
    return region


def perimeter_length(plots, region):
    perimeter = 0
    for pos, plant in region.items():
        for n_pos in iter_neighbors(pos):
            n_plant = plots.get(n_pos)
            if n_plant is None or plant != n_plant:
                perimeter += 1
    return perimeter


def count_sides(plots, region):
    sides = {'ns': [], 'ew': []}

    for pos, plant in region.items():
        for direction, n_pos in iter_neighbors(pos, named=True):
            n_plant = plots.get(n_pos)
            if n_plant is None or plant != n_plant:
                side_start, side_end, orientation = side_from_pos(pos, direction)
                add_side(sides[orientation], side_start, side_end)

    return len(sides['ns']) + len(sides['ew']) + find_splits(sides)


def find_splits(sides):
    """
    Finds the number of positions where a side meets a side going the other way at some point other
    than the end positions of the first side. In this case the first side is really two sides.
    """
    corner_splits = 0
    for orientation_a, orientation_b in (('ns', 'ew'), ('ew', 'ns')):
        sides_a, sides_b = sides[orientation_a], sides[orientation_b]
        for side in sides_a:
            # Sort so that end positions are first and last, then iterate non-end positions
            for pos in list(sorted(side))[1:-1]:
                for crossing_side in sides_b:
                    if pos in crossing_side:
                        corner_splits += 1
                        break
    return corner_splits


def side_from_pos(pos, direction):
    match direction:
        case 'n':
            return pos, (pos[0], pos[1]+1), 'ew'
        case 's':
            return (pos[0]+1, pos[1]), (pos[0]+1, pos[1]+1), 'ew'
        case 'e':
            return (pos[0], pos[1]+1), (pos[0]+1, pos[1]+1), 'ns'
        case 'w':
            return pos, (pos[0]+1, pos[1]), 'ns'


def add_side(sides, start, end):
    start_set = None
    end_set = None
    for position_set in sides:
        if start in position_set:
            start_set = position_set
        if end in position_set:
            end_set = position_set

    if start_set is None and end_set is None:
        sides.append({start, end})
    elif start_set is None:
        end_set.add(start)
    elif end_set is None:
        start_set.add(end)
    else:
        assert start_set != end_set
        start_set.update(end_set)
        sides.remove(end_set)


def iter_neighbors(pos, named=False):
    if named:
        yield 'n', (pos[0] - 1, pos[1])
        yield 's', (pos[0] + 1, pos[1])
        yield 'w', (pos[0], pos[1] - 1)
        yield 'e', (pos[0], pos[1] + 1)
    else:
        yield pos[0] - 1, pos[1]
        yield pos[0] + 1, pos[1]
        yield pos[0], pos[1] - 1
        yield pos[0], pos[1] + 1


def main():
    _input_file = 'input'
    expected = {
        'input': (1370100, 818286),
        'example': (140, 80),
        'example2': (772, 436),
        'example3': (1930, 1206),
    }[_input_file]

    run(__file__, solve, _input_file, expected[0], p1=True)
    run(__file__, solve, _input_file, expected[1], p1=False)


if __name__ == '__main__':
    main()
