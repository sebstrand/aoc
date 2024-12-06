from aocl import *


def solve(input_file, p1=True):
    lines = read_lines(input_file)

    pairs = (ints(line) for line in lines)
    left, right = zip(*pairs)

    if p1:
        return sum(
            abs(lx - rx)
            for lx, rx in zip(sorted(left), sorted(right)))
    else:
        return sum(lx * right.count(lx) for lx in left)


def main():
    _input_file = 'input'
    expected = {
        'input': (1579939, 20351745),
        'example': (11, 31),
    }[_input_file]

    run(__file__, solve, _input_file, expected[0], p1=True)
    run(__file__, solve, _input_file, expected[1], p1=False)


if __name__ == '__main__':
    main()
