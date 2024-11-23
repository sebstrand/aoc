import math

from collections import namedtuple
from aocl import *


sensor_report = namedtuple('sensor_report', ['sensor', 'beacon', 'distance'])


def solve(input_file, x_range=(-math.inf, math.inf), y_range=(0, 0)):
    lines = read_lines(input_file)

    sensor_reports = []
    for line in lines:
        parts = splits(line, sep=('[,:]? ',))
        # Throw away everything except coordinates
        parts = parts[2:4] + parts[-2:]
        s_pos1 = p2d(int(parts[1][2:]), int(parts[0][2:]))
        b_pos2 = p2d(int(parts[3][2:]), int(parts[2][2:]))
        sensor_reports.append(
            sensor_report(
                sensor=s_pos1,
                beacon=b_pos2,
                distance=manhattan(s_pos1, b_pos2)))

    no_beacon_positions = None
    for y in range(y_range[0], y_range[1]+1):
        covered_intervals = find_covered_intervals(sensor_reports, x_range, y)
        used_x_positions = find_used_positions(sensor_reports, y)
        for x in used_x_positions:
            covered_intervals.remove(x, x)

        possible_intervals = Intervals()
        if x_range[1] < math.inf:
            possible_intervals.add(*x_range)
            for x in used_x_positions:
                possible_intervals.remove(x, x)

        no_beacon_positions = 0
        for x_start, x_end in covered_intervals.intervals:
            no_beacon_positions += (x_end - x_start) + 1
            possible_intervals.remove(x_start, x_end)

        if len(possible_intervals) == 1:
            x = next(iter(possible_intervals))
            pos = p2d(x=x, y=y)
            return pos.x * 4000000 + pos.y

    return no_beacon_positions


def find_covered_intervals(sensor_reports, x_range, y):
    """Finds the intervals on the row at y that is covered by a sensor."""
    covered_intervals = Intervals()
    for report in sensor_reports:
        y_dist = abs(y - report.sensor.y)
        # The further away a sensor is vertically, the less range (spread) it has in the x direction."""
        x_spread = report.distance - y_dist
        if x_spread >= 0:
            x_start = max(x_range[0], report.sensor.x - x_spread)
            x_end = min(x_range[1], report.sensor.x + x_spread)
            if x_start <= x_end:
                covered_intervals.add(x_start, x_end)
    return covered_intervals


def find_used_positions(sensor_reports, y):
    """Finds the set of positions on the row at y that is taken up by sensors or beacons."""
    row_beacons = {report.beacon.x for report in sensor_reports if report.beacon.y == y}
    row_sensors = {report.sensor.x for report in sensor_reports if report.sensor.y == y}
    return row_beacons | row_sensors


def main():
    _input_file = 'input'
    expected = {
        'input': (5525847, 13340867187704),
        'example': (26, 56000011),
    }[_input_file]

    y = {'input': 2000000, 'example': 10}[_input_file]
    run(__file__, solve, _input_file, expected[0], y_range=(y, y))

    search_area = {'input': (0, 4000000), 'example': (0, 20)}[_input_file]
    run(__file__, solve, _input_file, expected[1], x_range=search_area, y_range=search_area)


if __name__ == '__main__':
    main()
