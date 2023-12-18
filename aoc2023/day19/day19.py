import re
import operator
from aocl import *
from collections import Counter
from functools import reduce


rule_re = re.compile(r'([a-z])([<>])(\d+):([a-zA-Z]+)|([a-zA-Z]+)')


def solve(input_file, p1=True):
    lines = read_lines(input_file, skip_empty=False)

    workflows = {}
    parts = []
    in_rules = True
    for line in lines:
        if not line:
            in_rules = False
            continue
        if in_rules:
            [label], rules = splits(line, ('[{}]', ','))
            workflows[label] = rules
        else:
            [ratings] = splits(line, ('[{}]', ',', '='))
            parts.append({a: int(r) for a, r in ratings})

    if p1:
        return follow_workflow(workflows, parts)
    else:
        return calc_accepted(workflows)


def follow_workflow(workflows, parts):
    accepted = Counter()
    for part in parts:
        workflow = workflows['in']
        while workflow:
            for rule in workflow:
                m = rule_re.match(rule)
                if m[5]:
                    w_next = m[5]
                else:
                    attr, comp, val = m[1], m[2], m[3]
                    if comp == '<' and part[attr] < int(val):
                        w_next = m[4]
                    elif comp == '>' and part[attr] > int(val):
                        w_next = m[4]
                    else:
                        continue

                if w_next == 'A':
                    accepted.update(part)
                    workflow = None
                    break
                elif w_next == 'R':
                    workflow = None
                    break
                else:
                    workflow = workflows[w_next]
                    break

    return sum(accepted.values())


def calc_accepted(workflows):
    root = build_tree('in', workflows)
    # print_tree(root)
    print('Node count:', root.node_count())
    return root.num_accepted()


def build_tree(label, workflows, condition=None):
    workflow = workflows[label]
    node = Node(label, condition)
    for rule in workflow:
        m = rule_re.match(rule)
        target = m[5] or m[4]
        if m[1]:
            child_condition = (m[1], m[2], int(m[3]))
        else:
            child_condition = None

        if target in ('A', 'R'):
            node.children.append(Node(target, child_condition))
        else:
            child = build_tree(target, workflows, child_condition)
            node.children.append(child)

    return node


def print_tree(node, indent=0):
    print(' ' * indent + str(node), sep='')
    for child in node.children:
        print_tree(child, indent + 2)


class Node:
    def __init__(self, label, condition):
        self.label = label
        self.condition = condition
        self.children = []

    def num_accepted(self, allowed=None):
        if not allowed:
            allowed = {c: set(range(1, 4001)) for c in 'xmas'}

        allowed_copy = {c: allowed[c].copy() for c in 'xmas'}
        if self.condition:
            attr, test, value = self.condition
            for i in range(1, 4001):
                if test == '<' and i < value or test == '>' and i > value:
                    allowed[attr].discard(i)
                else:
                    allowed_copy[attr].discard(i)

        if self.label == 'A':
            num_accepted = reduce(operator.mul, [len(s) for s in allowed_copy.values()])
        elif self.label == 'R':
            num_accepted = 0
        else:
            num_accepted = 0
            for child in self.children:
                num_accepted += child.num_accepted(allowed_copy)

        return num_accepted

    def node_count(self):
        return 1 + sum(n.node_count() for n in self.children)

    def __str__(self):
        if self.condition:
            attr, test, value = self.condition
            return f'{self.label} ({attr} {test} {value})'
        else:
            return self.label


def main():
    _input_file = 'input'
    expected = {
        'input': (330820, 123972546935551),
        'example': (19114, 167409079868000),
    }[_input_file]

    run(__file__, solve, _input_file, expected[0], p1=True)
    run(__file__, solve, _input_file, expected[1], p1=False)


if __name__ == '__main__':
    main()
