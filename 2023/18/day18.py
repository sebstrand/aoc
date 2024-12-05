from aocl import *


def solve(input_file, p1=True):
    lines = read_lines(input_file)

    plan = []
    for line in lines:
        if p1:
            direction, distance, _ = splits(line)
            distance = int(distance)
            plan.append((direction, distance))
        else:
            _, _, color = splits(line)
            distance = int(color[2:7], 16)
            direction = ('R', 'D', 'L', 'U')[int(color[7])]
            plan.append((direction, distance))

    trench = dig(plan)
    return int(polygon_area(trench))


def dig(plan):
    r, c = 0, 0
    trench = []
    last = plan[-1][0]
    for direction, distance in plan:
        corner = last + direction
        last = direction
        if corner in ('RU', 'UR'):
            trench.append((r, c))
        elif corner in ('RD', 'DR'):
            trench.append((r, c+1))
        elif corner in ('LU', 'UL'):
            trench.append((r+1, c))
        elif corner in ('LD', 'DL'):
            trench.append((r+1, c+1))

        if direction == 'U':
            r -= distance
        elif direction == 'D':
            r += distance
        elif direction == 'L':
            c -= distance
        elif direction == 'R':
            c += distance
    return trench


def main():
    _input_file = 'input'
    expected = {
        'input': (40714, 129849166997110),
        'example': (62, 952408144115),
    }[_input_file]

    run(__file__, solve, _input_file, expected[0], p1=True)
    run(__file__, solve, _input_file, expected[1], p1=False)


if __name__ == '__main__':
    main()
