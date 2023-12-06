from aocl import *
from collections import Counter


def main():
    lines = read_lines('input', skip_empty=False)

    elves = Counter()
    elf = 0
    for line in lines:
        if not line:
            elf += 1
        else:
            elves[elf] += int(line)

    calories = list(elves.values())
    max_calories = max(calories)
    print('max single elf calories:', max_calories)
    assert max_calories == 69836

    calories.sort(reverse=True)
    top_three_calories = sum(calories[:3])
    print('top three elf calories:', top_three_calories)
    assert top_three_calories == 207968


if __name__ == '__main__':
    main()
