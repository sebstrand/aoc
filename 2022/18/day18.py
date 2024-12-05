from collections import deque
from aocl import *


LAVA = 'L'
EXPOSED = 'X'
ENCLOSED = 'C'


def solve(input_file, p1=True):
    lines = read_lines(input_file)

    cubes = {}
    minimums = [2**31] * 3
    maximums = [-1] * 3

    for pos in map(ints, lines):
        cubes[tuple(pos)] = LAVA
        for d in range(3):
            minimums[d] = min(minimums[d], pos[d])
            maximums[d] = max(maximums[d], pos[d])

    if not p1:
        # Make sure there a layer of unoccupied cubes on the outside
        for d in range(3):
            minimums[d] -= 1
            maximums[d] += 1
        # Floodfill from the outside so that outside lava faces have neighbors marked as exposed
        floodfill(cubes, minimums, maximums)

    # Note: for p1 any unused position is exposed, p2 requires position to be explicitly marked as exposed
    return count_exposed_faces(cubes, default=EXPOSED if p1 else ENCLOSED)


def floodfill(cubes, minimums, maximums):
    q = deque()
    q.append((minimums[0], minimums[1], minimums[2]))

    while len(q):
        pos = q.popleft()
        if pos not in cubes:
            cubes[pos] = EXPOSED

        for d in range(3):
            head, tail = pos[:d], pos[d+1:]
            for d_pos in pos[d] - 1, pos[d] + 1:
                if minimums[d] <= d_pos <= maximums[d]:
                    n_pos = head + (d_pos,) + tail
                    if n_pos not in cubes:
                        q.appendleft(n_pos)


def count_exposed_faces(cubes: dict, default=EXPOSED):
    exposed_sides = 0
    for pos, content in (item for item in cubes.items() if item[1] == LAVA):
        for d in range(3):
            head, tail = pos[:d], pos[d+1:]
            for d_pos in pos[d] - 1, pos[d] + 1:
                if cubes.get(head + (d_pos,) + tail, default) == EXPOSED:
                    exposed_sides += 1
    return exposed_sides


def main():
    _input_file = 'input'
    expected = {
        'input': (4460, 2498),
        'example': (64, 58),
    }[_input_file]

    run(__file__, solve, _input_file, expected[0], p1=True)
    run(__file__, solve, _input_file, expected[1], p1=False)


if __name__ == '__main__':
    main()
