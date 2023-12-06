from aocl import *
import string


priorities_l = [v+1 for v in range(0, len(string.ascii_lowercase)+1)]
priorities_u = [v+27 for v in range(0, len(string.ascii_lowercase)+1)]


def main():
    lines = read_lines('input')

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
            print('badge:', badge)
            badge_p_sum += get_priority(badge)

    print('priority sum:', p_sum)
    assert p_sum == 7848
    print('badge priority sum:', badge_p_sum)
    assert p_sum == 2616


def get_priority(s):
    o = ord(s)
    if o < ord('a'):
        return priorities_u[o - ord('A')]
    else:
        return priorities_l[o - ord('a')]


if __name__ == '__main__':
    main()
