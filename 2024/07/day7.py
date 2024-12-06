import operator
from itertools import repeat
from concurrent.futures import ProcessPoolExecutor
from aocl import *


def solve(input_file, p1=True):
    lines = read_lines(input_file)

    equations = list(ints(line) for line in lines)
    operators = [operator.add, operator.mul]
    if not p1:
        operators.append(concat)

    with ProcessPoolExecutor() as executor:
        results = executor.map(solvable, equations, repeat(operators))
        return sum(eq[0] for eq, result in zip(equations, results) if result)


def concat(a, b):
    match b:
        case n if n < 10:
            b_digits = 1
        case n if n < 100:
            b_digits = 2
        case n if n < 1000:
            b_digits = 3
        case _:
            assert False
    return a * 10**b_digits + b


def solvable(equation, operators):
    result, operands = equation[0], equation[1:]
    if len(operands) == 1:
        return result == operands[0]
    elif result < operands[0]:
        # All the operators increase the value, so result isn't possible
        return False
    else:
        for op in operators:
            value = op(operands[0], operands[1])
            if solvable([result, value] + equation[3:], operators):
                return True
    return False


def main():
    _input_file = 'input'
    expected = {
        'input': (932137732557, 661823605105500),
        'example': (3749, 11387),
    }[_input_file]

    run(__file__, solve, _input_file, expected[0], p1=True)
    run(__file__, solve, _input_file, expected[1], p1=False)


if __name__ == '__main__':
    main()
