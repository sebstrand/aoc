import itertools
import numpy as np
import re
import requests
import time
import tomllib
import traceback

from PIL import Image, ImageShow
from collections import namedtuple
from functools import reduce
from heapq import heappush, heappop
from pathlib import Path
from datetime import datetime


digit_names = ('zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine')
p2d = namedtuple('point2d', ['y', 'x'])
p3d = namedtuple('point3d', ['y', 'x', 'z'])

_labeline_n_re = re.compile(r'([^\d]*?) *(\d+):\s*(.*)')
_labeline_re = re.compile(r'([^:]*):\s*(.*)')
_labeline_type = namedtuple('labeline', ['label', 'number', 'content'])


def run(puzzle, f, input_file, expected_answer, *args, **kwargs):
    puzzle_path = Path(puzzle).parent
    year, day = ints(puzzle_path.as_posix())[-2:]
    input_dir = puzzle_path.joinpath(f'../../input/{year}/{day:02d}')
    _fetch_puzzle_input(input_dir)

    input_file = input_dir.joinpath(input_file)
    print(f'\nRunning ({datetime.now()})', puzzle_path)
    print(f'  Input = "{input_file.relative_to(puzzle_path)}"')
    print('  Args =', args, kwargs)
    start = time.time()
    try:
        answer = f(input_file, *args, **kwargs)
        if answer == expected_answer:
            print('Answer:', _format_answer(answer))
        else:
            print('==== WRONG ANSWER ====')
            print('  Expected:', _format_answer(expected_answer))
            if answer is None or expected_answer is None:
                print('    Actual:', _format_answer(answer))
            else:
                print('    Actual:', _format_answer(answer), ('(too big)', '(too small)')[answer < expected_answer])
    except KeyboardInterrupt:
        print('Canceled by user')
    except Exception as e:
        print('Failed with', e.__class__.__name__)
        traceback.print_exception(e)

    time_taken = time.time() - start
    print('Time taken:', f'{time_taken:.04}s')


def _format_answer(answer):
    output = f'{answer}'
    if '\n' in output:
        return '\n' + output
    return output


def _fetch_puzzle_input(input_dir):
    year, day = ints(input_dir.as_posix())[-2:]
    input_file = input_dir.joinpath('input')
    if not input_file.exists():
        conf = _read_aoc_config()
        cookies = {'session': conf.get('session_cookie')}
        headers = {'User-Agent': 'AoC runner by github.com/sebstrand'}
        print(f'Fetching puzzle input for {year}/{day}...', end=' ', flush=True)
        r = requests.get(f'https://adventofcode.com/{year}/day/{day}/input',
                         cookies=cookies, headers=headers)
        with open(input_file.as_posix(), 'wb') as f:
            f.write(r.content)
        print('done!')
    return input_file


def _read_aoc_config():
    p = Path('~/.config/aoc.toml').expanduser()
    with open(p.as_posix(), 'rb') as f:
        config = tomllib.load(f)
    return config


def read_lines(filename, strip='a', skip_empty=True):
    """Read lines from a file.

    Keyword arguments:
    strip -- what whitespace to strip; 'l' for left, 'r', for right, 'a'/True for both or False/None for none
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


def labeline(line: str, numbered=True):
    """Parses a line that consists of a label with content into a named tuple.

    >>> labeline( "Item 42: some content" )
    labeline(label='Item', number=42, content='some content')

    >>> labeline( "Label: some content", numbered=False )
    labeline(label='Label', number=None, content='some content')
    """
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


def ints(s, sep=(r'[^\d-]+',)):
    """Convenience function which uses splits to find all integers in a string. By default accepts any separator that
    isn't a digit or a dash.

    >>> ints( '1,-5  6:7')
    [1, -5, 6, 7]
    """
    return splits(s, sep, int)


def splits(s: str, sep=(r' ',), f=None):
    """Uses sep to split s into parts using the separator(s) in sep. If multiple separators are specified then each
    part is split using the second separator, and then each of those parts using the third separator, and so on. A
    transform function f can be specified which is used to transform the final parts.

    >>> splits('a b c')
    ['a', 'b', 'c']

    >>> splits('1,2,3', sep=(',',), f=int)
    [1, 2, 3]

    >>> splits('a:1,  b:2,    c:3', sep=(r', *',':'))
    [['a', '1'], ['b', '2'], ['c', '3']]
    """
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
    """Finds the factors of a number.

    >>> factors(32)
    {32, 1, 2, 4, 8, 16}

    >>> factors(7)
    {1, 7}
    """
    return set(reduce(list.__add__,
                      ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))


def prime_factors(n):
    """Finds the prime factors of a number.

    >>> prime_factors(32)
    [2, 2, 2, 2, 2]

    >>> prime_factors(33)
    [3, 11]
    """
    p_factors = []
    divisor = 2

    while n > 1:
        while n % divisor == 0:
            p_factors.append(divisor)
            n //= divisor
        divisor += 1

    return p_factors


def neighbors_2d(grid, pos, named=False, valid_only=False):
    """Returns neighbor positions and values in a grid. When not using named position they are returned as a list using
    the order nswe, named positions are a dictionary with the keys nswe.

    >>> neighbors_2d([[1,2,3],[4,5,6],[7,8,9]], (1,1))
    [((0, 1), 2), ((2, 1), 8), ((1, 0), 4), ((1, 2), 6)]

    >>> neighbors_2d([[1,2,3],[4,5,6],[7,8,9]], (0,0), valid_only=True)
    [((1, 0), 4), ((0, 1), 2)]

    >>> neighbors_2d([[1,2,3],[4,5,6],[7,8,9]], (0,0), named=True, valid_only=True)
    {'s': ((1, 0), 4), 'e': ((0, 1), 2)}
    """
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
        if named:
            return {k: v for k, v in n.items() if v}
        else:
            return [x for x in n if x]
    else:
        return n


def visualize_grid(grid, filename, tile_map, bg_color=(0, 0, 0, 0), show=False):
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

    if show:
        ImageShow.show(image, filename)
    else:
        image.save(filename)


def contains_sublist(lst, sublist):
    """Checks if sublist is contained within lst.

    >>> contains_sublist(['a', 'b'], [])
    True
    >>> contains_sublist(['a', 'b'], ['a'])
    True
    >>> contains_sublist(['a', 'b'], ['a', 'b'])
    True
    >>> contains_sublist(['a', 'b'], ['a', 'b', 'c'])
    False
    """
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
    """Calculate the area of a polygon defined as a list of coordinates.

    >>> polygon_area([(0,0), (2,0), (0,2)])
    np.float64(2.0)
    """
    x = [x for x, _ in coordinates]
    y = [y for _, y in coordinates]
    return 0.5 * np.abs(
        + np.dot(x, np.roll(y, 1))
        - np.dot(y, np.roll(x, 1))
    )


def gridify(lines, convert, valid=None, default=-1, dtype=np.int32):
    """Creates a numpy 2D array from a list of iterables, running the values through a converter
    function and optionally checking if the value is in a collection first.

    >>> gridify(['123','456','789'], int)
    array([[1, 2, 3],
           [4, 5, 6],
           [7, 8, 9]], dtype=int32)
    >>> gridify([('1','2'),'..',['3','4']], lambda x: int(x)**2, default=99, valid='0123456')
    array([[ 1,  4],
           [99, 99],
           [ 9, 16]], dtype=int32)
    """
    rows, cols = len(lines), len(lines[0])
    grid = np.full((rows, cols), default, dtype=dtype)
    for r, line in enumerate(lines):
        for c, char in enumerate(line):
            if valid and char not in valid: continue
            grid[r, c] = convert(char)
    return grid


class PriorityQueue:
    def __init__(self, max_q=False):
        self.max_q = max_q
        self.pq = self.entries = None
        self.clear()

    def __len__(self):
        return len(self.entries)

    def add(self, priority, item):
        if item in self.entries:
            self.entries.pop(item)[-1] = ()
        if self.max_q:
            priority = -priority
        entry = [priority, item]
        self.entries[item] = entry
        heappush(self.pq, entry)

    def pop(self):
        while self.pq:
            priority, item = heappop(self.pq)
            if item != ():
                del self.entries[item]
                return item
        raise KeyError('priority queue is empty')

    def clear(self):
        self.pq = []
        self.entries = {}


class Terminal:
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    CLEAR = '\033[2J'
