import re
import functools
from aocl import *


def solve(input_file, expand):
    records = [splits(s) for s in read_lines(input_file)]

    for i, (springs, groups) in enumerate(records):
        springs = springs.replace('.', '_').replace('?', '.')
        groups = ints(groups)
        if expand > 1:
            springs = '.'.join([springs] * expand)
            groups *= expand
            records[i] = (springs, groups)
        records[i] = (springs, tuple(groups))

    return sum(arrange(springs, groups) for springs, groups in records)


@functools.cache
def arrange(springs, groups):
    if len(groups) == 0:
        return 0 if '#' in springs else 1
    head, tail = groups[:1][0], groups[1:]

    num_arrangements = 0
    for i in range(len(springs) - head - sum(tail) + 1):
        end = '_' if len(tail) > 0 else ''
        test_group = '_' * i + '#' * head + end
        pattern = springs[:len(test_group)]

        if re.match(pattern, test_group):
            num_arrangements += arrange(end + springs[i+head+len(end):], tail)

    return num_arrangements


def main():
    _input_file = 'input'
    expected = {
        'input': (7007, 3476169006222),
        'example': (21, 525152),
    }[_input_file]

    run(__file__, solve, _input_file, expected[0], expand=1)
    run(__file__, solve, _input_file, expected[1], expand=5)


if __name__ == '__main__':
    main()
