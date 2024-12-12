from aocl import *
from dataclasses import dataclass


def solve(input_file, correction: int = 0):
    lines = read_lines(input_file)

    machines = []
    for a, b, prize in zip(lines[::3], lines[1::3], lines[2::3]):
        machines.append(Machine(ints(a), ints(b), tuple(p + correction for p in ints(prize))))

    return sum(machine.cost_to_win() for machine in machines)


@dataclass
class Machine:
    a_move: tuple[int, int]
    b_move: tuple[int, int]
    prize_loc: tuple[int, int]

    def cost_to_win(self):
        xa, ya = self.a_move
        xb, yb = self.b_move
        xp, yp = self.prize_loc

        b = (ya * xp / xa - yp) / (ya * xb / xa - yb)
        a = (xp - xb * b) / xa

        a = round(a)
        b = round(b)
        if a < 0 or b < 0 or a*xa + b*xb != xp or a*ya + b*yb != yp:
            # A negative or non-integer number of presses required
            return 0

        return a * 3 + b


def main():
    _input_file = 'input'
    expected = {
        'input': (31589, 98080815200063),
        'example': (480, 875318608908),
    }[_input_file]

    run(__file__, solve, _input_file, expected[0])
    run(__file__, solve, _input_file, expected[1], correction=10000000000000)


if __name__ == '__main__':
    main()
