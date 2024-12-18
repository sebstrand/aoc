import functools
from aocl import *


def solve(input_file, p1=True):
    lines = read_lines(input_file)

    patterns = tuple(splits(lines[0], sep=(', *',)))
    designs = lines[1:]

    count_all = not p1
    return sum(match(design, patterns, count_all=count_all) for design in designs)


@functools.cache
def match(design: str, patterns: tuple[str], count_all=False):
    if len(design) == 0:
        return 1

    count = 0
    for p in patterns:
        if design.startswith(p):
            count += match(design[len(p):], patterns, count_all=count_all)
            if not count_all and count > 0:
                break
    return count


def main():
    _input_file = 'input'
    expected = {
        'input': (336, 758890600222015),
        'example': (6, 16),
    }[_input_file]

    run(__file__, solve, _input_file, expected[0], p1=True)
    run(__file__, solve, _input_file, expected[1], p1=False)


if __name__ == '__main__':
    main()
