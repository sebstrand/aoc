from aocl import *


def main():
    lines = read_lines('input')

    full_containment_count = 0
    overlap_count = 0
    for line in lines:
        elf1, elf2 = ints(line, sep=(',', '-'))

        if elf1[1] >= elf2[0] and elf1[0] <= elf2[1]:
            overlap_count += 1

            if elf1[0] <= elf2[0] and elf1[1] >= elf2[1]:
                full_containment_count += 1
            elif elf2[0] <= elf1[0] and elf2[1] >= elf1[1]:
                full_containment_count += 1

    print('full containment count:', full_containment_count)
    assert full_containment_count == 547
    print('overlap count:', overlap_count)
    assert overlap_count == 843


if __name__ == '__main__':
    main()
