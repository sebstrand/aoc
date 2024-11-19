from aocl import *
from collections import Counter
import functools


card_values = {
    'A': 14,
    'K': 13,
    'Q': 12,
    'J': 11,
    'T': 10,
    '9': 9,
    '8': 8,
    '7': 7,
    '6': 6,
    '5': 5,
    '4': 4,
    '3': 3,
    '2': 2,
}


def solve(input_file, p1=True):
    lines = read_lines(input_file)

    hands_bids = []
    for line in lines:
        hand, bid = splits(line)
        bid = int(bid)
        hands_bids.append((hand, bid))

    use_jokers = not p1
    if use_jokers:
        card_values['J'] = 1

    hands_bids.sort(key=functools.cmp_to_key(lambda hb1, hb2: compare(hb1[0], hb2[0], use_jokers)))
    winnings = sum((rank0+1) * hb[1] for rank0, hb in enumerate(hands_bids))
    # for rank0, hb in enumerate(hands_bids):
    #     print(hb[0], hand_strength(hb[0]), f'b{hb[1]:3} r{rank0 + 1:3}')
    return winnings


def compare(hand1, hand2, use_jokers):
    s1 = hand_strength(hand1, use_jokers)
    s2 = hand_strength(hand2, use_jokers)
    # print('s1, s2:', hand1, s1, '::', hand2, s2)

    if s1 > s2:
        return 1
    elif s1 < s2:
        return -1
    else:
        for i, card1 in enumerate(hand1):
            card2 = hand2[i]
            card_value1, card_value2 = card_values[card1], card_values[card2]
            if card_value1 > card_value2:
                return 1
            elif card_value1 < card_value2:
                return -1
    return 0


def hand_strength(hand, use_jokers):
    c = Counter(hand)

    v = [v for v in c.values()]
    v.sort(reverse=True)

    if v[0] == 5:
        strength = 5.0
    elif v[0] == 4:
        strength = 4.0
    elif v[0] == 3:
        if v[1] == 2:
            strength = 3.5   # full house
        else:
            strength = 3.0   # three of a kind
    elif v[0] == 2:
        if v[1] == 2:
            strength = 2.5  # two pair
        else:
            strength = 2.0  # one pair
    else:
        strength = 1.0

    jokers = c['J']
    if use_jokers and jokers > 0 and strength < 5.0:
        if jokers == 4:
            # four jokers can copy the remaining card -> 5-of-a-kind
            strength = 5.0
        elif jokers == 3:
            if strength == 3.5:
                # remaining cards are a pair -> 5-of-a-kind
                strength = 5.0
            else:
                strength = 4.0  # copy one of the remaining cards -> 4-of-a-kind
        elif jokers == 2:
            if strength == 4.0:
                # not possible
                assert False
            elif strength == 3.5:
                # remaining three cards are identical, copy them -> 5-of-a-kind
                strength = 5.0
            elif strength == 3.0:
                # not possible
                assert False
            elif strength == 2.5:
                # there's another pair, copy them -> 4-of-a-kind
                strength = 4.0
            elif strength == 2.0:
                # 2 jokers + 3 dissimilar cards, copy one of the remaining cards -> 3-of-a-kind
                strength = 3.0
        elif jokers == 1:
            if strength == 4.0:
                # copy the other four identical cards -> 5-of-a-kind
                strength = 5.0
            elif strength == 3.5:
                # not possible
                assert False
            elif strength == 3.0:
                # 3-of-a-kind + joker + other card -> 4-of-a-kind
                strength = 4.0
            elif strength == 2.5:
                # joker + two pairs -> full house
                strength = 3.5
            elif strength == 2.0:
                # pair + joker + 2 dissimilar cards -> 3-of-a-kind
                strength = 3.0
            elif strength == 1.0:
                # joker + 4 dissimilar cards -> pair
                strength = 2.0

    return strength


def main():
    _input_file = 'input'
    expected = {
        'input': (255048101, 253718286),
        'example': (6440, 5905),
    }[_input_file]

    run(__file__, solve, _input_file, expected[0], p1=True)
    run(__file__, solve, _input_file, expected[1], p1=False)


if __name__ == '__main__':
    main()
