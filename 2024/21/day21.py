from aocl import *

# Typing 0:
# (nk) 0 (r1k) <A (r2k) v<<A>>^A (r3k) v<A<AA>>^AvAA<^A>A (user)
#
# what's required for output 0? (left) (press)
# what's required for output left? (down) (left) (left) (press)
# what's required for output down? (down) (left) (press)

def solve(input_file, p1=True):
    codes = read_lines(input_file)
    #codes = ['0', '9', '1', '4', '3'])
    # codes = ['0']

    keypads = make_keypads()
    complexities = []
    sequences = []
    for code in codes:
        for keypad in keypads: keypad.reset()
        print('Code', code, '-' * 70)
        sequence = []
        for c in code:
            sequence.append(expand(c, keypads))
        sequence = ''.join(sequence)
        print(len(sequence), ' ', sep='', end='')
        print(sequence)
        sequences.append(sequence)
        complexities.append(len(sequence) * ints(code)[0])
    # print(sequences)
    # print(complexities)
    return sum(complexities)


def expand(num_key, keypads):
    sequence = num_key
    for keypad, next_keypad in zip(keypads[0::1], keypads[1::1]):
        sequence = keypad.movement_alternatives(sequence, next_keypad.current_key())
        # print(''.join(sequence))
    sequence = keypads[-1].movement_alternatives(sequence)
    return sequence


def make_keypads():
    directional_keys = {
        '.': (0, 0), '^': (0, 1), 'A': (0, 2),
        '<': (1, 0), 'v': (1, 1), '>': (1, 2),
    }

    return [
        Keypad('numeric', {
            '7': (0, 0), '8': (0, 1), '9': (0, 2),
            '4': (1, 0), '5': (1, 1), '6': (1, 2),
            '1': (2, 0), '2': (2, 1), '3': (2, 2),
            '.': (3, 0), '0': (3, 1), 'A': (3, 2),
        }),
        Keypad('robot1', directional_keys),
        Keypad('robot2', directional_keys),
    ]


class Keypad:
    def __init__(self, name, keys):
        self.name = name
        self.keys = keys

        self.current = self.initial = self.keys['A']
        self.pos_to_key = {pos: key for key, pos in self.keys.items()}

        positions = self.keys.values()
        self.size = max(y for y, _ in positions) + 1, max(x for _, x in positions) + 1

    def reset(self):
        self.current = self.initial

    def current_key(self):
        return self.pos_to_key[self.current]

    def movement_alternatives(self, sequence, preferred_key=None):
        move_sequence = []
        current_y, current_x = self.current
        invalid_y, invalid_x = self.keys['.']

        for s in sequence:
            target_y, target_x = self.keys[s]

            while current_y != target_y or current_x != target_x:
                diff_x = target_x - current_x
                diff_y = target_y - current_y
                if diff_y != 0 and diff_x != 0:
                    if current_y == invalid_y and target_x == invalid_x or \
                            diff_y < 0 and preferred_key == '^' or \
                            diff_y > 0 and preferred_key == 'v':
                        # must move y first
                        current_y = target_y
                        move_sequence.append(('v' if diff_y > 0 else '^') * abs(diff_y))
                    else:
                        # can move x first
                        current_x = target_x
                        move_sequence.append(('>' if diff_x > 0 else '<') * abs(diff_x))
                elif diff_x != 0:
                    current_x = target_x
                    move_sequence.append(('>' if diff_x > 0 else '<') * abs(diff_x))
                elif diff_y != 0:
                    current_y = target_y
                    move_sequence.append(('v' if diff_y > 0 else '^') * abs(diff_y))
                # self.show((current_y, current_x), Terminal.CYAN)
            move_sequence.append('A')
        self.current = (current_y, current_x)
        return ''.join(move_sequence)

    def show(self, marker=None, style=None):
        print('-' * (self.size[1] + 2))
        for y in range(self.size[0]):
            print('|', end='')
            for x in range(self.size[1]):
                key = self.pos_to_key.get((y, x), '.')
                if (y, x) == marker:
                    print(term_effect(key, style), end='')
                else:
                    print(key, end='')
            print('|')
        print('-' * (self.size[1] + 2))

    def __str__(self):
        return f'Keypad "{self.name}"'


def main():
    _input_file = 'input'
    expected = {
        'input': (None, None),  # 223838 too high, seq lens = 68, 72, 74, 70, 76
        'example': (126384, None),
    }[_input_file]

    run(__file__, solve, _input_file, expected[0], p1=True)
    # run(__file__, solve, _input_file, expected[1], p1=False)


if __name__ == '__main__':
    main()
