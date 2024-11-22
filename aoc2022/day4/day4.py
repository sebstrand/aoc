from aocl import *


def solve(input_file, p1=True):
    lines = read_lines(input_file)

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

    if p1:
        return full_containment_count
    else:
        return overlap_count


def main():
    _input_file = 'input'
    expected = {
        'input': (547, 843),
        'example': (2, 4),
    }[_input_file]

    run(__file__, solve, _input_file, expected[0], p1=True)
    run(__file__, solve, _input_file, expected[1], p1=False)


if __name__ == '__main__':
    main()
