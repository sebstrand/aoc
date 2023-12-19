import math
from aocl import *
from collections import deque, defaultdict


def solve(input_file, p1=True):
    lines = read_lines(input_file)

    modules = {}
    for line in lines:
        [m_name], destinations = splits(line, (' -> ', ', '))

        if m_name[0] == '&':
            m_name = m_name[1:]
            module = Conjunction(m_name, destinations)
        elif m_name[0] == '%':
            m_name = m_name[1:]
            module = FlipFlop(m_name, destinations)
        else:
            module = Splitter(m_name, destinations)
        modules[m_name] = module

    for name, module in modules.items():
        for destination in module.destinations:
            if destination in modules:
                modules[destination].input_count += 1

    if p1:
        low_count = high_count = 0
        for i in range(1000):
            l, h, _ = push_button(modules)
            low_count += l
            high_count += h

        print('Pulse counts l/h:', low_count, high_count)
        return low_count * high_count
    else:
        output_module_name = 'rx'
        output_source = [
            m for m in modules.values()
            if len([n for n in m.destinations if n == output_module_name])
        ]
        # This is not a general solution
        assert len(output_source) == 1
        output_source = output_source[0]
        assert isinstance(output_source, Conjunction)

        # Need to figure out periods with which the output_source conjunction inputs produce low signals.
        # The LCM of the periods is the answer.
        button_presses = 0
        first_high = {}
        while len(first_high) < output_source.input_count:
            button_presses += 1
            _, _, tracking_result = push_button(modules, output_source)

            for src in tracking_result.keys():
                if src not in first_high:
                    first_high[src] = button_presses

        print('Cycle lengths:', first_high)
        return math.lcm(*first_high.values())


def push_button(modules, track_conjunction=None):
    pulse_queue = deque([('broadcaster', 'button', False)])
    low_count = high_count = 0
    tracking_result = {}
    while len(pulse_queue) > 0:
        p_target, p_source, p_value = pulse_queue.popleft()
        # print(f'{p_source} {("-low", "-high")[p_value]}-> {p_target}')
        if p_value:
            high_count += 1
        else:
            low_count += 1

        target_module = modules.get(p_target)
        if not target_module:
            continue

        output_pulses = target_module.process((p_source, p_value))
        if target_module == track_conjunction:
            for src, value in target_module.memory.items():
                if value:
                    tracking_result[src] = True
        if not output_pulses:
            continue

        for pulse in output_pulses:
            pulse_queue.append(pulse)
    return low_count, high_count, tracking_result


class Module:
    def __init__(self, name, destinations):
        self.name = name
        self.destinations = destinations
        self.input_count = 0
        self.type_id = ''

    def __str__(self):
        cname = self.__class__.__name__[:3]
        destinations = ', '.join([str(d) for d in self.destinations])
        return f'{cname}"{self.name}"<{self.input_count}->{destinations}>'

    def __repr__(self):
        return str(self)

    def process(self, pulse):
        return None


class Splitter(Module):
    def process(self, pulse):
        return [(d, self.name, pulse[1]) for d in self.destinations]


class Conjunction(Module):
    def __init__(self, name, destinations):
        super().__init__(name, destinations)
        self.type_id = '&'
        self.memory = defaultdict(bool)

    def process(self, pulse):
        p_source, p_value = pulse
        self.memory[p_source] = p_value
        high = [v for v in self.memory.values() if v]
        all_high = len(high) == self.input_count
        return [(d, self.name, not all_high) for d in self.destinations]


class FlipFlop(Module):
    def __init__(self, name, destinations):
        super().__init__(name, destinations)
        self.type_id = '%'
        self.state = False

    def process(self, pulse):
        if not pulse[1]:
            # process low pulse
            self.state = not self.state
            return [(d, self.name, self.state) for d in self.destinations]


def main():
    _input_file = 'input'
    expected = {
        'input': (929810733, 231657829136023),
        'example': (32000000, None),
        'example2': (11687500, None),
    }[_input_file]

    run(__file__, solve, _input_file, expected[0], p1=True)
    run(__file__, solve, _input_file, expected[1], p1=False)


if __name__ == '__main__':
    main()
