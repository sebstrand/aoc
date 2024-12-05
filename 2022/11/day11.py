from aocl import *
from collections import deque
from functools import reduce
import operator


def solve(input_file, rounds):
    lines = deque(read_lines(input_file))

    monkeys = {}
    while len(lines) > 0:
        monkey = labeline(lines.popleft())
        monkeys[monkey.number] = {
            'items': deque(ints(labeline(lines.popleft(), numbered=False).content, sep=(r', ',))),
            'operation': splits(labeline(lines.popleft(), numbered=False).content[6:])[1:],
            'divisor': int(splits(labeline(lines.popleft(), numbered=False).content)[-1]),
            'target_true': int(splits(lines.popleft())[-1]),
            'target_false': int(splits(lines.popleft())[-1]),
            'inspections': 0,
        }

    # for i, m in enumerate(monkeys.values()):
    #     print(f'm{i}', m)

    divisor_product = reduce(operator.mul, (m['divisor'] for m in monkeys.values()))
    # print('divisor_product:', divisor_product)

    for rnd in range(rounds):
        for turn in range(len(monkeys)):
            monkey = monkeys[turn]
            items = monkey['items']
            while len(items):
                monkey['inspections'] += 1
                item = items.popleft()
                item = apply_op(monkey['operation'], item) % divisor_product
                if rounds <= 20:
                    item //= 3
                if item % monkey['divisor'] == 0:
                    target_monkey = monkey['target_true']
                else:
                    target_monkey = monkey['target_false']
                monkeys[target_monkey]['items'].append(item)

    inspections = [monkey['inspections'] for monkey in monkeys.values()]
    # print('inspections:', inspections)
    sorted_inspections = sorted(inspections, reverse=True)
    return sorted_inspections[0] * sorted_inspections[1]


def apply_op(operation, item):
    op, num = operation
    if num == 'old':
        num = item
    else:
        num = int(num)

    if op == '*':
        new_value = item * num
    elif op == '+':
        new_value = item + num
    else:
        assert False

    return new_value


def main():
    _input_file = 'input'
    expected = {
        'input': (78678, 15333249714),
        'example': (10605, 2713310158),
    }[_input_file]

    run(__file__, solve, _input_file, expected[0], rounds=20)
    run(__file__, solve, _input_file, expected[1], rounds=10000)


if __name__ == '__main__':
    main()
