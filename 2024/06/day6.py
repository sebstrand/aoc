from aocl import *


def solve(input_file, p1=True):
    lines = read_lines(input_file)

    area = {}
    guard_pos = None
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            pos = row * -1j + col
            if char == '^':
                guard_pos = pos
                char = '.'
            area[pos] = char

    guard_path, is_loop = patrol(area, guard_pos)
    assert not is_loop

    if p1:
        return len(guard_path)
    else:
        # Count positions in the guard path where an obstacle causes a loop
        return sum(
            patrol(area | {pos: '#'}, guard_pos)[1]
            for pos in guard_path if pos is not guard_pos and area[pos] == '.'
        )


def patrol(area, starting_pos):
    direction = 1j + 0
    guard_path = {starting_pos: direction}
    is_loop = False
    pos = starting_pos
    while True:
        pos += direction
        tile = area.get(pos)
        if tile is None:
            break
        elif tile != '.':
            pos -= direction
            direction = direction * -1j
        elif guard_path.get(pos) == direction:
            is_loop = True
            break
        else:
            guard_path[pos] = direction

    return guard_path, is_loop


def main():
    _input_file = 'input'
    expected = {
        'input': (4778, 1618),
        'example': (41, 6),
    }[_input_file]

    run(__file__, solve, _input_file, expected[0], p1=True)
    run(__file__, solve, _input_file, expected[1], p1=False)


if __name__ == '__main__':
    main()
