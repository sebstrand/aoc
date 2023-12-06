from aocl import *


def main():
    lines = read_lines('input')

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

    print('total value:', total_value)
    assert total_value == 21558

    for i, card in enumerate(cards):
        num, winning, available = card
        matches = 0
        for n in available:
            if n in winning:
                matches += 1
        for j in range(i+1, i+1+matches):
            cards[j][0] += num

    total_cards = sum([card[0] for card in cards])
    print('total cards:', total_cards)
    assert total_cards == 10425665


if __name__ == '__main__':
    main()
