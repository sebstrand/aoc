from aocl import *
from functools import reduce


def solve(input_file, p1=True):
    lines = read_lines(input_file)

    time = labeline(lines[0], numbered=False)
    distance = labeline(lines[1], numbered=False)

    if not p1:
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
    return result


def main():
    _input_file = 'input'
    expected = {
        'input': (625968, 43663323),
        'example': (288, 71503),
    }[_input_file]

    run(__file__, solve, _input_file, expected[0], p1=True)
    run(__file__, solve, _input_file, expected[1], p1=False)


if __name__ == '__main__':
    main()
