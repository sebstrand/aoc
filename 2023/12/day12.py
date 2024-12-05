import math
import re
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from aocl import *


debug = False


def solve(input_file, expand, record_range=None):
    records = [splits(s) for s in read_lines(input_file)]

    for i, (springs, groups) in enumerate(records):
        springs = springs.replace('.', '_').replace('?', '.')
        groups = ints(groups)
        if expand > 1:
            springs = '.'.join([springs] * expand)
            groups *= expand
            records[i] = (springs, groups)
        records[i] = (springs, groups)

    start = time.time()
    total_arrangements = 0

    if record_range is not None:
        records = records[record_range[0]:record_range[1]]
    # unfinished = (303, 625, 925)
    unfinished = list(range(len(records)))
    total_finished = len(records) - len(unfinished)

    with ProcessPoolExecutor() as executor:
        future_to_idx = {
            executor.submit(begin_arrange, i, springs, groups): i
            for i, (springs, groups)
            in enumerate(records)
            if i in unfinished
        }
        for future in as_completed(future_to_idx):
            total_finished += 1
            idx = future_to_idx[future]
            try:
                num_arrangements = future.result()
            except Exception as exc:
                print('%r generated an exception: %s' % (idx, exc))
            else:
                total_arrangements += num_arrangements
                if debug:
                    springs, groups = records[idx]
                    print(f'r#{idx:04}:', springs)
                    print('  groups', groups)
                    print('  num arrangements:', num_arrangements, 'total now', total_arrangements)
                    print('  progress:', f'{math.floor(total_finished / len(records) * 100)}%',
                          f'({len(records)-total_finished} remaining)')

    if debug:
        print()
        print('total possible arrangements:', total_arrangements)
        print('time:', time.time() - start)
    return total_arrangements


def begin_arrange(idx, springs, groups):
    if debug:
        print(f'start r#{idx:04}')
    arrangement = [-1] * (len(groups)*2 + 1)
    return arrange(arrangement, springs, groups)


def arrange(arrangement, springs, groups, indent=4):
    # print(show_arrangement(arrangement), file=sys.stderr)
    gs = groups[0]
    ge = groups[-1]

    if min(arrangement) >= 0:
        return 0

    first_unset = arrangement.index(-1)
    last_unset = len(arrangement) - 1 - arrangement[::-1].index(-1)
    # print(' '*indent + 'arrange', last_unset - first_unset + 1, show_arrangement(arrangement), 'of', groups)

    gaps = len(groups) + 1
    min_p_len = sum(groups) + gaps
    if first_unset == 0:
        # no outer gaps needed
        min_p_len -= 2
        min_outside_space = 0
    else:
        min_outside_space = 1

    is_last = len(groups) <= 2
    is_single = len(groups) == 1

    used_before = sum(arrangement[:first_unset])
    used_after = sum(arrangement[last_unset + 1:])
    remaining_springs = springs[used_before:len(springs)-used_after]
    free_len = len(remaining_springs) - min_p_len
    # print(' '*indent + 'rs', remaining_springs, 'flen', free_len, 'minos', min_outside_space)
    if free_len < 0:
        # print(' '*indent + 'no 0, flen', free_len)
        return 0

    num_arrangements = 0
    if len(groups) > 2:
        inner_groups = groups[1:-1]
    else:
        inner_groups = None

    for s in range(min_outside_space, min_outside_space + free_len + 1):
        if 0 <= remaining_springs.find('#') < s:
            break
        test_s = '_' * s + '#' * gs
        if not re.match(remaining_springs[:len(test_s)], test_s):
            continue

        for e in range(min_outside_space, (min_outside_space + free_len + 1) - (s-min_outside_space)):
            if remaining_springs.rfind('#', len(remaining_springs)-e) >= 0:
                break
            test_e = '#' * ge + '_' * e

            if re.match(remaining_springs[-len(test_e):], test_e):
                if is_last:
                    if is_single and s + gs + e < len(remaining_springs):
                        # print(' '*indent + '=> no 1')
                        continue
                    elif remaining_springs.find('#', len(test_s), len(remaining_springs)-len(test_e)) >= 0:
                        # print(' '*indent + '=> no 2')
                        continue

                if is_single:  # (s, gs, e)
                    # arrangement[first_unset] = s
                    # arrangement[first_unset+1] = gs
                    # arrangement[last_unset] = e
                    # print(' '*indent + 'found single', (s, gs, e), num_arrangements + 1, show_arrangement(arrangement))
                    # arrangement[first_unset:last_unset+1] = -1
                    num_arrangements += 1
                elif is_last:  # (s, gs, len(remaining), ge, e)
                    # arrangement[first_unset] = s
                    # arrangement[first_unset+1] = gs
                    # arrangement[first_unset+2] = len(remaining)
                    # arrangement[last_unset-1] = gs
                    # arrangement[last_unset] = e
                    # print(' '*indent + 'found last', (s, gs, len(remaining), gs, e), num_arrangements + 1, show_arrangement(arrangement))
                    # arrangement[first_unset:last_unset+1] = -1
                    num_arrangements += 1
                elif inner_groups is None:  # (s, gs, ge, e)
                    num_arrangements += 1
                else:  # (s, gs, (subpattern), ge, e)
                    arrangement[first_unset] = s
                    arrangement[first_unset+1] = gs
                    arrangement[last_unset-1] = ge
                    arrangement[last_unset] = e
                    # print(' '*indent + 'potential match, checking inner groups')
                    num_arrangements += arrange(arrangement, springs, inner_groups, indent + 4)
                    arrangement[first_unset] = -1
                    arrangement[first_unset+1] = -1
                    arrangement[last_unset-1] = -1
                    arrangement[last_unset] = -1
            # else:
                # print(' '*indent + '=> no 3', test_s, remaining_springs[:len(test_s)], '*', test_e, remaining_springs[-len(test_e):], 'slen', len(remaining_springs))
    # print(' '*indent + 'arrange complete', num_arrangements)
    return num_arrangements


def show_arrangement(arrangement, width=0):
    def char(i, g):
        if i % 2 == 0:
            return '_' * g
        return '#' * g

    middle = len(arrangement) // 2
    start = ''.join([char(i, g) for i, g in enumerate(arrangement[:middle])])
    end = ''.join(reversed([char(i, g) for i, g in enumerate(reversed(arrangement[middle:]))]))
    if min(arrangement) < 0 and width > 0:
        return start + ' ' * (width - len(start) - len(end)) + end
    elif len(arrangement) % 2 == 0 or min(arrangement) < 0:
        return start + '|' + end
    else:
        return start + end


def main():
    _input_file = 'input'

    run(__file__, solve, _input_file, 7007, expand=0)
    run(__file__, solve, _input_file, 2113581, expand=3, record_range=(0, 201))


if __name__ == '__main__':
    main()
