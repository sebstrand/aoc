from aocl import *


def solve(input_file, p1=True):
    lines = read_lines(input_file)
    print('Input:', lines)


def main():
    _input_file = 'example'
    expected = {
        'input': (None, None),
        'example': (None, None),
    }[_input_file]

    run(__file__, solve, _input_file, expected[0], p1=True)
    # run(__file__, solve, _input_file, expected[1], p1=False)


if __name__ == '__main__':
    main()
