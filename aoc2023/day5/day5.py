from aocl import *
from collections import defaultdict, deque


use_seed_ranges = True


def main():
    lines = read_lines('input')

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

    if use_seed_ranges:
        seed_ranges = deque(zip(seeds[::2], seeds[1::2]))
    else:
        seed_ranges = deque(zip(seeds, [1]*len(seeds)))

    soil_ranges = lookup(maps['seed-to-soil'], seed_ranges)
    fertilizer_ranges = lookup(maps['soil-to-fertilizer'], soil_ranges)
    water_ranges = lookup(maps['fertilizer-to-water'], fertilizer_ranges)
    light_ranges = lookup(maps['water-to-light'], water_ranges)
    temperature_ranges = lookup(maps['light-to-temperature'], light_ranges)
    humidity_ranges = lookup(maps['temperature-to-humidity'], temperature_ranges)
    location_ranges = lookup(maps['humidity-to-location'], humidity_ranges)

    min_location = min([start for start, n in location_ranges])
    print('min location:', min_location)
    if use_seed_ranges:
        assert min_location == 108956227
    else:
        assert min_location == 322500873


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


if __name__ == '__main__':
    main()
