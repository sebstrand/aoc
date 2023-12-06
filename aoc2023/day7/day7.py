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


def main():
    lines = read_lines('input')

    hands_bids = []
    for line in lines:
        hand, bid = splits(line)
        bid = int(bid)
        hands_bids.append((hand, bid))

    use_jokers = False

    hands_bids.sort(key=functools.cmp_to_key(lambda hb1, hb2: compare(hb1[0], hb2[0])))
    winnings = sum((rank+1) * hb[1] for rank, hb in enumerate(hands_bids))

    print('winnings:', winnings)
    if use_jokers:
        pass
    else:
        assert winnings == 255048101


def compare(hand1, hand2):
    s1 = hand_strength(hand1)
    s2 = hand_strength(hand2)
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


def hand_strength(hand):
    c = Counter(hand)
    v = [v for v in c.values()]
    v.sort(reverse=True)
    if v[0] == 5:
        return 5.0
    elif v[0] == 4:
        return 4.0
    elif v[0] == 3:
        if v[1] == 2:
            return 3.5   # full house
        else:
            return 3.0   # three of a kind
    elif v[0] == 2:
        if v[1] == 2:
            return 2.5  # two pair
        else:
            return 2.0  # one pair
    else:
        return 1.0



if __name__ == '__main__':
    main()
