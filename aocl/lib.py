import itertools
import numpy as np
import re
import requests
import time
import tomllib
import traceback

from PIL import Image
from collections import namedtuple
from functools import reduce
from pathlib import Path


digit_names = ('zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine')

_labeline_n_re = re.compile(r'([^\d]*?) *(\d+):\s*(.*)')
_labeline_re = re.compile(r'([^:]*):\s*(.*)')
_labeline_type = namedtuple('labeline', ['label', 'number', 'content'])


def run(puzzle, f, input_file, expected_answer, *args, **kwargs):
    puzzle_path = Path(puzzle).parent
    input_file = puzzle_path.joinpath(input_file)
    _fetch_puzzle_input(puzzle_path)
    print('\nRunning', puzzle_path)
    print(f'  Input = "{input_file.relative_to(puzzle_path)}"')
    print('  Args =', args, kwargs)
    start = time.time()
    try:
        answer = f(input_file, *args, **kwargs)
        if answer == expected_answer:
            print('Answer:', answer)
        else:
            print('==== WRONG ANSWER ====')
            print('  Expected:', expected_answer)
            if answer is None or expected_answer is None:
                print('    Actual:', answer)
            else:
                print('    Actual:', answer, ('(too big)', '(too small)')[answer < expected_answer])
    except KeyboardInterrupt:
        print('Canceled by user')
    except Exception as e:
        print('Failed with', e.__class__.__name__)
        traceback.print_exception(e)

    time_taken = time.time() - start
    print('Time taken:', f'{time_taken:.04}s')


def _fetch_puzzle_input(puzzle_path):
    year, day = ints(puzzle_path.as_posix())[-2:]
    input_file = puzzle_path.joinpath('input')
    if not input_file.exists():
        conf = _read_aoc_config()
        cookies = {'session': conf.get('session_cookie')}
        print(f'Fetching puzzle input for {year}/{day}...', end=' ', flush=True)
        r = requests.get(f'https://adventofcode.com/{year}/day/{day}/input', cookies=cookies)
        with open(input_file.as_posix(), 'wb') as f:
            f.write(r.content)
        print('done!')


def _read_aoc_config():
    p = Path('~/.config/aoc.toml').expanduser()
    with open(p.as_posix(), 'rb') as f:
        config = tomllib.load(f)
    return config


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


def ints(s, sep=(r'\D+',)):
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


def neighbors_2d(grid, pos, named=False, valid_only=False):
    r, c = pos

    if named:
        n0, n1, n2, n3 = 'n', 's', 'w', 'e'
        n = {n0: None, n1: None, n2: None, n3: None}
    else:
        n0, n1, n2, n3 = 0, 1, 2, 3
        n = [None, None, None, None]

    if r > 0:
        n[n0] = ((r-1, c), grid[r-1][c])
    if r < len(grid) - 1:
        n[n1] = ((r+1, c), grid[r+1][c])
    if c > 0:
        n[n2] = ((r, c-1), grid[r][c-1])
    if c < len(grid[0]) - 1:
        n[n3] = ((r, c+1), grid[r][c+1])

    if valid_only:
        return [x for x in n if x]
    else:
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


def contains_sublist(lst, sublist):
    if len(sublist) == 0:
        return True
    elif len(lst) == len(sublist):
        return lst == sublist
    elif len(sublist) > len(lst):
        return False
    else:
        for i in range(len(lst)):
            if lst[i] == sublist[0] and lst[i:i + len(sublist)] == sublist:
                return True
    return False


def polygon_area(coordinates):
    x = [x for x, _ in coordinates]
    y = [y for _, y in coordinates]
    return 0.5 * np.abs(
        + np.dot(x, np.roll(y, 1))
        - np.dot(y, np.roll(x, 1))
    )
