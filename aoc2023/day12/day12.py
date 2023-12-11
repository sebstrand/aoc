from aocl import *
import time
from itertools import groupby
from collections import Counter
import math


expand = 5


def main():
    lines = [splits(s) for s in read_lines('input')]

    start = time.time()
    arrangement_sum = 0
    for i, (springs, groups) in enumerate(lines):
        groups = ints(groups)
        if expand > 1:
            springs = '?'.join([springs] * expand)
            groups *= expand
        groups = tuple(groups)
        print('r', i, springs, groups)

        gaps = len(groups) + 1
        min_p_len = sum(groups) + gaps - 2
        free_len = len(springs) - min_p_len
        assert free_len >= 0
        print('record', springs)
        print('  rlen', len(springs), 'min_p_len', min_p_len, 'free', free_len, 'gaps', gaps)

        s_possible = []
        for s in range(free_len):
            test = springs[:s].replace('?', '.') + '#' * groups[0]
            spring_pattern = re.compile(springs[:s + groups[0]].replace('.', r'\.').replace('?', '.'))
            if test.index('#') < s:
                break
            elif spring_pattern.match(test):
                print('  match', test)
                s_possible.append(s)
            pass
        print('  s possible', s_possible)

        gaparr = len(s_possible)
        for sp in s_possible:
            gaparr += space_gaps(free_len - sp, gaps - 1)
        print('  gaparr', gaparr, '<', space_gaps(free_len, gaps))


        e_possible = []
        for s in range(free_len):
            test = springs[:s].replace('?', '.') + '#' * groups[0]
            spring_pattern = re.compile(springs[:s + groups[0]].replace('.', r'\.').replace('?', '.'))
            if test.index('#') < s:
                break
            elif spring_pattern.match(test):
                print('  match', test)
                e_possible.append(s)
            pass
        print('  e possible', e_possible)

        record_sum = 0
        # for p in doit(springs, groups):
        #     record_sum += 1
        arrangement_sum += record_sum
        print('  line arrangements:', record_sum)
        if i >= 1000:
            break

    print('result:', arrangement_sum)
    print('time:', time.time() - start)
    if expand:
        assert False
    else:
        assert arrangement_sum == 7007


def doit(record, groups, permutation=''):
    anchor = record.find('#')
    if len(groups) == 0:
        if anchor < 0:
            # One solution found
            yield 1
        else:
            # There are unmatched groups
            pass
        return

    n_open = record.count('?')
    if n_open == 0 and anchor < 0:
        # No way of generating missing groups
        return

    group_len = groups[0]
    prefix = '.' * 0
    suffix = '.' * 0

    for x in range(420):
        doit(record, groups[1:], permutation)


def space_gaps(spaces, gaps):
    n = spaces + gaps - 1
    k = gaps - 1
    return int(math.factorial(n)/(math.factorial(k)*math.factorial(n-k)))


def permutate_run(run, i=0):
    if i == len(run):
        yield ''
    else:
        chars = run[i]
        if chars == '?':
            chars = '#.'

        for c in chars:
            for p in permutate_run(run, i+1):
                yield c + p


def permutate(record, groups, permutation=None):
    if not permutation:
        permutation = []

    c = record[len(permutation)]
    if c == '?':
        c = '#.'

    permutation.append(None)
    for x in c:
        permutation[-1] = x
        is_full = len(permutation) == len(record)
        if check(permutation, groups, match=is_full):
            if is_full:
                yield 1
            else:
                for _ in permutate(record, groups, permutation):
                    yield 1

    permutation.pop()


def check(permutation, groups, match=False):
    groups_now = groups_in(permutation)
    # print('  check', ''.join(permutation), groups_now, groups)
    if match:
        return groups_now == groups
    else:
        return groups_now <= groups[:len(groups_now)]


def groups_in(p):
    return tuple(len(tuple(g)) for k, g in groupby(p) if k != '.')


if __name__ == '__main__':
    main()
