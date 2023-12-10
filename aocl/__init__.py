import re
import itertools
from collections import namedtuple
from functools import reduce
from PIL import Image


digit_names = ('zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine')

_labeline_n_re = re.compile(r'([^\d]*?) *(\d+):\s*(.*)')
_labeline_re = re.compile(r'([^:]*):\s*(.*)')
_labeline_type = namedtuple('labeline', ['label', 'number', 'content'])


def read_lines(filename, strip='a', skip_empty=True):
    """Read lines from a file.

    Keyword arguments:
    strip -- what whitespace to strip; 'l' for left, 'r', for right, True for both or False/None for none
    skip_empty -- if true empty lines (after strip applied) are not included in the output
    """
    with open(filename, 'rt') as f:
        if strip:
            if strip == 'l':
                def stripper(s): return s.lstrip()
            elif strip == 'r':
                def stripper(s): return s.rstrip()
            else:
                def stripper(s): return s.strip()
        else:
            def stripper(s): return s

        return [stripper(line) for line in f.readlines() if not skip_empty or stripper(line) != '']


def labeline(line, numbered=True):
    if numbered:
        m = _labeline_n_re.match(line)
        if m:
            return _labeline_type(
                label=m.group(1),
                number=int(m.group(2)),
                content=m.group(3),
            )
    else:
        m = _labeline_re.match(line)
        if m:
            return _labeline_type(
                label=m.group(1),
                number=None,
                content=m.group(2),
            )


def ints(s, sep=(r' ',)):
    return splits(s, sep, int)


def splits(s, sep=(r' ',), f=None):
    s = s.strip()
    single_sep = sep[0]
    if single_sep == ' ':
        single_sep = r'\s+'
    if f is None:
        def f(x): return x

    if len(sep) > 1:
        return [splits(x, sep[1:], f) for x in re.split(single_sep, s) if x != '']
    else:
        return [f(x) for x in re.split(single_sep, s) if x != '']


def visit(lst):
    return itertools.chain.from_iterable(lst)


def factors(n):
    return set(reduce(list.__add__,
                      ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))


def prime_factors(n):
    p_factors = []
    divisor = 2

    while n > 1:
        while n % divisor == 0:
            p_factors.append(divisor)
            n //= divisor
        divisor += 1

    return p_factors


def neighbors_2d(grid, pos):
    r, c = pos
    n = [None, None, None, None]

    if r > 0:
        n[0] = ((r-1, c), grid[r-1, c])
    if r < len(grid) - 1:
        n[1] = ((r+1, c), grid[r+1, c])
    if c > 0:
        n[2] = ((r, c-1), grid[r, c-1])
    if c < len(grid[0]) - 1:
        n[3] = ((r, c+1), grid[r, c+1])
    return n


def visualize_grid(grid, filename, tile_map, bg_color=(0, 0, 0, 0)):
    rows, cols = len(grid), len(grid[0])
    first_tile = tuple(tile_map.values())[0]
    tile_height, tile_width = len(first_tile), len(first_tile[0])
    image = Image.new('RGBA', (cols*tile_width, rows*tile_height), color=bg_color)

    for tile_id in tile_map:
        tile_data = tile_map[tile_id]
        tile = Image.new('RGBA', (tile_width, tile_height))
        for x in range(tile_width):
            for y in range(tile_height):
                color = tile_data[y][x]
                if color:
                    tile.putpixel((x, y), color)
                    tile.putpixel((x, y), color)
                    tile.putpixel((x, y), color)
        tile_map[tile_id] = tile

    for r in range(rows):
        for c in range(cols):
            grid_data = grid[r, c]
            if grid_data and grid_data in tile_map:
                tile = tile_map[grid_data]
                image.paste(tile, (c*tile_width, r*tile_height))

    image.save(filename)
