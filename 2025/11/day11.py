import functools
from aocl import *


def solve(input_file, p1=True):
    lines = read_lines(input_file)

    devices = {}
    for line in lines:
        parts = splits(line)
        devices[parts[0][:-1]] = parts[1:]

    if p1:
        return count_paths(CacheIgnore(devices), 'you', True, True)
    else:
        return count_paths(CacheIgnore(devices), 'svr', False, False)


@functools.cache
def count_paths(devices, start, seen_fft, seen_dac):
    count = 0
    for device in devices[start]:
        if device == 'out':
            if seen_fft and seen_dac:
                count += 1
        else:
            count += count_paths(devices, device, seen_fft or device == 'fft', seen_dac or device == 'dac')
    return count


def main():
    _input_file = 'input'
    expected = {
        'input': (511, 458618114529380),
        'example': (5, None),
        'example2': (None, 2),
    }[_input_file]

    run(__file__, solve, _input_file, expected[0], p1=True)
    run(__file__, solve, _input_file, expected[1], p1=False)


if __name__ == '__main__':
    main()
