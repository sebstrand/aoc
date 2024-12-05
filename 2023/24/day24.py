from aocl import *
import numpy as np


def solve(input_file, p1=True):
    lines = read_lines(input_file)
    hail = []
    for line in lines:
        nums = ints(line)
        hail.append(Hail(nums[:3], nums[3:]))
    
    if 'example' in input_file.name:
        il_min, il_max = (7, 27)
    else:
        il_min, il_max = (200000000000000, 400000000000000)
    print('intersect limit:', (il_min, il_max))

    valid_intersect = 0
    for i, h1 in enumerate(hail[:-1]):
        for h2 in hail[i+1:]:
            pos = path_intersection(h1, h2)
            if pos:
                x, y = pos
                if x <= h1.p1[0] and h1.v[0] > 0 or y <= h1.p1[1] and h1.v[1] > 0:
                    continue
                elif x >= h1.p1[0] and h1.v[0] < 0 or y >= h1.p1[1] and h1.v[1] < 0:
                    continue
                elif x <= h2.p1[0] and h2.v[0] > 0 or y <= h2.p1[1] and h2.v[1] > 0:
                    continue
                elif x >= h2.p1[0] and h2.v[0] < 0 or y >= h2.p1[1] and h2.v[1] < 0:
                    continue

                if il_min <= x <= il_max and il_min <= y <= il_max:
                    valid_intersect += 1

    return valid_intersect


def path_intersection(h1, h2):
    # https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection
    denom = h1.x_det * h2.y_det - h1.y_det * h2.x_det
    if denom == 0:
        return None
    px = (h1.xy_det * h2.x_det - h1.x_det * h2.xy_det) / denom
    py = (h1.xy_det * h2.y_det - h1.y_det * h2.xy_det) / denom
    return px, py


def distance_between_paths(h1, h2):
    # Find the unit vector perpendicular to both lines
    n = np.cross(h1.v, h2.v)
    n /= np.linalg.norm(n)

    return np.dot(n, h1.p - h2.p)


def path_intersection_wip(h1, h2):
    if h1 == h2:
        return h1.p

    print('pi', h1, h2)
    d = distance_between_paths(h1, h2)
    # if abs(d) > 1e-3:
    #     return None
    print('  d', d)
    return None
    # ax+t*axv = bx+s*bxv
    # ay+t*ayv = by+s*byv
    # az+t*azv = bz+s*bzv
    #
    # x = h1px + t*h1vx
    # y = h1py + t*h1vy
    # z = h1pz + t*h1vz

    # elif is_parallell(h1, h2):
    #     return None
    # return h1.p
    v = np.array([h1.v[:2], h2.v[:2]]).T
    p1 = np.array(h1.p)[:2]
    p2 = np.array(h2.p)[:2]
    print('v, p1, p2\n', v, p1, p2)
    # A = np.array([[4, 0], [4, -3]])
    # B = np.array([[6, 2], [10, 2]])
    try:
        t, s = np.linalg.solve(v, p1-p2)
        print('  x', h1.p[0] + t * h1.v[0] - (h2.p[0] + s * h2.v[0]))
        print('  y', h1.p[1] + t * h1.v[1] - (h2.p[1] + s * h2.v[1]))
        print('  z', h1.p[2] + t * h1.v[2] - (h2.p[2] + s * h2.v[2]))
    except np.linalg.LinAlgError as e:
        print('parallell', e)
    return None


class Hail:
    def __init__(self, p, v) -> None:
        p1 = self.p1 = p
        self.v = v
        p2 = self.p2 = [
            p[0] + v[0],
            p[1] + v[1],
            p[2] + v[2],
        ]

        self.x_det = p1[0] - p2[0]
        self.y_det = p1[1] - p2[1]
        self.xy_det = p1[0] * p2[1] - p1[1] * p2[0]

    def __str__(self) -> str:
        return f'Hail<{self.p1}, {self.v}>'


def main():
    _input_file = 'input'
    expected = {
        'input': (15558, None),
        'example': (2, None),
    }[_input_file]

    run(__file__, solve, _input_file, expected[0], p1=True)
    # run(__file__, solve, _input_file, expected[1], p1=False)


if __name__ == '__main__':
    main()
