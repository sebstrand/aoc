from collections import defaultdict
import functools
from aocl import *


def solve(input_file, p1=True):
    lines = read_lines(input_file)

    ordering = defaultdict(list)
    updates = []
    for line in lines:
        if '|' in line:
            sooner, later = ints(line)
            ordering[sooner].append(later)
        elif ',' in line:
            updates.append(ints(line))

    middle = lambda u: u[len(u) // 2]
    if p1:
        return sum(map(
            middle,
            (u for u in updates if is_ordered(u, ordering))))
    else:
        return sum(map(
            middle,
            (sort_update(u, ordering) for u in updates if not is_ordered(u, ordering))))


def is_ordered(update, ordering):
    for i, number in enumerate(update[1:]):
        later = ordering[number]
        if any(p in later for p in update[:i]):
            return False
    return True


def sort_update(update, ordering):
    sort_key = functools.cmp_to_key(lambda a, b: compare(a, b, ordering))
    update.sort(key=sort_key)
    return update


def compare(a, b, ordering):
    later = ordering[b]
    if a in later:
        return 1
    return -1


def main():
    _input_file = 'input'
    expected = {
        'input': (5955, 4030),
        'example': (143, 123),
    }[_input_file]

    run(__file__, solve, _input_file, expected[0], p1=True)
    run(__file__, solve, _input_file, expected[1], p1=False)


if __name__ == '__main__':
    main()
