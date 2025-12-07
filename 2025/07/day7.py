import functools
import numpy as np
from aocl import *


START = 1
SPLITTER = 2
BEAM = 3


def solve(input_file, p1=True):
    manifold = gridify(
        read_lines(input_file),
        convert=lambda x: '.S^'.index(x),
    )
    return count_splits(manifold) if p1 else count_timelines(manifold)


def count_splits(manifold):
    num_splits = 0
    beam_sources = list(zip(*np.nonzero(manifold == START)))
    while len(beam_sources) > 0:
        row, col = beam_sources.pop(0)
        if manifold[row, col] == BEAM: continue

        obstacles = np.nonzero(manifold[row + 1:, col])[0]
        if len(obstacles) > 0:
            obstacle_row = row + 1 + obstacles[0]
            manifold[row:obstacle_row, col] = BEAM

            if manifold[obstacle_row, col] == BEAM: continue

            num_splits += 1
            beam_sources.append((obstacle_row, col - 1))
            beam_sources.append((obstacle_row, col + 1))
        else:
            manifold[row:, col] = BEAM
    return num_splits


def count_timelines(manifold):
    row, col = next(zip(*np.nonzero(manifold == START)))
    return count_timelines_from(CacheIgnore(manifold), int(row), int(col))


@functools.cache
def count_timelines_from(manifold, row, col):
    obstacles = np.nonzero(manifold.param[row + 1:, col])[0]
    if len(obstacles) == 0:
        return 1

    obstacle_row = row + 1 + obstacles[0]
    left = count_timelines_from(manifold, int(obstacle_row), col - 1)
    right = count_timelines_from(manifold, int(obstacle_row), col + 1)
    return left + right


# Helper to make functools.cache ignore unhashable argument
class CacheIgnore:
    def __init__(self, param):
        self.param = param

    def __hash__(self):
        return hash(type(self))


def main():
    _input_file = 'input'
    expected = {
        'input': (1609, 12472142047197),
        'example': (21, 40),
    }[_input_file]

    run(__file__, solve, _input_file, expected[0], p1=True)
    run(__file__, solve, _input_file, expected[1], p1=False)


if __name__ == '__main__':
    main()
