from aocl import *


def main():
    lines = read_lines('input')

    packet_marker = None
    message_marker = None
    for line in lines:
        packet_marker = find_marker(line, 4)
        message_marker = find_marker(line, 14)

    print('packet marker position:', packet_marker)
    assert packet_marker == 1093
    print('message marker position:', message_marker)
    assert message_marker == 3534


def find_marker(s, l):
    for i in range(l, len(s)):
        the_set = set(s[i-l:i])
        if len(the_set) == l:
            return i
    return -1


if __name__ == '__main__':
    main()
