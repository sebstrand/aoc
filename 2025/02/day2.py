from aocl import *


def solve(input_file, p1=True):
    line = ''.join(read_lines(input_file))
    ranges = ints(line, sep=(',', '-'))

    invalid_sum = 0
    for start_id, end_id in ranges:
        invalid_sum += sum(id for id in range(start_id, end_id + 1) if is_invalid(id, p1))
    return invalid_sum


def is_invalid(id: int, p1):
    id_str = str(id)
    str_len = len(id_str)

    # p1: See if ID consists of 2 repeating parts
    # p2: See if ID consists of 2, 3, 4, ... repeating parts
    for div in range(2, 3 if p1 else str_len + 1):
        if str_len % div != 0: continue
        seq_len = str_len // div
        if id_str.count(id_str[:seq_len]) == div:
            return True
    return False


def main():
    _input_file = 'input'
    expected = {
        'input': (53420042388, 69553832684),
        'example': (1227775554, 4174379265),
    }[_input_file]

    run(__file__, solve, _input_file, expected[0], p1=True)
    run(__file__, solve, _input_file, expected[1], p1=False)


if __name__ == '__main__':
    main()
