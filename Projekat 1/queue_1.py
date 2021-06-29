class EmptyQueueException(Exception):
    pass


class Queue(object):

    def __init__(self, capacity=100):
        self._front = 0
        self._size = 0
        self.items = [None] * capacity

    def __len__(self):
        return self._size

    def is_empty(self):
        return self._size == 0

    def first(self):
        if self.is_empty():
            raise EmptyQueueException
        return self.items[self._front]

    def _resize(self, n):
        old = self.items
        self.items = [None] * n
        x = self._front
        for k in range(self._size):
            self.items[k] = old[x]
            x = (x + 1) % len(old)
        self._front = 0

    def enqueue(self, item):
        if self._size == len(self.items):
            self._resize(2 * (len(self.items)))
        x = (self._size + self._front) % len(self.items)
        self.items[x] = item
        self._size += 1

    def dequeue(self):
        if self.is_empty():
            raise EmptyQueueException
        x = self.items[self._front]
        self.items[self._front] = None
        self._front = (self._front + 1) % len(self.items)
        self._size -= 1
        return x


if __name__ == '__main__':
    q1 = Queue()
