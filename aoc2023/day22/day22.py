import sys
import numpy as np

from aocl import *
from collections import defaultdict, deque


def solve(input_file, p1=True):
    lines = read_lines(input_file)

    np.set_printoptions(threshold=sys.maxsize)
    cube_grid = np.zeros((400, 10, 10), dtype=np.int32)

    bricks = {}
    for i, line in enumerate(lines):
        numbers = ints(line)
        brick_num = len(bricks) + 1
        brick = Brick(brick_num, [tuple(numbers[:3]), tuple(numbers[3:])])
        bricks[brick_num] = brick
        for x, y, z in brick:
            cube_grid[z, y, x] = brick_num

    cube_grid[0, :, :] = -1
    drop(cube_grid, bricks)

    if p1:
        return find_safe_bricks(cube_grid, bricks)
    else:
        affected_bricks = {}
        for brick in bricks:
            affected_bricks[brick] = disintegrate(cube_grid, bricks, brick)
        return sum(affected_bricks.values())


def find_support_bricks(cube_grid, bricks):
    supported_by = defaultdict(set)
    supports = defaultdict(set)
    for brick in bricks.values():
        for x, y, z in brick:
            support = cube_grid[z-1, y, x]
            if support > 0 and support != brick.num:
                supported_by[brick.num].add(support)
                supports[support].add(brick.num)

    return supported_by, supports


def find_safe_bricks(cube_grid, bricks):
    supported_by, _ = find_support_bricks(cube_grid, bricks)

    needed_bricks = set(next(iter(s)) for b, s in supported_by.items() if len(s) == 1)
    safe_bricks = set(b.num for b in bricks.values() if b.num not in needed_bricks)
    return len(safe_bricks)


def disintegrate(cube_grid, bricks, removed_brick):
    supported_by, supports = find_support_bricks(cube_grid, bricks)
    bricks_to_remove = deque([removed_brick])
    falling = 0
    while len(bricks_to_remove) > 0:
        removed_brick = bricks_to_remove.popleft()

        supported_bricks = supports[removed_brick]
        supports[removed_brick] = set()
        for supported_brick in supported_bricks:
            supported_by[supported_brick].discard(removed_brick)
            if not bricks[supported_brick].is_on_ground() and len(supported_by[supported_brick]) == 0:
                bricks_to_remove.append(supported_brick)
                falling += 1

    return falling


def drop(cube_grid, bricks):
    changed = True
    brick_list = bricks.values()
    while changed:
        changed = False
        for brick in brick_list:
            positions = list(iter(brick))
            free_below = 9999
            for x, y, z in positions:
                support = np.flip(cube_grid[0:z, y, x])
                if support[0] == brick.num:
                    # Ignore self-support in vertical bricks
                    continue
                free_below = min(free_below, support.nonzero()[0][0])

            if free_below > 0:
                changed = True
                brick.move_down(free_below)
                for x, y, z in positions:
                    cube_grid[z, y, x] = 0
                    cube_grid[z-free_below, y, x] = brick.num


class Brick:
    def __init__(self, num, ends):
        self.num = num
        self.ends = ends

    def move_down(self, steps):
        # print('moving brick', self.num, 'down', steps, 'steps')
        (x1, y1, z1), (x2, y2, z2) = self.ends
        self.ends[0] = x1, y1, z1-steps
        self.ends[1] = x2, y2, z2-steps

    def is_on_ground(self):
        return self.ends[0][-1] == 1 or self.ends[1][-1] == 1

    def __iter__(self):
        (x1, y1, z1), (x2, y2, z2) = self.ends
        for z in range(z1, z1+(z2-z1)+1):
            for y in range(y1, y1+(y2-y1)+1):
                for x in range(x1, x1+(x2-x1)+1):
                    yield x, y, z


def main():
    _input_file = 'input'
    expected = {
        'input': (480, 84021),
        'example': (5, 7),
    }[_input_file]

    run(__file__, solve, _input_file, expected[0], p1=True)
    run(__file__, solve, _input_file, expected[1], p1=False)


if __name__ == '__main__':
    main()
