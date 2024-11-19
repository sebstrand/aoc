import re
from aocl import *


number_re = re.compile(r'\D*(\d+)')
symbol_re = re.compile(r'[.\d]*([^0-9.])')


def solve(input_file, p1=True):
    lines = read_lines(input_file)

    number_locations = []
    symbol_locations = []

    for i, line in enumerate(lines):
        pos = 0
        while True:
            m = number_re.match(line, pos)
            if m is None:
                break
            pos = m.end()
            number_locations.append((m.group(1), i, m.start(1), m.end(1)-1))

        pos = 0
        while True:
            m = symbol_re.match(line, pos)
            if m is None:
                break
            pos = m.end()
            symbol_locations.append((m.group(1), i, m.start(1)))

    part_numbers = []
    for number, n_line, n_col_start, n_col_end in number_locations:
        for symbol, s_line, s_col in symbol_locations:
            if n_line - 1 <= s_line <= n_line + 1 and n_col_start - 1 <= s_col <= n_col_end + 1:
                part_numbers.append(int(number))
                break
    if p1:
        return sum(part_numbers)

    gear_ratios = []
    for symbol, s_line, s_col in symbol_locations:
        if symbol == '*':
            adjacent_numbers = []
            for number, n_line, n_col_start, n_col_end in number_locations:
                if n_line - 1 <= s_line <= n_line + 1 and n_col_start - 1 <= s_col <= n_col_end + 1:
                    adjacent_numbers.append(number)
            if len(adjacent_numbers) == 2:
                gear_ratios.append(int(adjacent_numbers[0]) * int(adjacent_numbers[1]))

    return sum(gear_ratios)


def main():
    _input_file = 'input'
    expected = {
        'input': (536576, 75741499),
        'example': (4361, 467835),
    }[_input_file]

    run(__file__, solve, _input_file, expected[0], p1=True)
    run(__file__, solve, _input_file, expected[1], p1=False)


if __name__ == '__main__':
    main()
