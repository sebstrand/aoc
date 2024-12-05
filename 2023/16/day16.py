from aocl import *

bounce = {
    '/':  ['e', 'w', 'n', 's'],
    '\\': ['w', 'e', 's', 'n'],

    '|':  ['n', 's', ('n', 's'), ('n', 's')],
    '-':  [('e', 'w'), ('e', 'w'), 'e', 'w'],
}


def main(input_file, find_max=False):
    grid = read_lines(input_file)
    rows, cols = len(grid), len(grid[0])

    starts = []
    if find_max:
        for r in range(rows):
            starts.append(((r, 0), 'e'))
            starts.append(((r, cols-1), 'w'))
        for c in range(cols):
            starts.append(((0, c), 's'))
            starts.append(((rows-1, c), 'n'))
    else:
        starts.append(((0, 0), 'e'))

    max_energized = 0
    for start_pos, start_dir in starts:
        energized = energize(grid, start_pos, start_dir)
        max_energized = max(max_energized, energized)

    return max_energized


def energize(grid, start_pos, start_direction):
    seen = set()
    energized = set()

    beams = [Beam(start_pos, start_direction)]
    changed = True
    step = 0
    while changed:
        changed = False
        step += 1
        for _, beam in enumerate(beams):
            if beam.direction is None or hash(beam) in seen:
                continue

            seen.add(hash(beam))
            energized.add(beam.pos)

            n = neighbors_2d(grid, beam.pos, named=True)
            br, bc = beam.pos
            tile = grid[br][bc]
            if tile in bounce:
                direction = bounce[tile][beam.direction_idx()]
                if len(direction) == 2:
                    direction, split_direction = direction

                    new_pos_and_tile = n[split_direction]
                    if new_pos_and_tile:
                        beams.append(Beam(new_pos_and_tile[0], split_direction))
                beam.direction = direction

            new_pos_and_tile = n[beam.direction]
            if new_pos_and_tile:
                beam.pos = new_pos_and_tile[0]
            else:
                beam.direction = None
            changed = True

    return len(energized)


class Beam:
    directions = ['n', 's', 'e', 'w']

    def __init__(self, pos, direction):
        self.pos = pos
        self.direction = direction

    def direction_idx(self):
        if self.direction:
            return Beam.directions.index(self.direction)
        return -1

    def __repr__(self):
        return f'B<{self.pos} {self.direction}>'

    def __hash__(self):
        return 7 * hash(self.pos) + hash(self.direction)


if __name__ == '__main__':
    _input_file = 'input'
    expected = {
        'input': (7074, 7530),
        'example': (46, 51),
    }[_input_file]

    run(__file__, main, _input_file, expected[0], find_max=False)
    run(__file__, main, _input_file, expected[1], find_max=True)
