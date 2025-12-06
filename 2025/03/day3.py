from aocl import *


def solve(input_file, p1=True):
    banks = read_lines(input_file)
    max_total_joltage = 0
    for bank in banks:
        max_total_joltage += int(find_max_joltage(bank, 2 if p1 else 12))
    return max_total_joltage


def find_max_joltage(bank, n):
    joltage_a = str(max(int(b) for b in bank[:len(bank)-n+1]))
    a_pos = bank.index(joltage_a)
    return joltage_a + (find_max_joltage(bank[a_pos + 1:], n-1) if n > 1 else '')


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
