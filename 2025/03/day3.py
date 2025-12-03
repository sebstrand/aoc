import functools
from aocl import *


def solve(input_file, p1=True):
    banks = read_lines(input_file)
    max_total_joltage = 0
    for bank in banks:
        max_total_joltage += find_max_joltage(bank, 2 if p1 else 12)
    return max_total_joltage


@functools.cache
def find_max_joltage(bank, n):
    max_joltage = 0
    for i, joltage_a in enumerate(bank[:len(bank)-n+1]):
        if n > 1:
            joltage_b = str(find_max_joltage(bank[i + 1:], n-1))
            joltage = int(joltage_a + joltage_b)
        else:
            joltage = int(joltage_a)
        if joltage > max_joltage:
            max_joltage = joltage
    return max_joltage


def main():
    _input_file = 'input'
    expected = {
        'input': (17613, 175304218462560),
        'example': (357, 3121910778619),
    }[_input_file]

    run(__file__, solve, _input_file, expected[0], p1=True)
    run(__file__, solve, _input_file, expected[1], p1=False)


if __name__ == '__main__':
    main()
