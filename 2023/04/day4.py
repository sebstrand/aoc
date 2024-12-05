from aocl import *


def solve(input_file, p1=True):
    lines = read_lines(input_file)

    total_value = 0
    cards = []
    for line in lines:
        line = labeline(line)
        winning, available = ints(line.content, sep=(r'\|', ' '))
        cards.append([1, winning, available])

        value = 0
        for n in available:
            if n in winning:
                value = max(1, 2*value)
        total_value += value

    if p1:
        return total_value

    for i, card in enumerate(cards):
        num, winning, available = card
        matches = 0
        for n in available:
            if n in winning:
                matches += 1
        for j in range(i+1, i+1+matches):
            cards[j][0] += num

    total_cards = sum([card[0] for card in cards])
    return total_cards


def main():
    _input_file = 'input'
    expected = {
        'input': (21558, 10425665),
        'example': (13, 30),
    }[_input_file]

    run(__file__, solve, _input_file, expected[0], p1=True)
    run(__file__, solve, _input_file, expected[1], p1=False)


if __name__ == '__main__':
    main()
