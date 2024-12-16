from collections import defaultdict
from aocl import *


debug = False


def solve(input_file, p1=True):
    lines = read_lines(input_file)

    maze = {}
    start_pos = end_pos = None
    for r, line in enumerate(lines):
        for c, char in enumerate(line):
            pos = (r, c)
            if char == 'S':
                start_pos = pos
                char = '.'
            elif char == 'E':
                end_pos = pos
                char = '.'
            maze[pos] = (char == '.')

    heading = 'e'
    scores, prev = dijkstra(maze, start_pos, heading, end_pos)
    best_score = best_end_score(scores, end_pos)

    if p1:
        if debug:
            for h in 'nswe':
                if scores.get((end_pos, h)) == best_score:
                    show(maze, start_pos, end_pos, [ph for ph in get_path(prev, (end_pos, h))])
                    break  # only show one of potentially several equal length paths
        return best_score
    else:
        tiles_on_best_paths = set()
        for h in 'nswe':
            pos_and_heading = end_pos, h
            if scores.get(pos_and_heading) == best_score:
                tiles_on_best_paths.update(get_path_tiles(prev, pos_and_heading))
                if debug:
                    show(maze, start_pos, end_pos, [(pos, 'x') for pos in tiles_on_best_paths])
        return len(tiles_on_best_paths)


def dijkstra(maze, start_pos, heading, end_pos):
    scores = {(start_pos, heading): 0}
    prev = defaultdict(set)

    q = PriorityQueue()
    q.add(0, (start_pos, heading))
    visited = set()
    while len(q) > 0:
        pos, heading = q.pop()
        if pos == end_pos:
            break

        for i in range(4):
            n_heading = rotate90(heading, i)
            n_pos = move(pos, n_heading)
            if not maze.get(n_pos) or (n_pos, n_heading) in visited:
                continue

            n_score = 1
            if i > 0:
                n_score += 2000 if i == 2 else 1000

            score_to_n = scores[pos, heading] + n_score
            old_score = scores.get((n_pos, n_heading), 2**64)
            if score_to_n <= old_score:
                scores[n_pos, n_heading] = score_to_n
                if score_to_n < old_score:
                    prev[n_pos, n_heading].clear()
                prev[n_pos, n_heading].add((pos, heading))
                q.add(score_to_n, (n_pos, n_heading))

    return scores, prev


def rotate90(heading, n):
    i = 'nesw'.index(heading)
    return 'nesw'[(i + n) % 4]


def move(pos, heading):
    match heading:
        case 'n':
            return pos[0] - 1, pos[1]
        case 's':
            return pos[0] + 1, pos[1]
        case 'w':
            return pos[0], pos[1] - 1
        case 'e':
            return pos[0], pos[1] + 1


def best_end_score(scores, end_pos):
    return min(scores.get((end_pos, h), 2**64) for h in 'nswe')


def get_path(prev, end_pos_and_heading):
    ph = end_pos_and_heading
    path = [ph]
    while True:
        p = prev.get(ph, None)
        if p is None: break
        ph = next(iter(p))
        path.append(ph)

    return path


def get_path_tiles(prev, end_pos_and_heading):
    tiles = set()
    tiles.add(end_pos_and_heading[0])

    for ph in prev.get(end_pos_and_heading, set()):
        tiles.update(get_path_tiles(prev, ph))

    return tiles


def show(maze, start_pos, end_pos, path=None):
    height = max(pos[0] for pos in maze.keys()) + 1
    width = max(pos[1] for pos in maze.keys()) + 1
    path_d = {pos: d for pos, d in path} if path else {}

    for r in range(height):
        for c in range(width):
            pos = (r, c)
            if pos in path_d:
                print(term_effect(dir_to_arrow(path_d.get(pos)), Terminal.B_CYAN), end='')
            elif pos == start_pos:
                print('S', end='')
            elif pos == end_pos:
                print('E', end='')
            else:
                print(term_effect(' ' if maze.get(pos) else BoxDraw.BLOCK['light'], Terminal.YELLOW), end='')
        print()
    print()


def dir_to_arrow(d):
    return {'n': '^', 's': 'v', 'e': '>', 'w': '<', 'x': 'O'}.get(d)


def main():
    _input_file = 'input'
    expected = {
        'input': (94436, 481),
        'example': (7036, 45),
        'example2': (11048, 64),
    }[_input_file]

    run(__file__, solve, _input_file, expected[0], p1=True)
    run(__file__, solve, _input_file, expected[1], p1=False)


if __name__ == '__main__':
    main()
