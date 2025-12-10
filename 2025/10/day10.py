from collections import defaultdict
from itertools import combinations
from aocl import *


def solve(input_file, p1=True):
    lines = read_lines(input_file)

    machines = []
    for line in lines:
        lights, *buttons, joltage = splits(line)
        lights = [(1 if l == '#' else 0) for l in lights[1:-1]]
        buttons = list(ints(b) for b in buttons)
        joltage = splits(joltage[1:-1], (',',))
        machines.append(Machine(lights, buttons, joltage))

    return sum(min_presses(m) for m in machines)


def min_presses(machine):
    best = None
    for buttons in machine.possible_button_combinations():
        if best is not None and len(buttons) >= best: continue
        counts = defaultdict(int)
        for button in buttons:
            for light in button:
                counts[light] += 1

        match = True
        for i, light in enumerate(machine.lights):
            if counts[i] % 2 != light:
                match = False
                break
        if match:
            best = len(buttons)
    return best


class Machine:
    def __init__(self, lights, buttons, joltage):
        self.lights = lights
        self.buttons = buttons
        self.joltage = joltage

    def possible_button_combinations(self):
        valid_combos = []
        lights = {i for i, l in enumerate(self.lights) if l == 1}
        for num_buttons in range(1, len(self.buttons) + 1):
            for buttons in combinations(self.buttons, num_buttons):
                affected_lights = set()
                for button in buttons:
                    for light in button:
                        affected_lights.add(light)
                if affected_lights.issuperset(lights):
                    # this button combo affects all the wanted lights (and maybe some unwanted)
                    valid_combos.append(buttons)
        return valid_combos


    def __repr__(self):
        joltage = ','.join(str(j) for j in self.joltage)
        return f'Machine<[{self.lights}] {self.buttons} {{{joltage}}}>'


def main():
    _input_file = 'input'
    expected = {
        'input': (441, None),
        'example': (7, None),
    }[_input_file]

    run(__file__, solve, _input_file, expected[0], p1=True)
    # run(__file__, solve, _input_file, expected[1], p1=False)


if __name__ == '__main__':
    main()
