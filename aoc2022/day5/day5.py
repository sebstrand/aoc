from aocl import *
from collections import defaultdict, deque


def main():
    lines = read_lines('input', skip_empty=False, strip='r')

    stacks = defaultdict(deque)
    moves = []
    multi_move = True

    for line in lines:
        if line.startswith('move'):
            moves.append([int(s) for s in splits(line) if s.isnumeric()])
        elif '[' in line:
            for stack_i in range(len(line)//4 + 1):
                crate_id = line[1 + stack_i*4]
                if crate_id != ' ':
                    stacks[stack_i + 1].append(crate_id)

    for n, from_stack, to_stack in moves:
        if multi_move:
            crate_ids = [stacks[from_stack].popleft() for _ in range(n)]
            crate_ids.reverse()
            stacks[to_stack].extendleft(crate_ids)
        else:
            for i in range(n):
                crate_id = stacks[from_stack].popleft()
                stacks[to_stack].appendleft(crate_id)

    n_stacks = len(stacks)
    top_crates = ''.join([stacks[i][0] for i in range(1, n_stacks+1)])
    print('top crates:', top_crates)
    if multi_move:
        assert top_crates == 'LVMRWSSPZ'
    else:
        assert top_crates == 'JCMHLVGMG'


if __name__ == '__main__':
    main()