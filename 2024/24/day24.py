from dataclasses import dataclass
from aocl import *


def solve(input_file, p1=True):
    lines = read_lines(input_file, skip_empty=False)
    split = lines.index('')

    wire_defs = (labeline(line, numbered=False) for line in lines[:split])
    wires = {wd.label: Wire(wd.label, int(wd.content)) for wd in wire_defs}

    gate_defs = [splits(line) for line in lines[split + 1:]]
    gate_map = {'AND': GateAnd, 'OR': GateOr, 'XOR': GateXor}
    gates = []
    for g_in1, g_type, g_in2, _, g_out in gate_defs:
        if g_in1 not in wires:
            wires[g_in1] = Wire(g_in1, None)
        if g_in2 not in wires:
            wires[g_in2] = Wire(g_in2, None)
        if g_out not in wires:
            wires[g_out] = Wire(g_out, None)
        gates.append(gate_map[g_type](wires[g_in1], wires[g_in2], wires[g_out]))

    circuit = Circuit(gates, wires)
    return circuit.simulate()


class Gate:
    def __init__(self, in1, in2, out):
        self.in1 = in1
        self.in2 = in2
        self.out = out

    def apply(self):
        if self.out.value is not None:
            return True

        if self.in1.value is not None and self.in2.value is not None:
            self.out.value = self._apply()
            # print('applied', self, self.in1.value, self.in2.value, '->', self.out.value)
            return True
        return False

    def _apply(self):
        return None

    def __repr__(self):
        logic = self.__class__.__name__[4:].upper()
        return f'{self.in1.name} {logic} {self.in2.name} -> {self.out.name}'


class GateAnd(Gate):
    def _apply(self):
        return 1 if self.in1.value and self.in2.value else 0


class GateOr(Gate):
    def _apply(self):
        return 1 if self.in1.value or self.in2.value else 0


class GateXor(Gate):
    def _apply(self):
        return 1 if self.in1.value != self.in2.value else 0


@dataclass
class Wire:
    name: str
    value: int|None


class Circuit:
    def __init__(self, gates, wires):
        self.gates = gates
        self.wires = wires

    def simulate(self):
        done = False
        while not done:
            done = True
            for gate in self.gates:
                if not gate.apply():
                    done = False
        return self.output()

    def output(self):
        value = 0
        for i in range(100):
            wire = self.wires.get(f'z{i:02}')
            if not wire: break
            if wire.value == 1:
                value += 2**i
        return value


def main():
    _input_file = 'example2'
    expected = {
        'input': (51745744348272, None),
        'example': (4, None),
        'example2': (2024, None),
    }[_input_file]

    run(__file__, solve, _input_file, expected[0], p1=True)
    # run(__file__, solve, _input_file, expected[1], p1=False)


if __name__ == '__main__':
    main()
