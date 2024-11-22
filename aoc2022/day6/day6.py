from aocl import *


def solve(input_file, p1=True):
    lines = read_lines(input_file)

    packet_markers = []
    message_markers = []
    for line in lines:
        packet_markers.append( find_marker(line, 4))
        message_markers.append( find_marker(line, 14))

    if p1:
        return packet_markers
    else:
        return message_markers


def find_marker(s, l):
    for i in range(l, len(s)):
        the_set = set(s[i-l:i])
        if len(the_set) == l:
            return i
    return -1


def main():
    _input_file = 'input'
    expected = {
        'input': ([1093], [3534]),
        'example': ([7, 5, 6, 10, 11], [19, 23, 23, 29, 26]),
    }[_input_file]

    run(__file__, solve, _input_file, expected[0], p1=True)
    run(__file__, solve, _input_file, expected[1], p1=False)


if __name__ == '__main__':
    main()
