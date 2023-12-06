from aocl import *


def main():
    lines = read_lines('input')

    first_p1 = re.compile(r'\D*(\d)')
    last_p1 = re.compile(r'.*(\d)')

    digit_names_re = '|'.join(digit_names)
    first_p2 = re.compile(f'.*?(\d|{digit_names_re})')
    last_p2 = re.compile(f'.*(\d|{digit_names_re})')

    sum_p1 = 0
    sum_p2 = 0
    for line in lines:
        m1 = first_p1.match(line)
        m2 = last_p1.match(line)
        if m1 and m2:
            digit1 = m1.group(1)
            digit2 = m2.group(1)
            sum_p1 += int(digit1 + digit2)

        digit1 = to_digit(first_p2.match(line).group(1))
        digit2 = to_digit(last_p2.match(line).group(1))
        sum_p2 += int(digit1 + digit2)

    print('calibration value p1:', sum_p1)
    assert sum_p1 == 54597

    print('calibration value p2:', sum_p2)
    assert sum_p2 == 54504


def to_digit(maybe_digit):
    try:
        return str(digit_names.index(maybe_digit))
    except ValueError:
        return maybe_digit


if __name__ == '__main__':
    main()
