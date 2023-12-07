from aocl import *
from collections import deque
from functools import reduce


def main():
    lines = deque(read_lines('example'))

    monkeys = {}
    while len(lines) > 0:
        monkey = labeline(lines.popleft())
        monkeys[monkey.number] = {
            'items': deque([factors(i) for i in ints(labeline(lines.popleft(), numbered=False).content, sep=(r', ',))]),
            'operation': splits(labeline(lines.popleft(), numbered=False).content[6:])[1:],
            'divisor': int(splits(labeline(lines.popleft(), numbered=False).content)[-1]),
            'target_true': int(splits(lines.popleft())[-1]),
            'target_false': int(splits(lines.popleft())[-1]),
            'inspections': 0,
        }
        # print(monkeys[monkey.number])

    p1 = False
    if p1:
        rounds = 20
    else:
        # rounds = 10000
        rounds = 1

    for rnd in range(rounds):
        print('round', rnd)
        for turn in range(len(monkeys)):
            print('Turn: Monkey', turn)
            monkey = monkeys[turn]
            items = monkey['items']
            while len(items):
                monkey['inspections'] += 1
                worry_level = items.popleft()
                print('  inspect', worry_level)
                worry_level = apply_op(monkey['operation'], worry_level)
                print('  increase to', worry_level)
                if p1:
                    worry_level = apply_op(('/', 3), worry_level)
                    print('  decrease to', worry_level)
                print('  check', worry_level, 'divisible by', monkey['divisor'])
                if monkey['divisor'] in worry_level:
                    target_monkey = monkey['target_true']
                    print('  true, throw to', target_monkey)
                else:
                    target_monkey = monkey['target_false']
                    print('  false, throw to', target_monkey)
                monkeys[target_monkey]['items'].append(worry_level)
        print()
        for m in monkeys:
            monkey = monkeys[m]
            print(f'Monkey {m}:', [w for w in monkey['items']])
        print()

    inspections = [monkey['inspections'] for monkey in monkeys.values()]
    # print(inspections)
    inspections.sort(reverse=True)
    monkey_business = inspections[0] * inspections[1]
    print('monkey business:', monkey_business)
    if p1:
        assert monkey_business == 78678
    else:
        assert monkey_business == 0


def apply_op(operation, worry_level):
    op, num = operation
    if num == 'old':
        num = max(worry_level)
    else:
        num = int(num)

    # print(op, num, worry_level)
    if op == '*':
        return factors(max(worry_level) * num)
    elif op == '+':
        return factors(max(worry_level) + num)
    elif op == '/':
        return factors(max(worry_level) // num)


if __name__ == '__main__':
    main()
