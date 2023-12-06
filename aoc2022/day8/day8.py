import numpy as np
import sys
from aocl import *


def main():
    lines = read_lines('input')

    n_rows = len(lines)
    n_cols = len(lines[0])

    heights = np.zeros((n_rows, n_cols), dtype=np.int32)
    for i, line in enumerate(lines):
        for j, h in enumerate(int(t) for t in line):
            heights[i, j] = h

    print(heights)
    visible = n_cols*2 + n_rows*2 - 4

    heights_copy = heights.copy()
    print('\nchecking rows')
    visible += check_visible_by_row(heights_copy)
    # print(heights_copy)

    print('\nchecking cols')
    visible += check_visible_by_row(heights_copy.T)
    # print(heights_copy)

    print('visible:', visible)
    # assert visible == 1840

    view_dist_left = np.zeros_like(heights)
    view_dist_right = np.zeros_like(heights)
    view_dist_up = np.zeros_like(heights)
    view_dist_down = np.zeros_like(heights)

    check_view_dist(heights, view_dist_left, view_dist_right, view_dist_up, view_dist_down)
    print('\nvdu')
    print(view_dist_up)
    print('\nvdl')
    print(view_dist_left)
    print('\nvdr')
    print(view_dist_right)
    print('\nvdd')
    print(view_dist_down)

    print('\nscore')
    view_scores = view_dist_left * view_dist_right * view_dist_up * view_dist_down
    print(view_scores)
    max_score = view_scores.max()
    print('max score:', max_score)
    assert max_score == 405769


def check_visible_by_row(heights):
    visible = 0
    for i, axis1 in enumerate(heights[1:-1]):
        n_cols = len(axis1)
        max_h_on_axis = 0
        for j, height in enumerate(axis1):
            if height > 0 and 0 < j < n_cols - 1 and height > max_h_on_axis:
                visible += 1
                axis1[j] = -height
            max_h_on_axis = max(max_h_on_axis, abs(height))

        max_h_on_axis = 0
        for j, height in enumerate(axis1[::-1]):
            if height > 0 and 0 < j < n_cols - 1 and height > max_h_on_axis:
                visible += 1
                axis1[::-1][j] = -height
            max_h_on_axis = max(max_h_on_axis, abs(height))
    print('visible in check:', visible)
    return visible


def check_view_dist(heights, view_dist_left, view_dist_right, view_dist_up, view_dist_down):
    n_rows = np.size(heights, 0)
    n_cols = np.size(heights, 1)
    for y in range(n_rows):
        for x in range(n_cols):
            height = heights[y, x]

            view_dist_left  [y, x] = get_view_dist(heights, height, range(x-1,     -1, -1), range(y, y+1), x, y)
            view_dist_right [y, x] = get_view_dist(heights, height, range(x+1, n_cols,  1), range(y, y+1), x, y)

            view_dist_up    [y, x] = get_view_dist(heights, height, range(x, x+1), range(y-1,     -1, -1), x, y)
            view_dist_down  [y, x] = get_view_dist(heights, height, range(x, x+1), range(y+1, n_rows,  1), x, y)


def get_view_dist(heights, tree_height, range_x, range_y, x, y):
    last_x = None
    last_y = None
    for ty in range_y:
        last_y = ty
        for tx in range_x:
            last_x = tx
            if heights[ty, tx] >= tree_height:
                return abs(x - tx) + abs(y - ty)

    if last_x is None or last_y is None:
        return 0
    else:
        return abs(x - last_x) + abs(y - last_y)


if __name__ == '__main__':
    main()
