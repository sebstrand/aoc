from aocl import *
from collections import defaultdict
import numpy as np


p2 = True


def main():
    lines = read_lines('input')

    directions = list(lines.pop(0))
    nodes = {}
    for line in lines:
        node, l, r = visit(splits(line, sep=(' = ', ', ')))
        nodes[node] = (l[1:], r[:-1])

    if p2:
        locations = [loc for loc in nodes.keys() if loc.endswith('A')]
    else:
        locations = [loc for loc in nodes.keys() if loc == 'AAA']

    print('start', len(locations), locations)
    steps = defaultdict(list)
    for location in locations:
        ends = set()
        step = 0
        while True:
            mod_step = step % len(directions)
            step += 1
            direction = 'LR'.index(directions[mod_step])
            location = nodes[location][direction]
            if (p2 and location[-1] == 'Z') or (not p2 and location == 'ZZZ'):
                end = (location, mod_step)
                if end in ends:
                    break
                else:
                    ends.add(end)
                    steps[location].append(step)

    print('steps', steps, list(visit(steps.values())))
    steps_required = np.lcm.reduce(list(visit(steps.values())))
    print('steps required:', steps_required)

    if p2:
        assert steps_required == 20685524831999
    else:
        assert steps_required == 17621


if __name__ == '__main__':
    main()
