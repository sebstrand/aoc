import re
import itertools
from collections import namedtuple, Counter
from functools import reduce


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
