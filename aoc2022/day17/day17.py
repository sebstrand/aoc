from aocl import *


def solve(input_file, num_rocks):
    lines = read_lines(input_file)

    jets = list(c for c in lines[0])

    states = dict()
    room = Room()
    next_rock = 0
    next_jet = 0
    offset = 0
    i = 0
    while i < num_rocks:
        next_rock, next_jet = drop_rock(room, jets, next_rock, next_jet)

        if offset == 0:
            state_key = next_rock, next_jet
            state = states.get(state_key)

            if state is not None:
                previous_top, previous_diff, previous_i = state
                diff_now = room.top - previous_top
                if diff_now == previous_diff:
                    cycle_length = i - previous_i
                    remaining_rocks = num_rocks - i - 1
                    cycles = remaining_rocks // cycle_length
                    offset = cycles * diff_now
                    i = num_rocks - (remaining_rocks % cycle_length)
                    continue
            else:
                diff_now = -1
            states[state_key] = room.top, diff_now, i
        i += 1

    return room.top + offset


class Rock:
    def __init__(self, shape):
        lines = shape.split('\n')
        self.id = lines.pop(0)

        d = dict()
        for row, line in enumerate(reversed(lines)):
            for col, char in enumerate(line):
                if char == '#':
                    d[(row, col)] = True
        self.d = d

        self._width = max(abs(int(c)) for _, c in d.keys()) + 1
        self._height = max(abs(int(r)) for r, _ in d.keys()) + 1

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def at(self, x, y):
        return {(row + y, col + x): True for (row, col) in self.d.keys()}

    def collides(self, room, x, y):
        if x < 0: return True
        if x > room.width - self._width: return True
        if y < 0: return True

        d = self.at(x=x, y=y)
        return any(room.has(pos) for pos in d)

    def __repr__(self):
        return f'Rock({self.id}, {self.width}, {self.height})'


class Room:
    def __init__(self, width=7):
        self.top = 0
        self.d = dict()
        self._width = width

    @property
    def width(self):
        return self._width

    def has(self, pos):
        return pos in self.d

    def put(self, rock, x, y):
        rock_dict = rock.at(x=x, y=y)
        self.d.update(rock_dict)
        self.top = max(self.top, y + rock.height)

    def __repr__(self):
        return f'Room({self.d})'


def drop_rock(room, jets, next_rock, next_jet):
    rock = rocks[next_rock]
    x = 2
    y = room.top + 3
    while y >= 0:
        jet = jets[next_jet]
        if jet == '<' and not rock.collides(room, x=x-1, y=y):
            x -= 1
        elif jet == '>' and not rock.collides(room, x=x+1, y=y):
            x += 1
        next_jet = (next_jet + 1) % len(jets)

        if rock.collides(room, x, y - 1):
            room.put(rock, x, y)
            break
        else:
            y -= 1
    else:
        room.put(rock, x, y)

    return (next_rock + 1) % len(rocks), next_jet


rocks = list(map(Rock, '''
-
####

+
.#.
###
.#.

_|
..#
..#
###

|
#
#
#
#

#
##
##
'''.strip().split('\n\n')))


def main():
    _input_file = 'input'
    expected = {
        'input': (3109, 1541449275365),
        'example': (3068, 1514285714288),
    }[_input_file]

    run(__file__, solve, _input_file, expected[0], num_rocks=2022)
    run(__file__, solve, _input_file, expected[1], num_rocks=1000000000000)


if __name__ == '__main__':
    main()
