from collections import Counter
from aocl import *

red_cubes = 12
green_cubes = 13
blue_cubes = 14


def solve(input_file, p1=True):
    lines = read_lines(input_file)

    valid_game_id_sum = 0
    power_sum = 0
    for line in lines:
        line = labeline(line)
        max_seen = Counter()
        for num, color in visit(splits(line.content, sep=(';', ',', ' '))):
            max_seen[color] = max(max_seen[color], int(num))

        is_valid = (
            max_seen['red'] <= red_cubes and
            max_seen['green'] <= green_cubes and
            max_seen['blue'] <= blue_cubes
        )

        if is_valid:
            valid_game_id_sum += line.number
        power_sum += max_seen['red'] * max_seen['green'] * max_seen['blue']
        # print('game', line.number, 'required cubes:', max_seen, 'valid', is_valid)

    if p1:
        return valid_game_id_sum
    else:
        return power_sum


def main():
    _input_file = 'input'
    expected = {
        'input': (2879, 65122),
        'example': (8, 2286),
    }[_input_file]

    run(__file__, solve, _input_file, expected[0], p1=True)
    run(__file__, solve, _input_file, expected[1], p1=False)


if __name__ == '__main__':
    main()
