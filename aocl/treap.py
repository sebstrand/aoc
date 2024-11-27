import math
from random import random


MAX_PRIORITY = 99


class TreapNode:
    def __init__( self, item, left=None, right=None ):
        self.item = item
        self.left = left
        self.right = right
        self.priority = int(random() * MAX_PRIORITY)

    def insert(self, node):
        if node.item < self.item:
            if self.left:
                self.left, result = self.left.insert(node)
            else:
                self.left = node
                result = True
            return self._rotate_left_child(), result
        elif node.item > self.item:
            if self.right:
                self.right, result = self.right.insert(node)
            else:
                self.right = node
                result = True
            return self._rotate_right_child(), result
        # else duplicate; no change
        return self, False

    def remove(self, item):
        new_self = self
        result = False
        if item == self.item:
            self.priority = math.inf
            if self.left and (not self.right or self.left.priority < self.right.priority):
                new_self = self._rotate_left_child()
                new_self, result = new_self.remove(item)
            elif self.right:
                new_self = self._rotate_right_child()
                new_self, result = new_self.remove(item)
            else:
                new_self, result = None, True
        elif item < self.item:
            if self.left:
                self.left, result = self.left.remove(item)
        elif item > self.item:
            if self.right:
                self.right, result = self.right.remove(item)
        return new_self, result

    def print( self, level=0, label='' ):
        print(' ' * level, label, self.item, f' ({self.priority})', sep='')
        if self.left: self.left.print(level + 2, label='l:')
        if self.right: self.right.print(level + 2, label='r:')

    def _rotate_left_child(self):
        child = self.left
        if child.priority < self.priority:
            self.left = child.right
            child.right = self
            return child
        return self

    def _rotate_right_child(self):
        child = self.right
        if child.priority < self.priority:
            self.right = child.left
            child.left = self
            return child
        return self

    def __iter__(self):
        if self.left: yield from self.left
        yield self.item
        if self.right: yield from self.right

    def reverse_iter(self):
        if self.right: yield from self.right.reverse_iter()
        yield self.item
        if self.left: yield from self.left.reverse_iter()

    def __repr__(self):
        return f'TreapNode(item={self.item} prio={self.priority})'


class Treap:
    """Implements a Treap; a type of binary search tree.

    >>> t = Treap().insert(5).insert(1).insert(9).insert(12).insert(12).remove(9)
    >>> (t.min(), t.max(), t.size, t.has(9), t.has(5))
    (1, 12, 3, False, True)
    """

    def __init__( self ):
        self.root = None
        self._size = 0

    @property
    def size(self):
        return self._size

    def insert(self, item):
        node = TreapNode(item)
        if self.root is None:
            self.root = node
            self._size += 1
        else:
            self.root, result = self.root.insert(node)
            if result:
                self._size += 1
        return self

    def remove(self, item):
        if self.root:
            self.root, result = self.root.remove(item)
            if result:
                self._size -= 1
        return self

    def min(self):
        node = last = self.root
        while node:
            last = node
            node = node.left
        if last:
            return last.item

    def max(self):
        node = last = self.root
        while node:
            last = node
            node = node.right
        if last:
            return last.item

    def has(self, item):
        return self._find(item) is not None

    def print( self ):
        print(f'Treap(size={self._size})')
        if self.root:
            self.root.print(level=2, label='r:')

    def _find(self, item):
        node = self.root
        while node:
            if node.item == item:
                return item
            elif item < node.item:
                node = node.left
            else:
                node = node.right

    def __len__(self):
        return self._size

    def __iter__(self):
        if self.root:
            yield from self.root.__iter__()

    def reverse_iter(self):
        if self.root:
            yield from self.root.reverse_iter()

    def __repr__(self):
        return f'Treap(size={self.size} root={self.root})'


class IntervalTreapNode:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.priority = int(random() * MAX_PRIORITY)
        self.left = None
        self.right = None

    @property
    def size(self):
        size = 1
        if self.left:
            size += self.left.size
        if self.right:
            size += self.right.size
        return size

    def insert(self, start, end):
        # print('insert', node, 'into', self)
        if end < self.start:
            return self._insert_left(start, end)
        elif start > self.end:
            return self._insert_right(start, end)
        else: # there is overlap
            start_diff = start - self.start
            end_diff = end - self.end
            # print({'start_diff': start_diff, 'end_diff': end_diff})

            if start_diff >= 0 >= end_diff:
                # fully contained, no change needed
                return self

            fits_left = start_diff >= 0 or not self.left or start > self.left.max()[1]
            fits_right = end_diff <= 0 or not self.right or end < self.right.min()[0]

            if fits_left:
                if fits_right:
                    # can modify self to cover new interval
                    self.start = min(self.start, start)
                    self.end = max(self.end, end)
                    return self
                else: # extends too far right
                    # reduce to non-overlapping right part and insert right
                    return self._insert_right(self.end + 1, end)
            elif fits_right:
                # reduce to non-overlapping left part and insert left
                return self._insert_left(start, self.start - 1)
            else: # doesn't fit on either side, must split in half
                new_self = self._insert_left(start, self.start - 1)
                return new_self._insert_right(self.end + 1, end)

    def _insert_left(self, start, end):
        if self.left:
            self.left = self.left.insert(start, end)
        else:
            self.left = IntervalTreapNode(start, end)
        return self._rotate_left_child()

    def _insert_right(self, start, end):
        if self.right:
            self.right = self.right.insert(start, end)
        else:
            self.right = IntervalTreapNode(start, end)
        return self._rotate_right_child()

    def min(self):
        node = last = self
        while node:
            last = node
            node = node.left
        if last:
            return last.start, last.end

    def max(self):
        node = last = self
        while node:
            last = node
            node = node.right
        if last:
            return last.start, last.end

    def print( self, level=0, label='' ):
        print(f'{" " * level} {label} ({self.start},{self.end}) p{self.priority}', sep='')
        if self.left: self.left.print(level + 2, label='l:')
        if self.right: self.right.print(level + 2, label='r:')

    def _rotate_left_child(self):
        child = self.left
        if child.priority < self.priority:
            self.left = child.right
            child.right = self
            return child
        return self

    def _rotate_right_child(self):
        child = self.right
        if child.priority < self.priority:
            self.right = child.left
            child.left = self
            return child
        return self

    def __iter__(self):
        if self.left: yield from self.left
        yield self.start, self.end
        if self.right: yield from self.right

    def reverse_iter(self):
        if self.right: yield from self.right.reverse_iter()
        yield self.start, self.end
        if self.left: yield from self.left.reverse_iter()

    def __repr__(self):
        return f'IntervalTreapNode[({self.start},{self.end}) p{self.priority}]'


class IntervalTreap:
    """Implements an IntervalTreap."""

    def __init__( self ):
        self.root = None

    @property
    def size(self):
        if self.root:
            return self.root.size
        return 0

    def clear(self):
        self.root = None

    def insert(self, start, end):
        if self.root is None:
            self.root = IntervalTreapNode(start, end)
        else:
            self.root = self.root.insert(start, end)
        return self

    def remove(self, start, end):
        if self.root:
            self.root = self.root.remove(start, end)
        return self

    def min(self):
        if self.root:
            return self.root.min()

    def max(self):
        if self.root:
            return self.root.max()

    def print( self ):
        print(f'IntervalTreap(size={self.size})')
        if self.root:
            self.root.print(level=2, label='r:')

    def __len__(self):
        return self.size

    def __iter__(self):
        if self.root:
            yield from self.root.__iter__()

    def reverse_iter(self):
        if self.root:
            yield from self.root.reverse_iter()

    def __repr__(self):
        return f'IntervalTreap[size={self.size} root={self.root}]'


if __name__ == '__main__':
    from random import seed
    seed(123)

    t = IntervalTreap()
    t.root = IntervalTreapNode(10, 15)
    t.root.priority = 0

    t.root.left = IntervalTreapNode(2, 4)
    t.root.left.priority = 10

    t.root.left.left = IntervalTreapNode(0, 0)
    t.root.left.left.priority = 15

    t.root.left.right = IntervalTreapNode(6, 8)
    t.root.left.right.priority = 20

    t.root.right = IntervalTreapNode(18, 20)
    t.root.right.priority = 30

    t.print()

    # data = 3, 19
    # print('\ninserting', data)
    # t.insert(*data)
    # t.print()

    data = []
    for i in range(40):
        start = int(random() * 50)
        end = start + int(random() * 8)
        data.append((start, end))

    t = IntervalTreap()
    def treap_insert(t):
        for d in data:
            t.insert(*d)
        lst = list(iter(t))
        t.clear()
        return lst

    def intervals_insert(i):
        for d in data:
            i.add(*d)
        return list(iter(i))

    number = 100000

    import timeit
    # print('t:', timeit.timeit(
    #     'treap_insert(t)',
    #     setup='from __main__ import IntervalTreap, treap_insert; t=IntervalTreap()',
    #     number=number))
    # print('i:', timeit.timeit(
    #     'intervals_insert(i)',
    #     setup='from __main__ import intervals_insert; from aocl.interval import Intervals; i=Intervals()',
    #     number=number))

    import cProfile
    from pstats import SortKey
    cProfile.run('for i in range(number): treap_insert(t)', sort=SortKey.CUMULATIVE)
