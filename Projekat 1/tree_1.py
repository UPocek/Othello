import queue_1
from Projekat1 import State


class Node(object):
    __slots__ = ['value', 'parent', 'children']

    def __init__(self, value, parent=None, children=None):
        self.value = value
        self.parent = parent
        if children is None:
            self.children = []
        else:
            self.children = [children]

    def __eq__(self, other):
        return self.value == other.value

    def is_root(self):
        return self.parent is None

    def is_leaf(self):
        return self.num_children() == 0

    def num_children(self):
        return len(self.children)

    def add_child(self, new):
        new.parent = self
        self.children.append(new)

    def __str__(self):
        return str(self.value)

    def __iter__(self):
        for child in self.children:
            yield child

    def deepcopy(self):
        value = State()
        self.value.calculate_board()
        white = self.value.white
        black = self.value.black
        i = 7
        j = 7
        while white != 0:
            if j < 0:
                i -= 1
                j = 7
            if white % 2 != 0:
                value.board[i][j] = 'w'
            white = white >> 1
            j -= 1

        i = 7
        j = 7
        while black != 0:
            if j < 0:
                i -= 1
                j = 7
            if black % 2 != 0:
                value.board[i][j] = 'b'
            black = black >> 1
            j -= 1
        new_node = Node(value)
        return new_node


class Tree(object):

    def __init__(self, root=None):
        self._root = root

    def is_empty(self):
        return self._root is None

    def depth(self, node):
        if node.parent is None:
            return 0
        return 1 + self.depth(node.parent)

    def preorder(self, func):
        self._preorder(self._root, func)

    def _preorder(self, node, func):
        func(node)
        for child in node.children:
            self._preorder(child, func)

    def postorder(self, func):
        self._postorder(self._root, func)

    def _postorder(self, node, func):
        for child in node.children:
            self._postorder(child, func)
        func(node)

    def breadth_first(self, func):
        queue = queue_1.Queue()
        queue.enqueue(self._root)
        while not queue.is_empty():
            current = queue.dequeue()
            func(current)
            for child in current:
                queue.enqueue(child)


if __name__ == '__main__':
    t = Tree()
