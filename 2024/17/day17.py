from aocl import *


def solve(input_file, p1=True):
    lines = read_lines(input_file, skip_empty=False)
    split = lines.index('')

    registers = {}
    for line in lines[:split]:
        s = splits(line)
        registers[s[1][:-1]] = int(s[-1])

    program = ints(lines[-1])

    computer = Computer(registers)
    output = computer.run(program)
    return ','.join(str(i) for i in output)


class Computer:
    OP = ['adv', 'bxl', 'bst', 'jnz', 'bxc', 'out', 'bdv', 'cdv']

    def __init__(self, registers, debug=False):
        self.output = []
        self.registers = registers
        self.debug = debug
        if self.debug: print('initial registers:', registers)

    def run(self, program):
        pointer = 0
        while pointer < len(program):
            opcode, operand = program[pointer], program[pointer+1]
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
        nom = self.registers['A']
        den = 2**self._combo(operand)
        result = nom // den
        self.registers['A'] = result
        if self.debug: print('adv', nom, '/', den, '=>', result)

    def bxl(self, operand):
        # The bxl instruction (opcode 1) calculates the bitwise XOR of register B and the
        # instruction's literal operand, then stores the result in register B.
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
        value = self._combo(operand) % 8
        if self.debug: print('out', operand, '=>', value)
        self.output.append(value)

    def bdv(self, operand):
        nom = self.registers['A']
        den = 2**self._combo(operand)
        result = nom // den
        self.registers['B'] = result
        if self.debug: print('bdv', nom, '/', den, '=>', result)

    def cdv(self, operand):
        self._div(operand, 'C')
        nom = self.registers['A']
        den = 2**self._combo(operand)
        result = nom // den
        self.registers['C'] = result
        if self.debug: print('cdv', nom, '/', den, '=>', result)

    def _div(self, operand, register):
        nom = self.registers['A']
        den = 2**self._combo(operand)
        result = nom // den
        self.registers[register] = result
        if self.debug: print(register.lower() + 'dv', nom, '/', den, '=>', result)


def main():
    _input_file = 'input'
    expected = {
        'input': ('4,3,7,1,5,3,0,5,4', None),
        'example': ('4,6,3,5,6,3,5,2,1,0', None),
    }[_input_file]

    run(__file__, solve, _input_file, expected[0], p1=True)
    # run(__file__, solve, _input_file, expected[1], p1=False)


if __name__ == '__main__':
    main()
