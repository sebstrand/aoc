import math

from aocl import *


def solve(input_file, p1=True):
    lines = read_lines(input_file)

    root = Node('/')
    path = [root]
    for line in lines:
        if line.startswith('$ '):
            command = line[2:]
            if command.startswith('cd'):
                loc = command[3:]
                if loc == '/':
                    path = [root]
                elif loc == '..':
                    path.pop()
                    assert len(path) > 0
                else:
                    path.append(path[-1].get_child(loc))
                # print('path', path)
        elif line.startswith('dir'):
            path[-1].add_child(Node(line[4:]))
        else:
            size, filename = line.split(' ')
            size = int(size)
            path[-1].add_child(Node(filename, is_dir=False, size=size))
            # print('size', int(size), 'for', filename, 'in', path)

    # print('\nfs:')
    # print_tree(root)

    collected_dirs = []

    def collect_dirs_between(node, _, min_size, max_size):
        if node.is_dir and min_size <= node.size <= max_size:
            collected_dirs.append(node)

    traverse_tree(root, lambda node, level: collect_dirs_between( node, level, 0, 100000))
    if p1:
        return sum(d.size for d in collected_dirs)

    collected_dirs = []
    disk_space = 70000000
    required_free_space = 30000000
    # print('root size:', root.size)
    available_space = disk_space - root.size
    space_to_free = required_free_space - available_space
    # print('space to free:', space_to_free)
    traverse_tree(root, lambda node, level: collect_dirs_between( node, level, space_to_free, math.inf))
    # print('deletion candidate dirs:', collected_dirs)
    collected_dirs.sort(key=lambda node: node.size)
    dir_to_delete = collected_dirs[0]
    # print('dir to delete:', dir_to_delete)
    return dir_to_delete.size


class Node:
    def __init__(self, name, is_dir=True, size=0):
        self.name = name
        self.is_dir = is_dir
        self._size = size
        self.parent = None
        self.children = []

    def add_child(self, child):
        assert self.is_dir
        child.parent = self
        self.children.append(child)

    def get_child(self, name):
        assert self.is_dir
        return next(c for c in self.children if c.name == name)

    @property
    def size(self):
        if self.is_dir:
            return sum(child.size for child in self.children)
        else:
            return self._size

    def __repr__(self):
        type_name = ('file', 'dir')[self.is_dir]
        return f'{type_name}<{self.name}, size={self.size}>'


def traverse_tree(node, handler, level=0):
    handler(node, level)
    for child in node.children:
        traverse_tree(child, handler, level + 4)


def print_tree(node):
    traverse_tree(node, node_printer)


def node_printer(node, level=0):
    print(' ' * level, end='')
    type_name = ('file', 'dir')[node.is_dir]
    print(node.name, f'{type_name}, size={node.size})')


def main():
    _input_file = 'input'
    expected = {
        'input': (1908462, 3979145),
        'example': (95437, 24933642),
    }[_input_file]

    run(__file__, solve, _input_file, expected[0], p1=True)
    run(__file__, solve, _input_file, expected[1], p1=False)


if __name__ == '__main__':
    main()
