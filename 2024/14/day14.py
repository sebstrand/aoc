from collections import defaultdict
from dataclasses import dataclass
from aocl import *


# The elusive p2 christmas tree:
# 1111111111111111111111111111111
# 1.............................1
# 1.............................1
# 1.............................1
# 1.............................1
# 1..............1..............1
# 1.............111.............1
# 1............11111............1
# 1...........1111111...........1
# 1..........111111111..........1
# 1............11111............1
# 1...........1111111...........1
# 1..........111111111..........1
# 1.........11111111111.........1
# 1........1111111111111........1
# 1..........111111111..........1
# 1.........11111111111.........1
# 1........1111111111111........1
# 1.......111111111111111.......1
# 1......11111111111111111......1
# 1........1111111111111........1
# 1.......111111111111111.......1
# 1......11111111111111111......1
# 1.....1111111111111111111.....1
# 1....111111111111111111111....1
# 1.............111.............1
# 1.............111.............1
# 1.............111.............1
# 1.............................1
# 1.............................1
# 1.............................1
# 1.............................1
# 1111111111111111111111111111111


animate = False


def solve(input_file, room_size, p1=True):
    lines = read_lines(input_file)

    robots = []
    for x, y, vx, vy in (ints(line) for line in lines):
        robots.append(Robot(x, y, vx, vy))

    if p1:
        for robot in robots:
            robot.simulate(100, room_size)

        q_count = defaultdict(int)
        for robot in robots:
            q_count[robot.quadrant(room_size)] += 1
        return q_count[0] * q_count[1] * q_count[2] * q_count[3]
    elif animate:
        animate_movement(robots, room_size, 8149)
    else:
        t = 0
        while True:
            col_count = defaultdict(int)
            row_count = defaultdict(int)
            for robot in robots:
                robot.simulate(1, room_size)
                col_count[robot.x] += 1
                row_count[robot.y] += 1

            # Find first instance when there are 2+ rows and 2+ cols with 30+ robots
            t += 1
            if len(list(r for r in row_count.values() if r >= 30)) >= 2:
                if len(list(r for r in col_count.values() if r >= 30)) >= 2:
                    # show(robots, room_size, middle=True)
                    return t


def animate_movement(robots, room_size, target_time):
    import time
    t = 0
    start = target_time - 1
    for robot in robots:
        robot.simulate(start, room_size)
    while t < 2:
        for robot in robots:
            robot.simulate(0.01, room_size)
        t += 0.01
        show(robots, room_size, middle=True)
        time.sleep(max(0.02, 0.2 - abs(8149 - (start + t))))


def show(robots, room_size, middle=False):
    counts = defaultdict(int)
    for r in robots:
        counts[round(r.x), round(r.y)] += 1

    print(Terminal.CLEAR)
    for y in range(room_size[1]):
        print('   ', end='')
        for x in range(room_size[0]):
            count = counts[x, y]
            if not middle and (x == room_size[0] // 2 or y == room_size[1] // 2):
                s = ' '
            else:
                s = term_effect(str(count), Terminal.B_CYAN) if count > 0 else '.'
            print(s, end='')
        print()
    print()


@dataclass
class Robot:
    x: int
    y: int
    vx: int
    vy: int

    def simulate(self, sim_time, room_size):
        w, h = room_size[0], room_size[1]
        self.x = (self.x + self.vx * sim_time) % w
        self.y = (self.y + self.vy * sim_time) % h

    def quadrant(self, room_size):
        middle_x, middle_y = room_size[0] // 2, room_size[1] // 2
        if self.x == middle_x or self.y == middle_y:
            return -1
        elif self.y < middle_y:
            return 0 if self.x < middle_x else 1
        else:
            return 2 if self.x < middle_x else 3


def main():
    _input_file = 'input'
    expected = {
        'input': (214400550, 8149),
        'example': (12, None),
    }[_input_file]
    room_size = {
        'input': (101, 103),
        'example': (11, 7),
    }[_input_file]

    run(__file__, solve, _input_file, expected[0], room_size, p1=True)
    if _input_file == 'input':
        run(__file__, solve, _input_file, expected[1], room_size, p1=False)
    else:
        print('\nno p2 for example')


if __name__ == '__main__':
    main()
