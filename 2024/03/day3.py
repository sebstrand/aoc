import re
from aocl import *


matcher = re.compile(r'''mul\((\d+),(\d+)\)|do\(\)|don't\(\)''')


def solve(input_file, p1=True):
    lines = read_lines(input_file)

    result = 0
    do = True

    for line in lines:
        for m in matcher.finditer(line):
            start = m.group(0)[:3]
            match start:
                case 'do(':
                    do = True
                case 'don':
                    if not p1:
                        do = False
                case 'mul':
                    if do:
                        result += int(m.group(1)) * int(m.group(2))
    return result


def main():
    real_input = True

    if real_input:
        run(__file__, solve, 'input', 178794710, p1=True)
        run(__file__, solve, 'input', 76729637, p1=False)
    else:
        run(__file__, solve, 'example', 161, p1=True)
        run(__file__, solve, 'example2', 48, p1=False)


if __name__ == '__main__':
    main()
