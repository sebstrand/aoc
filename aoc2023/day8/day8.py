from aocl import *
from collections import defaultdict
import numpy as np


def solve(input_file, p1=True):
    lines = read_lines(input_file)

    directions = list(lines.pop(0))
    nodes = {}
    for line in lines:
        node, l, r = visit(splits(line, sep=(' = ', ', ')))
        nodes[node] = (l[1:], r[:-1])

    if p1:
        locations = [loc for loc in nodes.keys() if loc == 'AAA']
    else:
        locations = [loc for loc in nodes.keys() if loc.endswith('A')]

    # print('starts', len(locations), locations)
    steps = defaultdict(list)
    for location in locations:
        ends = set()
        step = 0
        while True:
            mod_step = step % len(directions)
            step += 1
            direction = 'LR'.index(directions[mod_step])
            location = nodes[location][direction]
            if (not p1 and location[-1] == 'Z') or (p1 and location == 'ZZZ'):
                end = (location, mod_step)
                if not end in ends:
                    ends.add(end)
                    steps[location].append(step)
                break

    return np.lcm.reduce(list(visit(steps.values())))


def main():
    real_input = True

    if real_input:
        run(__file__, solve, 'input', 17621, p1=True)
        run(__file__, solve, 'input', 20685524831999, p1=False)
    else:
        run(__file__, solve, 'example', 2, p1=True)
        run(__file__, solve, 'example2', 6, p1=True)
        run(__file__, solve, 'examplep2', 6, p1=False)


if __name__ == '__main__':
    main()
