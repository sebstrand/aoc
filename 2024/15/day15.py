import time
from collections import deque
from aocl import *


WALL = 1
ROBOT = 9

direction_by_move = {
    '^': -1j,
    'v': +1j,
    '<': -1,
    '>': +1,
}

visualize = False


def solve(input_file, wide=False):
    lines = read_lines(input_file, skip_empty=False)
    split = lines.index('')

    warehouse = {}
    robot_position = None
    boxes = []
    for y, line in enumerate(lines[:split]):
        for x, char in enumerate(line):
            real_x = 2*x if wide else x
            positions = [real_x + y * 1j]
            if wide:
                positions.append(positions[0] + 1)

            if char == '@':
                robot_position = positions[0]
            else:
                content = None
                if char == 'O':
                    content = Box(positions)
                    boxes.append(content)
                elif char == '#':
                    content = WALL
                if content is not None:
                    for position in positions:
                        warehouse[position] = content

    moves = deque(''.join(lines[split+1:]))

    move_robot(warehouse, boxes, moves, robot_position)
    return sum(box.gps() for box in boxes)


class Box:
    positions: list[complex]

    def __init__(self, positions):
        self.positions = positions

    def gps(self):
        pos = self.positions[0]
        return int(pos.imag * 100 + pos.real)

    def can_push(self, warehouse, direction):
        other = []
        for pos in self.positions:
            content = warehouse.get(pos + direction)
            if content == WALL:
                return False
            elif content == self:
                pass  # wide box moving left/right
            elif isinstance(content, Box):
                other.append(content)

        return all(box.can_push(warehouse, direction) for box in other)

    def push(self, warehouse, direction):
        # First clear old position...
        for pos in self.positions:
            del warehouse[pos]

        # ...then push other boxes that are in the way before updating new position
        for i, pos in enumerate(self.positions):
            new_pos = pos + direction
            content = warehouse.get(new_pos)
            if content != self and isinstance(content, Box):
                content.push(warehouse, direction)
            self.positions[i] = new_pos
            warehouse[new_pos] = self

    def __repr__(self):
        return f'Box({self.positions})'


def show(warehouse, boxes, robot_position, move, num_moves):
    width = int(max(p.real for p in warehouse.keys())) + 1
    height = int(max(p.imag for p in warehouse.keys())) + 1

    gps_sum = sum(box.gps() for box in boxes)

    print(Terminal.CLEAR)
    print(f' Move {move} / {num_moves} (GPS score: {gps_sum})')
    print(' ', box_char('lr') * width, sep='')
    print()

    for y in range(height):
        print(' ', end='')
        for x in range(width):
            pos = x + y * 1j
            char = ' '
            if pos == robot_position or warehouse.get(pos) == ROBOT:
                char = term_effect('@', Terminal.B_GREEN, Terminal.BOLD)
            elif warehouse.get(pos) == WALL:
                char = term_effect(BoxDraw.BLOCK['medium'], Terminal.BLUE)
            else:
                box = warehouse.get(pos)
                if box is not None:
                    if len(box.positions) == 1:
                        char = term_effect('O', Terminal.YELLOW)
                    else:
                        char = '[' if pos == box.positions[0] else ']'
                        char = term_effect(char, Terminal.YELLOW)
            print(char, end='')
        print()
    print()
    time.sleep(0.01)


def move_robot(warehouse, boxes, moves, robot_position):
    move = 0
    num_moves = len(moves)
    while len(moves) > 0:
        move += 1
        direction = direction_by_move[moves.popleft()]
        new_position = robot_position + direction
        content = warehouse.get(new_position)
        if content == WALL:
            continue
        elif content is None:
            robot_position = new_position
        elif content.can_push(warehouse, direction):
            content.push(warehouse, direction)
            robot_position = new_position
        if visualize:
            show(warehouse, boxes, robot_position, move, num_moves)
    if visualize:
        time.sleep(5)
    return robot_position


def main():
    _input_file = 'input'
    expected = {
        'input': (1527563, 1521635),
        'example': (10092, 9021),
    }[_input_file]

    run(__file__, solve, _input_file, expected[0], wide=False)
    run(__file__, solve, _input_file, expected[1], wide=True)


if __name__ == '__main__':
    main()
