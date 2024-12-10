import math
import functools
from aocl import *


def solve(input_file, blinks):
    lines = read_lines(input_file)

    stones = ints(lines[0])
    return sum(blink(stone, blinks) for stone in stones)


@functools.cache
def blink(stone: int, blinks: int):
    for i in range(blinks):
        if stone == 0:
            stone = 1
        else:
            digits = int(math.log10(stone)) + 1
            if digits % 2 == 0:
                half = digits // 2
                left = blink(stone // 10**half, blinks - i - 1)
                right = blink(stone % 10**half, blinks - i - 1)
                return left + right
            else:
                stone *= 2024
    return 1


def main():
    _input_file = 'input'
    expected = {
        'input': (235850, 279903140844645),
        'example': (55312, 65601038650482),
    }[_input_file]

    run(__file__, solve, _input_file, expected[0], blinks=25)
    run(__file__, solve, _input_file, expected[1], blinks=75)


if __name__ == '__main__':
    main()
