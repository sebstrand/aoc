from aocl import *
from collections import Counter


def solve(input_file, p1=True):
    lines = read_lines(input_file, skip_empty=False)

    elves = Counter()
    elf = 0
    for line in lines:
        if not line:
            elf += 1
        else:
            elves[elf] += int(line)

    calories = list(elves.values())
    if p1:
        return max(calories)

    calories.sort(reverse=True)
    return sum(calories[:3])


def main():
    _input_file = 'input'
    expected = {
        'input': (69836, 207968),
        'example': (24000, 45000),
    }[_input_file]

    run(__file__, solve, _input_file, expected[0], p1=True)
    run(__file__, solve, _input_file, expected[1], p1=False)


if __name__ == '__main__':
    main()
