import math
from random import randint


MAX_PRIORITY = 99


class TreapNode:
    def __init__( self, item, left=None, right=None ):
        self.item = item
        self.left = left
        self.right = right
        self.priority = randint(0, MAX_PRIORITY)

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
