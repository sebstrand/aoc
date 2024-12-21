from aocl import *


def solve(input_file, p1=True):
    codes = read_lines(input_file)
    print('Codes:', codes)

    numeric = Keypad('numeric', {
        (0, 0): '7',
        (0, 1): '8',
        (0, 2): '9',
        (1, 0): '4',
        (1, 1): '5',
        (1, 2): '6',
        (2, 0): '1',
        (2, 1): '2',
        (2, 2): '3',
        (3, 1): '0',
        (3, 2): 'A',
    }, (3, 2))

    directional_keys = {
        (0, 1): '^',
        (0, 2): 'A',
        (1, 0): '<',
        (1, 1): 'v',
        (1, 2): '>',
    }

    robot1 = Keypad('robot1', directional_keys, (0, 2))
    robot2 = Keypad('robot2', directional_keys, (0, 2))
    normal = Keypad('normal', directional_keys, (0, 2))


class Keypad:
    def __init__(self, name, keys, current):
        self.name = name
        self.keys = keys
        self.current = current

    def __str__(self):
        return f'Keypad "{self.name}" at {self.current} = {self.keys[self.current]}'


def main():
    _input_file = 'example'
    expected = {
        'input': (None, None),
        'example': (126384, None),
    }[_input_file]

    run(__file__, solve, _input_file, expected[0], p1=True)
    # run(__file__, solve, _input_file, expected[1], p1=False)


if __name__ == '__main__':
    main()
