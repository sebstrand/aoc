from aocl import *
from collections import defaultdict


def main():
    lines = read_lines('input')

    steps = splits(lines[0], sep=(',',))

    boxes = defaultdict(Box)
    for step in steps:
        parts = splits(step, ('-', '='))[0]

        label = parts[0]
        focal_length = None
        if len(parts) == 2:
            focal_length = int(parts[1])

        box = HASH(label)
        if focal_length:
            boxes[box].add((label, focal_length))
        else:
            boxes[box].remove(label)

    total_focusing_power = 0
    for box in boxes:
        box_lens_powers = [(box+1) * pwr for pwr in boxes[box].lens_powers()]
        print(f'box: {box:3}', boxes[box].lenses, 'lens focusing powers', box_lens_powers)
        total_focusing_power += sum(box_lens_powers)

    print()
    hash_sum = sum(HASH(step) for step in steps)
    assert hash_sum == 509167
    print('step HASH sum:', hash_sum)

    print('total focusing power:', total_focusing_power)
    assert total_focusing_power == 259333


class Box:
    def __init__(self):
        self.lenses = []

    def add(self, lens):
        for i, old_lens in enumerate(self.lenses):
            if old_lens[0] == lens[0]:
                self.lenses[i] = lens
                return
        self.lenses.append(lens)

    def remove(self, label):
        for i, old_lens in enumerate(self.lenses):
            if old_lens[0] == label:
                self.lenses.pop(i)
                break

    def lens_powers(self):
        return [(i+1) * lens[1] for i, lens in enumerate(self.lenses)]



def HASH(s):
    h = 0
    for c in s:
        h += ord(c)
        h *= 17
        h = h % 256
    return h


if __name__ == '__main__':
    main()
