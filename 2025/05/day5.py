from collections import namedtuple
from aocl import *


Range = namedtuple('Range', ['start', 'end'])


def solve(input_file, p1=True):
    lines = read_lines(input_file)

    fresh_ranges = []
    ingredients = []

    for line in lines:
        if '-' in line:
            fresh_ranges.append(Range(*ints(line, ('-',))))
        else:
            ingredients.append(int(line))

    fresh = 0
    if p1:
        for ingredient in ingredients:
            if any(r.start <= ingredient <= r.end for r in fresh_ranges):
                fresh += 1
    else:
        fresh = sum(r.end - r.start + 1 for r in clean_ranges(fresh_ranges))
    return fresh


def clean_ranges(ranges):
    cleaned_ranges = []
    last_end = 0
    for r in sorted(ranges):
        if r.start <= last_end:
            if r.end <= last_end:
                # full overlap
                continue
            else:
                # partial overlap
                cleaned_ranges.append(Range(last_end + 1, r.end))
        else:
            # no overlap
            cleaned_ranges.append(r)
        last_end = r.end
    return cleaned_ranges


def main():
    _input_file = 'input'
    expected = {
        'input': (638, 352946349407338),
        'example': (3, 14),
    }[_input_file]

    run(__file__, solve, _input_file, expected[0], p1=True)
    run(__file__, solve, _input_file, expected[1], p1=False)


if __name__ == '__main__':
    main()
