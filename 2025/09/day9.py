from aocl import *


RED = 1
GREEN = 2


def solve(input_file, p1=True):
    lines = read_lines(input_file)

    red = list(p2d(y, x) for x, y in (ints(line) for line in lines))

    vertical = {}
    horizontal = {}
    if not p1:
        for c1, c2 in zip(red, red[1:] + [red[0]]):
            if c1.x == c2.x:
                vertical.setdefault(c1.x, []).append((min(c1.y, c2.y), max(c1.y, c2.y)))
            else:
                horizontal.setdefault(c1.y, []).append((min(c1.x, c2.x), max(c1.x, c2.x)))

    max_area = 0
    for i, c1 in enumerate(red):
        for c2 in red[i+1:]:
            x1, x2 = min(c1.x, c2.x), max(c1.x, c2.x)
            y1, y2 = min(c1.y, c2.y), max(c1.y, c2.y)

            area = ((x2 - x1) + 1) * ((y2 - y1) + 1)
            if area > max_area:
                if not p1:
                    if line_inside(vertical, x1, x2, y1, y2):
                        continue
                    elif line_inside(horizontal, y1, y2, x1, x2):
                        continue
                max_area = area
    return max_area


def line_inside(lines, p1, p2, c1, c2):
    for p in (p for p in lines.keys() if p1 < p < p2):
        for start, end in lines[p]:
            if start < c2 and end > c1:
                return True
    return False


def main():
    _input_file = 'input'
    expected = {
        'input': (4763932976, 1501292304),
        'example': (50, 24),
    }[_input_file]

    run(__file__, solve, _input_file, expected[0], p1=True)
    run(__file__, solve, _input_file, expected[1], p1=False)


if __name__ == '__main__':
    main()
