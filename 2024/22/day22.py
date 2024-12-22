import numpy as np
from collections import defaultdict
from aocl import *


SECRET_COUNT = 2000


def solve(input_file, p1=True):
    secrets = [int(line) for line in read_lines(input_file)]

    if p1:
        return sum(next(next_secret(secret, SECRET_COUNT)) for secret in secrets)
    else:
        bananas_per_sequence = defaultdict(int)
        for seed in secrets:
            prices = np.array(list(generate_prices(seed, SECRET_COUNT)), dtype=np.int8)
            changes = prices[1:] - prices[0:-1]

            # Track price at end of first instance of each 4-change sequence for this seed
            seed_sequence_prices = {}
            for i in range(SECRET_COUNT - 3):
                sequence = tuple(changes[i:i+4])
                if sequence not in seed_sequence_prices:
                    seed_sequence_prices[sequence] = int(prices[i+4])

            # Update the combined dict to track total banana count for each 4-change sequence
            for sequence, price in seed_sequence_prices.items():
                bananas_per_sequence[sequence] += price

        return max(bananas_per_sequence.values())


def next_secret(secret, count=1, generate=False):
    for i in range(count):
        secret = (secret ^ (secret * 64)) % 16777216
        secret = (secret ^ (secret // 32)) % 16777216
        secret = (secret ^ (secret * 2048)) % 16777216
        if generate: yield secret
    if not generate: yield secret


def generate_prices(seed, count=1):
    yield seed % 10
    for secret in next_secret(seed, count, True):
        yield secret % 10


def main():
    _input_file = 'input'
    expected = {
        'input': (20332089158, 2191),
        'example': (37327623, 24),
    }[_input_file]

    run(__file__, solve, _input_file, expected[0], p1=True)
    run(__file__, solve, _input_file, expected[1], p1=False)


if __name__ == '__main__':
    main()
