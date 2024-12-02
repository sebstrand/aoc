from collections import defaultdict, namedtuple
from aocl import *

robot = namedtuple('robot', ['ore', 'clay', 'obsidian'], defaults=(0, 0, 0))
start_minutes = 18


# Blueprint 2:
#   Each ore robot costs 2 ore.
#   Each clay robot costs 3 ore.
#   Each obsidian robot costs 3 ore and 8 clay.
#   Each geode robot costs 3 ore and 12 obsidian.

def solve(input_file, p1=True):
    lines = read_lines(input_file)
    blueprints = []
    for bid, oro, cro, bro, brc, gro, grb in map(ints, lines):
        blueprints.append((
            bid,
            {
                'geode': robot(ore=gro, clay=0, obsidian=grb),
                'obsidian': robot(ore=bro, clay=brc, obsidian=0),
                'clay': robot(ore=cro, clay=0, obsidian=0),
                'ore': robot(ore=oro, clay=0, obsidian=0),
            }
        ))
    print('\n'.join(str(b) for b in blueprints))

    return sum(map(evaluate, blueprints[1:]))


def debug(level, *msg):
    print(' ' * level, *msg)


def evaluate(blueprint, minutes=start_minutes) -> int:
    robots = defaultdict(int)
    robots['ore'] = 1
    resources = defaultdict(int)

    bid, robot_data = blueprint
    print('Evaluating', bid)
    return bid * evaluate_with_data(robot_data, start_minutes, robots, resources)


def evaluate_with_data(robot_data: dict, minutes: int, robots: defaultdict, resources: defaultdict, level=0) -> int:
    debug(level, f'Minute {start_minutes + 1 - minutes}')
    if minutes == 0:
        debug(level, 'outtatime')
        return 0

    buildable = list(ritem for ritem in robot_data.items() if can_afford(ritem[1], resources))

    updated_resources = resources.copy()
    for rid in robots.keys():
        updated_resources[rid] += 1
    debug(level, 'resources now', updated_resources)

    geodes = resources['geode']
    for rid, rcost in buildable:
        debug(level, 'trying', rid, 'build')
        resources_when_built = updated_resources.copy()
        spend(rcost, resources_when_built)
        new_robots = robots.copy()
        new_robots[rid] += 1
        remaining_geodes = evaluate_with_data(robot_data, minutes - 1, new_robots, resources_when_built, level + 2)
        debug(level, 'remaining geodes with', rid, '->', remaining_geodes)
        geodes = max(geodes, remaining_geodes)

    remaining_geodes = evaluate_with_data(robot_data, minutes - 1, robots, updated_resources, level + 2)
    debug(level, 'remaining geodes without build:', geodes)
    geodes = max(geodes, remaining_geodes)

    debug(level, 'best geodes', geodes)
    return geodes


def can_afford(cost, resources):
    return (resources['ore'] >= cost.ore and
            resources['clay'] >= cost.clay and
            resources['obsidian'] >= cost.obsidian)


def spend(cost, resources):
    resources['ore'] -= cost.ore
    resources['clay'] -= cost.clay
    resources['obsidian'] -= cost.obsidian
    assert resources['ore'] >= 0
    assert resources['clay'] >= 0
    assert resources['obsidian'] >= 0


def main():
    _input_file = 'example'
    expected = {
        'input': (None, None),
        'example': (33, None),
    }[_input_file]

    run(__file__, solve, _input_file, expected[0], p1=True)
    # run(__file__, solve, _input_file, expected[1], p1=False)


if __name__ == '__main__':
    main()
