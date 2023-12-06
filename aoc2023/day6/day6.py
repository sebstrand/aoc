from aocl import *
from functools import reduce


ignore_spaces = True


def main():
    lines = read_lines('input')

    time = labeline(lines[0], numbered=False)
    distance = labeline(lines[1], numbered=False)

    if ignore_spaces:
        races = [(
            int(time.content.replace(' ', '')),
            int(distance.content.replace(' ', ''))
        )]
    else:
        races = list(zip(ints(time.content), ints(distance.content)))

    win_counts = []
    for time, distance in races:
        holds = range(1, time)
        distances = [(time - hold) * hold for hold in holds]
        distances = [d for d in distances if d > distance]
        win_counts.append(len(distances))

    result = reduce(lambda a, b: a*b, win_counts)
    print('result:', result)
    if ignore_spaces:
        assert result == 43663323
    else:
        assert result == 625968


if __name__ == '__main__':
    main()
