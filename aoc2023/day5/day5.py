from aocl import *
from collections import defaultdict, deque


def solve(input_file, p1=True):
    lines = read_lines(input_file)

    seeds = []
    maps = defaultdict(list)
    label = None
    for line in lines:
        lbl = labeline(line, numbered=False)
        if lbl:
            label = lbl.label
            if lbl.content:
                seeds = ints(lbl.content)
        else:
            add_to_map(maps, label.replace(' map', ''), ints(line))

    if p1:
        seed_ranges = deque(zip(seeds, [1]*len(seeds)))
    else:
        seed_ranges = deque(zip(seeds[::2], seeds[1::2]))

    soil_ranges = lookup(maps['seed-to-soil'], seed_ranges)
    fertilizer_ranges = lookup(maps['soil-to-fertilizer'], soil_ranges)
    water_ranges = lookup(maps['fertilizer-to-water'], fertilizer_ranges)
    light_ranges = lookup(maps['water-to-light'], water_ranges)
    temperature_ranges = lookup(maps['light-to-temperature'], light_ranges)
    humidity_ranges = lookup(maps['temperature-to-humidity'], temperature_ranges)
    location_ranges = lookup(maps['humidity-to-location'], humidity_ranges)

    return min([start for start, n in location_ranges])


def add_to_map(maps, map_name, range_spec):
    destination_start, source_start, n = range_spec
    maps[map_name].append((source_start, destination_start, n))


def lookup(map_data, value_ranges):
    output = deque()
    while len(value_ranges) > 0:
        value_range = value_ranges.popleft()

        value_min, num = value_range
        value_max = value_min + num - 1

        found = False
        for source_min, destination_min, n in map_data:
            adjust = destination_min - source_min
            source_max = source_min + n

            overlap_min = max(source_min, value_min)
            overlap_max = min(source_max, value_max)

            if overlap_min <= overlap_max:
                found = True
                output.append((overlap_min + adjust, overlap_max - overlap_min + 1))

                if overlap_min > value_min:
                    value_ranges.append((value_min, overlap_min - value_min))
                if overlap_max < value_max:
                    value_ranges.append((overlap_max+1, value_max-overlap_max))

        if not found:
            output.append((value_min, num))
    return output


def main():
    _input_file = 'input'
    expected = {
        'input': (322500873, 108956227),
        'example': (35, 46),
    }[_input_file]

    run(__file__, solve, _input_file, expected[0], p1=True)
    run(__file__, solve, _input_file, expected[1], p1=False)


if __name__ == '__main__':
    main()
