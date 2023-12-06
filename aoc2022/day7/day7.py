from aocl import *
from collections import Counter


def main():
    lines = read_lines('input')

    sizes = Counter()
    path = []
    for line in lines:
        if line.startswith('$ '):
            command = line[2:]
            if command.startswith('cd'):
                loc = command[3:]
                if loc == '/':
                    path = []
                elif loc == '..':
                    path.pop()
                else:
                    path.append(loc)
                print('path', path)
        elif line.startswith('dir'):
            pass
        else:
            size, filename = line.split(' ')
            size = int(size)
            print('size', int(size), 'for', filename, 'in', path)
            for loc in path:
                sizes[loc] += size
            sizes[''] += size

    for loc in sizes:
        if sizes[loc] <= 100000:
            print('size', loc, sizes[loc])
    sizes_below = [size for size in sizes.values() if size <= 100000]
    size_sum = sum(sizes_below)
    print('sum of sizes below:', size_sum)
    assert size_sum > 1598125


class Node:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent

    def add_child(self, child):
        pass

if __name__ == '__main__':
    main()
