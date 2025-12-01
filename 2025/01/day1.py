from aocl import *


def solve(input_file, p1=True):
    lines = read_lines(input_file)

    dial = 50
    password = 0
    for dir, rot in ((l[:1], ints(l)) for l in lines):
        rot = rot[0]
        if dir == 'L':
            rot = -rot

        if p1:
            dial = (dial + rot) % 100
            if dial == 0:
                password += 1
        else:
            full_turns = abs(rot) // 100
            remain_rot = rot % 100
            old = dial
            dial = (dial + remain_rot) % 100

            password += full_turns
            if dial == 0:
                password += 1
            elif old != 0 and rot < 0 and dial > old:
                password += 1
            elif old != 0 and rot > 0 and dial < old:
                password += 1

    return password


def main():
    _input_file = 'input'
    expected = {
        'input': (1048, 6498),
        'example': (3, 6),
    }[_input_file]

    run(__file__, solve, _input_file, expected[0], p1=True)
    run(__file__, solve, _input_file, expected[1], p1=False)


if __name__ == '__main__':
    main()
