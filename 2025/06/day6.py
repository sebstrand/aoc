from functools import reduce
from aocl import *


def solve(input_file, p1=True):
    lines = read_lines(input_file, strip=False)
    operators = splits(lines[-1])

    grand_total = 0
    if p1:
        numbers = [ints(line) for line in lines[:-1]]
        for problem, operator in enumerate(operators):
            grand_total += reduce(lambda a, b: apply(operator, a, b), (row[problem] for row in numbers))
    else:
        numbers = []
        for vslice in vslices(lines[:-1]):
            if vslice:
                numbers.append(int(vslice))
            else:  # empty column separates problems
                operator = operators.pop(0)
                grand_total += reduce(lambda a, b: apply(operator, a, b), numbers)
                numbers = []
    return grand_total


def apply(operator, op1, op2):
    match operator:
        case '+':
            return op1 + op2
        case '*':
            return op1 * op2
    assert False


def vslices(lines):
    n = len(lines[0])
    for i in range(n):
        yield ''.join([line[i] for line in lines]).strip()


def main():
    _input_file = 'example'
    expected = {
        'input': (5877594983578, 11159825706149),
        'example': (4277556, 3263827),
    }[_input_file]

    run(__file__, solve, _input_file, expected[0], p1=True)
    run(__file__, solve, _input_file, expected[1], p1=False)


if __name__ == '__main__':
    main()
