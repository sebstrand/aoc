from aocl import *
import string


priorities_l = [v+1 for v in range(0, len(string.ascii_lowercase)+1)]
priorities_u = [v+27 for v in range(0, len(string.ascii_lowercase)+1)]


def solve(input_file, p1=True):
    lines = read_lines(input_file)

    p_sum = 0
    badge_p_sum = 0
    badge_set = None
    for i, line in enumerate(lines):
        c1 = set(line[:len(line)//2])
        c2 = set(line[len(line)//2:])
        shared = c1.intersection(c2).pop()
        p_sum += get_priority(shared)

        if i % 3 == 0:
            badge_set = set(line)
        else:
            badge_set = badge_set.intersection(set(line))

        if i % 3 == 2:
            badge = badge_set.pop()
            badge_p_sum += get_priority(badge)

    if p1:
        return p_sum
    else:
        return badge_p_sum


def get_priority(s):
    o = ord(s)
    if o < ord('a'):
        return priorities_u[o - ord('A')]
    else:
        return priorities_l[o - ord('a')]


def main():
    _input_file = 'input'
    expected = {
        'input': (7848, 2616),
        'example': (157, 70),
    }[_input_file]

    run(__file__, solve, _input_file, expected[0], p1=True)
    run(__file__, solve, _input_file, expected[1], p1=False)


if __name__ == '__main__':
    main()
