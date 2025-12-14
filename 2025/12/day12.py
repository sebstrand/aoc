from aocl import *
import numpy as np


def solve(input_file):
    lines = read_lines(input_file)

    presents = {}
    for label, *shape in zip(*(lines[i:24:4] for i in range(4))):
        index = ints(label)[0]
        shape_grid = gridify(shape, lambda c: 1 if c == '#' else 0)
        presents[index] = shape_grid

    regions = []
    for line in lines[24:]:
        w, h, *counts = ints(line, ('[ x:]',))
        regions.append((np.full((h, w), 0), counts))

    potential = []
    for region, counts in regions:
        rows, cols = region.shape
        region_area = rows * cols

        total_present_area = 0
        for present_index, count in enumerate(counts):
            present = presents[present_index]
            total_present_area += count * np.sum(present)

        if total_present_area <= region_area:
            potential.append((region, counts))

    return len(potential)


def main():
    _input_file = 'input'
    expected = {
        'input': (534, ),
        'example': (2, ),
    }[_input_file]

    run(__file__, solve, _input_file, expected[0])


if __name__ == '__main__':
    main()
