from aocl import *
from collections import deque
from functools import reduce
import operator


def main():
    lines = deque(read_lines('input'))

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

    for i, m in enumerate(monkeys.values()):
        print(f'm{i}', m)

    divisor_product = reduce(operator.mul, (m['divisor'] for m in monkeys.values()))
    print('divisor_product:', divisor_product)

    p1 = False
    if p1:
        rounds = 20
    else:
        rounds = 10000

    for rnd in range(rounds):
        if rnd % 1000 == 0:
            print('round', rnd)
        for turn in range(len(monkeys)):
            monkey = monkeys[turn]
            items = monkey['items']
            while len(items):
                monkey['inspections'] += 1
                item = items.popleft()
                item = apply_op(monkey['operation'], item) % divisor_product
                if p1:
                    item //= 3
                if item % monkey['divisor'] == 0:
                    target_monkey = monkey['target_true']
                else:
                    target_monkey = monkey['target_false']
                monkeys[target_monkey]['items'].append(item)

    inspections = [monkey['inspections'] for monkey in monkeys.values()]
    print('inspections:', inspections)
    sorted_inspections = sorted(inspections, reverse=True)
    monkey_business = sorted_inspections[0] * sorted_inspections[1]
    print('monkey business:', monkey_business)
    if p1:
        assert monkey_business == 78678
    else:
        assert inspections == [123834, 112260, 118063, 123821, 11603, 118089, 123818, 55724]
        assert monkey_business == 15333249714


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


if __name__ == '__main__':
    main()
