from functools import cmp_to_key
from aocl import *


def solve(input_file, p1=True):
    lines = read_lines(input_file)
    packets = [parse_packet(line) for line in lines]

    if p1:
        packet_pairs = []
        for p1, p2 in zip(packets[::2], packets[1::2]):
            packet_pairs.append((p1, p2))

        correct = []
        for i, pair in enumerate(packet_pairs):
            if compare(*pair) < 0:
                correct.append(i+1) # 1-based indices
        return sum(correct)
    else:
        divider1, divider2 = [[2]], [[6]]
        packets.append(divider1)
        packets.append(divider2)
        divider1_loc = None
        divider2_loc = None
        for i, packet in enumerate(sorted(packets, key=cmp_to_key(compare))):
            if packet == divider1:
                divider1_loc = i + 1
            elif packet == divider2:
                divider2_loc = i + 1
        return divider1_loc * divider2_loc


def parse_packet(pkt):
    return consume_list(pkt, 0)[1]


def consume_list(pkt, pos):
    assert pkt[pos] == '['
    pos += 1
    items = []
    while True:
        if pkt[pos] == ']':
            pos += 1
            break
        elif pkt[pos] == ',':
            pos += 1
            continue
        elif pkt[pos] == '[':
            pos, item = consume_list(pkt, pos)
        else:
            pos, item = consume_number(pkt, pos)
        items.append(item)
    return pos, items


def consume_number(pkt, pos):
    i = 0
    for i in range(pos, len(pkt)):
        if pkt[i] == ']' or pkt[i] == ',':
            break
    return i, int(pkt[pos:i])


def compare(left, right):
    l_type, r_type = type(left), type(right)
    if l_type == int and r_type == int:
        return left - right
    elif l_type == int and r_type == list:
        return compare([left], right)
    elif l_type == list and r_type == int:
        return compare(left, [right])
    else: # both lists
        lengths = len(left), len(right)
        for i in range(min(lengths)):
            order = compare(left[i], right[i])
            if order != 0:
                return order
        return lengths[0] - lengths[1]


def main():
    _input_file = 'input'
    expected = {
        'input': (5529, 27690),
        'example': (13, 140),
    }[_input_file]

    run(__file__, solve, _input_file, expected[0], p1=True)
    run(__file__, solve, _input_file, expected[1], p1=False)


if __name__ == '__main__':
    main()
