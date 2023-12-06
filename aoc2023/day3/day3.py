from aocl import *


number_re = re.compile(r'\D*(\d+)')
symbol_re = re.compile(r'[.\d]*([^0-9.])')


def main():
    lines = read_lines('input')

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
    print(number_locations)
    print(symbol_locations)

    part_numbers = []
    for number, n_line, n_col_start, n_col_end in number_locations:
        for symbol, s_line, s_col in symbol_locations:
            if n_line - 1 <= s_line <= n_line + 1 and n_col_start - 1 <= s_col <= n_col_end + 1:
                part_numbers.append(int(number))
                break
    part_number_sum = sum(part_numbers)
    print('part number sum:', part_number_sum)
    assert part_number_sum == 536576

    gear_ratios = []
    for symbol, s_line, s_col in symbol_locations:
        if symbol == '*':
            adjacent_numbers = []
            for number, n_line, n_col_start, n_col_end in number_locations:
                if n_line - 1 <= s_line <= n_line + 1 and n_col_start - 1 <= s_col <= n_col_end + 1:
                    adjacent_numbers.append(number)
            if len(adjacent_numbers) == 2:
                gear_ratios.append(int(adjacent_numbers[0]) * int(adjacent_numbers[1]))

    print('gear ratios:', gear_ratios)
    gear_ratio_sum = sum(gear_ratios)
    print('gear ratio sum:', gear_ratio_sum)
    assert gear_ratio_sum == 75741499


if __name__ == '__main__':
    main()
