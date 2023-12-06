from collections import Counter
from aocl import *

red_cubes = 12
green_cubes = 13
blue_cubes = 14


def main():
    lines = read_lines('input')

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
        print('game', line.number, 'required cubes:', max_seen, 'valid', is_valid)

    print('valid game ID sum:', valid_game_id_sum)
    assert valid_game_id_sum == 2879
    print('power sum:', power_sum)
    assert power_sum == 65122


if __name__ == '__main__':
    main()

