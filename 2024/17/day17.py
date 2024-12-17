import functools
# from dataclasses import dataclass
import math
from aocl import read_lines, splits, ints, run


def solve(input_file, p1=True):
    lines = read_lines(input_file, skip_empty=False)
    split = lines.index('')
    registers = {}
    for line in lines[:split]:
        s = splits(line)
        registers[s[1][:-1]] = int(s[-1])

    program = ints(lines[-1])

    computer = Computer(registers, debug=False)
    if p1:
        out = computer.run(program)
        return ','.join(str(i) for i in out)
    else:
        # Example program:
        # 0,3,5,4,3,0
        # adv 3 => A = A / 2**3 => A = A / 8
        # out 4 => o = A % 8
        # jnz 0 => jump to start if A is not 0
        #
        # (a // 8**1) % 8 = 0 => remainder of a//8 == 0       ~> x = 0 + a1*8        => (8**-1)*x ≡ 0 (mod 8)
        # (a // 8**2) % 8 = 3 => remainder of a//64 == 3      ~> x = 3 + a2*64       => (8**-2)*x ≡ 3 (mod 8)
        # (a // 8**3) % 8 = 5 => remainder of a//512 == 5     ~> x = 5 + a3*512      => (8**-3)*x ≡ 5 (mod 8)
        # (a // 8**4) % 8 = 4 => remainder of a//4096 == 4    ~> x = 4 + a4*4096     => (8**-4)*x ≡ 4 (mod 8)
        # (a // 8**5) % 8 = 3 => remainder of a//32768 == 3   ~> x = 3 + a5*32768    => (8**-5)*x ≡ 3 (mod 8)
        # (a // 8**6) % 8 = 0 => remainder of a//262144 == 0  ~> x = 0 + a6*262144   => (8**-6)*x ≡ 0 (mod 8)
        #
        # Real program:
        # 2,4,1,2,7,5,4,5,0,3,1,7,5,5,3,0
        #
        # bst 4 => B = A % 8
        # bxl 2 => B = B ^ 2
        # cdv 5 => C = A / 2**B
        # bxc 5 => B = B ^ C
        # adv 3 => A = A / 2**3 => A = A / 8
        # bxl 7 => B = B ^ 7
        # out 5 => o = B % 8
        # jnz 0 => jump to start if A is not 0
        #
        # o = ((((A % 8)^2)^(A/2**((A % 8)^2)))^7) % 8

        print(program)
        print()

        test_a = 894450703
        registers['A'] = test_a
        computer.reset()
        out = computer.run(program)
        print('test result', out, out == program[:len(out)])
        return None

        search_space, output_extend_cycle = find_search_space(program)
        print('search space', search_space)
        print('output extend cycle', output_extend_cycle)
        program = program[:10]

        for a in range(0, 8**len(program)):
            i = 0
            a_start = a
            while a > 0:
                calc_o = ((((a % 8) ^ 2) ^ (a // 2 ** ((a % 8) ^ 2))) ^ 7) % 8
                if calc_o != program[i]:
                    break
                a //= 8
                i += 1
            if i == len(program):
                print('FOUND IT!', a_start)
                break

        # cycles = find_cycles(program, output_extend_cycle)
        # print('cycles', cycles)
        return None

        a = 0
        cycles = {}
        found_cycles = 0

        while True:
            registers['A'] = a
            computer.reset()
            out = computer.run(program)
            if len(out) > len(program):
                print('output too long', a)
                break
            elif out == program:
                print('found it!')
                return a

            next_a = a + 1
            for i, value in enumerate(out):
                cycle = cycles.get(i)
                if out[i] == program[i]:
                    if not cycle:
                        cycle = cycles[i] = Cycle(value=out[i], first_seen=a)
                        print(f'cycle #{i}:{cycle.value}', 'starts on', cycle.first_seen)
                    elif cycle.duration > 0 and cycle.repeats < 0:
                        cycle.repeats = a - cycle.first_seen
                        cycle.repeats = 2 ** math.ceil(math.log2(cycle.repeats) - 0.1)
                        print(f'cycle #{i}:{cycle.value}', 'repeats', cycle.repeats,
                              math.log2(a - cycle.first_seen) - 0.1)
                        found_cycles += 1
                elif cycle:
                    if cycle.duration < 0:
                        cycle.duration = a - cycle.first_seen
                        # print(f'cycle #{i}:{cycle.value}', 'duration', cycle.duration)
                    # n_repeat = (a - cycle.first_seen) / cycle.repeats
                    repeat_i = math.ceil((a - cycle.first_seen) / cycle.repeats)
                    this_jump = cycle.first_seen + repeat_i * cycle.repeats
                    if this_jump > next_a:
                        # print('jump with', i, cycle.repeats)
                        next_a = this_jump

            # --xx----xx----xx----xx--
            # first_seen = 2
            # repeats = 6
            #
            # a = 15
            # a - first_seen = 13
            # n_repeats = ceil(_ / repeats) = 13/6 = 3
            # first_seen + n_repeats * repeats = 14

            if found_cycles == len(program):
                print('found all cycles')
                break
            # print('jump', next_a - a)
            a = next_a

        out = []
        for i, cycle in cycles.items():
            registers['A'] = cycle.first_seen + cycle.repeats * 2
            computer.reset()
            this_out = computer.run(program)
            out.append(this_out[i])
            print(this_out[i], end=', ')
        print()
        print('is same', out == program)


def check(computer, program, a, i):
    registers = {'A': a, 'B': 0, 'C': 0}
    computer.reset()
    out = computer.run(program)
    if i < len(out):
        return out[i]


def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y


def chinese_remainder_theorem(congruences):
    # Extract divisors and remainders from tuples
    num = [n for n, r in congruences]
    rem = [r for n, r in congruences]

    # Compute product of all numbers
    prod = 1
    for n in num:
        prod *= n

    result = 0
    # Apply CRT formula
    for n, r in zip(num, rem):
        pp = prod // n
        gcd, inv, _ = extended_gcd(pp, n)
        result += r * pp * inv

    return result % prod


def find_search_space(program):
    last_len = 0
    last_len_change = None
    a = 0
    registers = {'A': 0, 'B': 0, 'C': 0}
    computer = Computer(registers)
    while True:
        registers['A'] = a
        computer.reset()
        out = computer.run(program)
        if len(out) > last_len:
            if last_len_change is None:
                last_len_change = a
                last_len = len(out)
            else:
                output_extend_cycle = a - last_len_change
                break
        a += 1

    lens = len(program) - 1, len(program)
    return (output_extend_cycle ** lens[0], output_extend_cycle ** lens[1]), output_extend_cycle


def find_cycles(program, output_extend_cycle):
    # last one right: >= 175921860444160 (certain) <= 211106165767183 (certain)
    # answer is above    187025214891616

    registers = {'A': 0, 'B': 0, 'C': 0}
    computer = Computer(registers)

    # left = 175921827232783
    # right = 211106165767183
    # value = program[-1]
    # while True:
    #     middle = (right + left) // 2
    #     print('middle', middle)
    #     computer.reset()
    #     registers['A'] = middle - 1
    #     out1 = computer.run(program)[-1]
    #
    #     computer.reset()
    #     registers['A'] = middle
    #     out2 = computer.run(program)[-1]
    #     if out1 != value:
    #         if out2 == value:
    #             print('found border', middle, out1, out2)
    #             break
    #         else:
    #             left = middle
    #     else:
    #         right = middle
    #     print('l/r', left, right)

    # for i in range(len(program)):
    # for a in range(output_extend_cycle**i, output_extend_cycle**(i+1)):
    # for a in range(15, 99999, 512):
    # for a in range(67451919, 9999999999, 2**26):
    # for a in range(35184372088832, 281474976710656, 2**25):
    # for a in range(187025214891616, 281474976710656, 2**26):
    # for a in range(187025156553743, 281474976710656, 2**24):
    # for a in range(281467930622991 - 1000*2**26, 281474976710656, 2**26):
    # for a in range(281450750753807 - 2**26, 281474976710656, 2**10):
    # last_one_right_previous = False
    # for a in range(281450750753807, 0, -2**26):
    # for a in range(211106165767183, 0, -2**25):
    for a in range(0, 30000 + 1):
        computer.reset()
        registers['A'] = a
        out = computer.run(program)

        if out == program:
            print('=== WOO === ', a, out)
            break
        # elif best > 4:
        #     print('best', best, len(program))

        # if (a - 187025214891616) % 100000 == 0:
        #     print((a - 187025214891616) / (211106165767183 - 187025214891616) * 100, '%')

        #     last_one_right = out[-1] == program[-1]
        #     if not last_one_right or len(out) < len(program):
        #         print('not right anymore at', a, last_one_right)
        #         break
        # if last_one_right:
        #     if not last_one_right_previous:
        #         last_one_right_previous = True
        #         print('last one flip right at', a)
        # else:
        #     last_one_right_previous = False
        # elif last_one is None:
        #     last_one = out[-1]
        #     last_one_a = a
        # elif out[-1] != last_one:
        #     print('last one', a, last_one_a - a)
        #     break
        # print((a - (281450750753807 - 2**26)) / (281474976710656 - (281450750753807 - 2**26)) * 100, '%')
        # print(f'@{a:10}: ', end='')
        # # one_correct = False
        # for i in range(len(out)):
        #     correct = out[i] == program[i]
        #     # one_correct = one_correct or correct
        #     if correct:
        #         print(term_effect(str(out[i]), Terminal.CYAN), end=' ')
        #     else:
        #         print(str(out[i]), end=' ')
        # print()
        # if one_correct:
        #     print('             ', end='')
        #     for i in range(len(out)):
        #         calc_o = ((((a % 8) ^ 2) ^ (a // 2 ** ((a % 8) ^ 2))) ^ 7) % 8
        #         a //= 8
        #         print(term_effect(str(calc_o), Terminal.CYAN), end=' ')
        #     print()

        # last one flip at 211106165767183
        # last one flip at 26388212300815
        # last one flip at 3298468117519
        # last one flip at 412250094607
        # last one flip at 51472841743
        # last one flip at 6375685135
        # last one flip at 738540559

        # 1039, 2993, 3087 (first 3) => 4947
        # 15375 (first 5)
        # 80911 (first 6)
        # 343055, 17120271 (first 7)
        # 67451919, 134560783 (first 8)
        # 1543846927, 1946500111 (first 10)
        # 281467930622991: 2, 4, 1, 2, 7, 5, 4, 5, 0, 3, 3, 5, 5, 5, 3, 2 (only 3 wrong)
        # 281450750753807: 2, 4, 1, 2, 7, 5, 4, 5, 0, 3, 1, 7, 5, 5, 3, 2 (only last one wrong!)

        # if out == program[i]:
        #     if not cycle:
        #         cycle = cycles[i] = Cycle(value=out, first_seen=a)
        #         print(f'cycle #{i}:{cycle.value}', 'starts on', cycle.first_seen)
        #     elif cycle.duration > 0 and cycle.repeats < 0:
        #         cycle.repeats = a - cycle.first_seen
        #         cycle.repeats = 2**math.ceil(math.log2(cycle.repeats) - 0.1)
        #         print(f'cycle #{i}:{cycle.value}', 'repeats', cycle.repeats, math.log2(a - cycle.first_seen) - 0.1)
        #         found_cycles += 1
        # elif cycle:
        #     if cycle.duration < 0:
        #         cycle.duration = a - cycle.first_seen
        #         # print(f'cycle #{i}:{cycle.value}', 'duration', cycle.duration)
        #     # n_repeat = (a - cycle.first_seen) / cycle.repeats
        #     repeat_i = math.ceil((a - cycle.first_seen) / cycle.repeats)
        #     this_jump = cycle.first_seen + repeat_i * cycle.repeats
        #     if this_jump > next_a:
        #         # print('jump with', i, cycle.repeats)
        #         next_a = this_jump
    # if i > 2:
    #     break


# @dataclass
# class Cycle:
#     value: int = -1
#     first_seen: int = -1
#     duration: int = -1
#     repeats: int = -1


class Computer:
    OP = ['adv', 'bxl', 'bst', 'jnz', 'bxc', 'out', 'bdv', 'cdv']

    def __init__(self, registers, debug=False):
        self.output = []
        self.registers = registers
        self.debug = debug

    def reset(self):
        self.output.clear()

    def run(self, program):
        if self.debug: print('initial registers:', self.registers)
        pointer = 0
        while pointer < len(program):
            opcode, operand = program[pointer], program[pointer + 1]
            jump_to = getattr(self, Computer.OP[opcode])(operand)
            if jump_to is not None:
                pointer = jump_to
            else:
                pointer += 2
        return self.output

    def _combo(self, operand):
        if operand < 4:
            return operand
        else:
            return self.registers['ABC'[operand - 4]]

    def adv(self, operand):
        self._div(operand, 'A')

    def bxl(self, operand):
        value = self.registers['B']
        result = value ^ operand
        if self.debug: print('bst', value, '^', operand, '=>', result)
        self.registers['B'] = result

    def bst(self, operand):
        value = self._combo(operand) % 8
        if self.debug: print('bst', operand, '=>', value)
        self.registers['B'] = value

    def jnz(self, operand):
        if self.registers['A'] != 0:
            if self.debug: print('jnz', self.registers['A'], '=> jump', operand)
            return operand
        else:
            if self.debug: print('jnz', self.registers['A'], '=> no jump')

    def bxc(self, _):
        operand1, operand2 = self.registers['B'], self.registers['C']
        result = operand1 ^ operand2
        if self.debug: print('bxc', operand1, '^', operand2, '=>', result)
        self.registers['B'] = result

    def out(self, operand):
        real_operand = self._combo(operand)
        value = real_operand % 8
        if self.debug: print('out', operand, real_operand, '=>', value)
        self.output.append(value)

    def bdv(self, operand):
        self._div(operand, 'B')

    def cdv(self, operand):
        self._div(operand, 'C')

    def _div(self, operand, register):
        nom = self.registers['A']
        den = 2 ** self._combo(operand)
        result = nom // den
        self.registers[register] = result
        if self.debug: print(register.lower() + 'dv', nom, '/', den, '=>', result)


def main():
    real_input = True

    expected = {
        'input': ('4,3,7,1,5,3,0,5,4', 190384615275535),
        'example': '4,6,3,5,6,3,5,2,1,0',
        'example2': 117440,
    }

    if real_input:
        # run(__file__, solve, 'input', expected['input'][0], p1=True)
        run(__file__, solve, 'input', expected['input'][1], p1=False)
    else:
        # run(__file__, solve, 'example', expected['example'], p1=True)
        run(__file__, solve, 'example2', expected['example2'], p1=False)


if __name__ == '__main__':
    main()
