from aocl import *


valid_mas_pairs = (('M', 'S'), ('S', 'M'))


def solve(input_file, p1=True):
    lines = read_lines(input_file)

    # Make grid with (row,col) as key and letter as value
    grid = {}
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            grid[(row, col)] = char

    count = 0
    for (row, col), char in grid.items():
        if p1 and char == 'X':
            count += find_xmas(grid, row, col)
        elif not p1 and char == 'A':
            if find_x_mas(grid, row, col):
                count += 1
    return count


def find_xmas(grid, row, col):
    """Find the word XMAS starting from X at (row, col)"""
    count = 0
    for rd in -1, 0, 1:
        for cd in -1, 0, 1:
            char = grid.get((row + 1*rd, col + 1*cd))
            if char != 'M': continue
            char = grid.get((row + 2*rd, col + 2*cd))
            if char != 'A': continue
            char = grid.get((row + 3*rd, col + 3*cd))
            if char != 'S': continue
            count += 1
    return count


def find_x_mas(grid, row, col):
    """Find MAS in the shape of an X starting from A at (row, col)"""
    pair1 = grid.get((row-1, col-1)), grid.get((row+1, col+1))
    pair2 = grid.get((row+1, col-1)), grid.get((row-1, col+1))

    return pair1 in valid_mas_pairs and pair2 in valid_mas_pairs


def main():
    _input_file = 'input'
    expected = {
        'input': (2521, 1912),
        'example': (18, 9),
    }[_input_file]

    run(__file__, solve, _input_file, expected[0], p1=True)
    run(__file__, solve, _input_file, expected[1], p1=False)


if __name__ == '__main__':
    main()
