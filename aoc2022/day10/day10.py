from aocl import *
from collections import defaultdict, deque


def main():
    lines = read_lines('input')

    instructions = deque()
    for line in lines:
        parts = splits(line)
        command = parts[0]
        args = [int(x) for x in parts[1:]]
        instructions.append((command, args))

    display = [
        ['.'] * 40,
        ['.'] * 40,
        ['.'] * 40,
        ['.'] * 40,
        ['.'] * 40,
        ['.'] * 40,
    ]

    cpu = Cpu(instructions, display, trace=False)
    signal_strength_sum = 0
    while True:
        registers = cpu.tick()
        if registers is None:
            show_display(display)
            break
        elif cpu.cycle >= 20 and (cpu.cycle - 20) % 40 == 0:
            signal_strength = cpu.cycle * registers['x']
            print('cycle', cpu.cycle)
            print('  signal strength:', signal_strength, f'(reg x={registers["x"]})')
            signal_strength_sum += signal_strength

    print()
    print('signal strength sum:', signal_strength_sum)
    assert signal_strength_sum == 13140

    # display should read EHPZPJGL


def show_display(display):
    print()
    for row in display:
        print(''.join(row))


class Cpu:
    def __init__(self, instructions, display, trace=False):
        self.instructions = instructions
        self.display = display
        self.display_size = (len(display), len(display[0]))
        self.cur_pixel = 0
        self.trace = trace

        registers = defaultdict(int)
        registers['x'] = 1
        self.registers = registers
        self.cycle = 0
        self.in_progress = None
        print('Cpu initialized with', len(instructions), 'instructions', instructions)

    def tick(self):
        self.cycle += 1
        if self.trace:
            print('begin cycle', self.cycle)

        if self.in_progress or len(self.instructions):
            self.draw()
        register_copy = self.registers.copy()

        if self.in_progress:
            self.in_progress[0] -= 1
            if self.in_progress[0] == 0:
                self.execute(self.in_progress[1])
                self.in_progress = None
            else:
                if self.trace:
                    print('(busy)')
        elif len(self.instructions):
            command, args = self.instructions.popleft()

            if command == 'noop':
                if self.trace:
                    print('noop')
            elif command.startswith('add'):
                self.in_progress = [1, (command, args)]
                if self.trace:
                    print('begin', command)
        else:
            if self.trace:
                print('exit')
            return None

        if self.trace:
            print('end cycle', self.cycle, 'registers', self.registers)
            print()
        return register_copy

    def draw(self):
        if not self.display:
            return

        rows, cols = self.display_size
        x = self.cur_pixel % cols
        y = (self.cur_pixel // cols) % rows
        sprite_left = max(0, self.registers['x'] - 1)
        sprite_right = min(cols-1, self.registers['x'] + 1)
        if sprite_left <= x <= sprite_right:
            pixel = '#'
        else:
            pixel = '.'
        self.display[y][x] = pixel
        self.cur_pixel += 1

    def execute(self, instruction):
        command, args = instruction
        if self.trace:
            print('executing command', command)

        if command == 'noop':
            pass
        elif command.startswith('add'):
            assert len(args) == 1
            register = command[3:4]
            self.registers[register] += args[0]


if __name__ == '__main__':
    main()
