import math
from collections import deque, defaultdict
from dataclasses import dataclass
import random
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

    if p1:
        circuit.simulate()
        return circuit.get('z')
    else:
        random.seed(2024)

        initial_x = circuit.get('x')
        initial_y = circuit.get('y')

        # trace_per_bit = get_trace_per_bit(circuit)
        # bits = len(trace_per_bit)
        bits = 45
        # gates_on_bad_path = get_gates_on_bad_path(circuit, trace_per_bit)

        gates_per_wire = defaultdict(list)
        for gate in gates:
            gates_per_wire[gate.in1.name].append(gate)
            gates_per_wire[gate.in2.name].append(gate)
            gates_per_wire[gate.out.name].append(gate)

        # affected_bits = set()
        # for i in range(300):
        #     x = random.randint(0, 2**45)
        #     y = random.randint(0, 2**45)
        #     circuit.set('x', x)
        #     circuit.set('y', y)
        #     circuit.simulate()
        #     actual = circuit.get('z')
        #     expected = x + y
        #     for bit in range(100):
        #         mask = 2**bit
        #         if actual & mask != expected & mask:
        #             affected_bits.add(bit)
        #
        # print('affected bits', len(affected_bits), affected_bits)

        # potential_pairs = None
        # for i in range(10):
        #     circuit.reset()
        #     circuit.set('x', random.randint(0, 2**45))
        #     circuit.set('y', random.randint(0, 2**45))
        #     circuit.simulate()
        #     x = circuit.get('x')
        #     y = circuit.get('y')
        #     actual = circuit.get('z')
        #     expected = x + y
        #     assert actual != expected
        #
        #     pairs = set()
        #     for w0 in (w.name for w in wires.values() if w.value == 0):
        #         for w1 in (w.name for w in wires.values() if w.value == 1):
        #             pair = w0 + '-' + w1 if w0 < w1 else w1 + '-' + w0
        #             pairs |= {pair}
        #     if potential_pairs is None:
        #         potential_pairs = pairs
        #     else:
        #         potential_pairs &= pairs
        # print('potential pairs:', len(potential_pairs))
        # print(potential_pairs)

        # affected_bits_per_wire = {}
        # for wire in wires.values():
        #     # Ignore input wires (which aren't flipped)
        #     if wire.name[0] in ('x', 'y'): continue
        #     circuit.reset()
        #     circuit.set('x', 0)
        #     circuit.set('y', 0)
        #     wire.disabled = True
        #     circuit.simulate()
        #     wire.disabled = False
        #     affected = [i for i, value in enumerate(circuit.get_values('z')) if value is None]
        #     affected_bits_per_wire[wire.name] = affected
        # for wire, affected in affected_bits_per_wire.items():
        #     if len(affected) < bits:
        #         print(wire, affected)

        wrong_outputs = []
        y = 1
        for i in range(44):
            x = 0
            y *= 2
            circuit.set('x', x)
            circuit.set('y', y)
            circuit.simulate()
            expected = x + y
            actual = circuit.get('z')
            if actual != expected:
                show(circuit)
                ac = count_set_bits(actual)
                if ac == 1:
                    wrong_outputs.append(f'z{int(math.log2(actual)):02}')
        print(wrong_outputs)


def show(circuit):
    x = circuit.get('x')
    y = circuit.get('y')
    actual = circuit.get('z')
    expected = x + y
    if actual != expected:
        print('         x', f'{bin(x):>50}')
        print('         y', f'{bin(y):>50}')
        print('  actual z', f'{bin(actual):>50}')
        print('expected z', f'{bin(expected):>50}')
        print()


def count_set_bits(n):
    count = 0
    while n:
        n &= (n - 1)
        count += 1
    return count


def get_trace_per_bit(circuit):
    trace_per_bit = []
    for bit in range(100):
        wire = circuit.wires.get(f'z{bit:02}')
        if not wire: break
        trace_per_bit.append(set(circuit.trace(wire)))
    return trace_per_bit


def get_gates_on_bad_path(circuit, trace_per_bit):
    circuit.simulate()
    x = circuit.get('x')
    y = circuit.get('y')

    expected = x + y
    actual = circuit.get('z')

    gates = None
    for bit in range(len(trace_per_bit)):
        mask = 2**bit
        if expected & mask != actual & mask:
            if not gates:
                gates = trace_per_bit[bit]
            else:
                gates |= trace_per_bit[bit]
    return gates


class Gate:
    def __init__(self, in1, in2, out):
        self.in1 = in1
        self.in2 = in2
        self.out = out

    def apply(self):
        if self.in1.value is not None and self.in2.value is not None:
            value = self._apply()
            if value != self.out.value and not self.out.disabled:
                self.out.value = value
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
    disabled: bool = False

    def __setattr__(self, attr, value):
        if not self.disabled or attr != 'value':
            self.__dict__[attr] = value
        else:
            raise Exception('wire is disabled')


class Circuit:
    def __init__(self, gates, wires):
        self.gates = gates
        self.wires = wires

    def reset(self):
        for wire in self.wires.values():
            wire.value = None

    def get(self, prefix):
        value = 0
        for i in range(100):
            wire = self.wires.get(f'{prefix}{i:02}')
            if not wire: break
            if wire.value == 1:
                value += 2**i
        return value

    def get_values(self, prefix):
        values = []
        for i in range(100):
            wire = self.wires.get(f'{prefix}{i:02}')
            if not wire: break
            values.append(wire.value)
        return values

    def set(self, prefix, value):
        for i in range(100):
            wire = self.wires.get(f'{prefix}{i:02}')
            if not wire: break
            wire.value = 1 if value & 2**i != 0 else 0

    def simulate(self):
        while any([gate.apply() for gate in self.gates]):
            pass

    def trace(self, out):
        remaining = deque((out,))
        found = []
        while len(remaining):
            wire = remaining.popleft()
            for gate in self.gates:
                if gate.out == wire:
                    found.append(gate)
                    remaining.append(gate.in1)
                    remaining.append(gate.in2)
        return found


def main():
    _input_file = 'input'
    expected = {
        'input': (51745744348272, None),
        'example': (4, None),
        'example2': (2024, None),
    }[_input_file]

    # run(__file__, solve, _input_file, expected[0], p1=True)
    run(__file__, solve, _input_file, expected[1], p1=False)


if __name__ == '__main__':
    main()
