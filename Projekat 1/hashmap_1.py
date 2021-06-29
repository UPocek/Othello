class NotImplementedException(Exception):
    pass


import random


class MapElement(object):
    __slots__ = '_key', '_value'

    def __init__(self, key, value):
        self._key = key
        self._value = value

    @property
    def key(self):
        return self._key

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value


class Map(object):
    __slots__ = ['_data']

    def __init__(self):
        self._data = []

    def __getitem__(self, key):
        for item in self._data:
            if key == item.key:
                return item.value

        raise KeyError('Traženi el. ne postoji!')

    def __setitem__(self, key, value):
        for item in self._data:
            if key == item.key:
                item.value = value
                return

        self._data.append(MapElement(key, value))

    def __delitem__(self, key):
        length = len(self._data)
        for i in range(length):
            if key == self._data[i].key:
                self._data.pop(i)
                return

        raise KeyError('Traženi el. ne postoji!')

    def __len__(self):
        return len(self._data)

    def __contains__(self, key):
        for item in self._data:
            if key == item.key:
                return True
        return False

    def __iter__(self):
        for item in self._data:
            yield item.key

    def items(self):
        for item in self._data:
            yield item.key, item.value

    def keys(self):
        keys = []
        for key in self:
            keys.append(key)

        return keys

    def values(self):
        values = []
        for key in self:
            values.append(self[key])

        return values

    def clear(self):
        self._data = []


class HashMap(object):
    __slots__ = ['_data', '_capacity', '_size', 'prime', '_a', '_b']

    def __init__(self, capacity=99991):
        self._data = capacity * [None]
        self._capacity = capacity
        self._size = 0
        self.prime = 109345121

        self._a = 1 + random.randrange(self.prime - 1)
        self._b = random.randrange(self.prime)

    def __len__(self):
        return self._size

    def _hash(self, x):
        hashed_value = (hash(x) * self._a + self._b) % self.prime
        compressed = hashed_value % self._capacity
        return compressed

    def _resize(self, capacity):
        old_data = list(self.items())
        self._data = capacity * [None]
        self._size = 0

        for (k, v) in old_data:
            self[k] = v

    def __getitem__(self, key):
        bucket_index = self._hash(key)
        return self._bucket_getitem(bucket_index, key)

    def __setitem__(self, key, value):
        bucket_index = self._hash(key)
        self._bucket_setitem(bucket_index, key, value)

        current_capacity = len(self._data)
        if self._size > current_capacity // 2:
            self._resize(2 * current_capacity - 1)

    def __delitem__(self, key):
        bucket_index = self._hash(key)
        self._bucket_delitem(bucket_index, key)

    def items(self):
        raise NotImplementedException()

    def _bucket_getitem(self, index, key):
        raise NotImplementedException()

    def _bucket_setitem(self, index, key, value):
        raise NotImplementedException()

    def _bucket_delitem(self, index, key):
        raise NotImplementedException()


class ChainedHashMap(HashMap):
    def _bucket_getitem(self, i, key):
        bucket = self._data[i]
        if bucket is None:
            raise KeyError('Traženi el. ne postoji.')

        return bucket[key]

    def _bucket_setitem(self, bucket_index, key, value):
        bucket = self._data[bucket_index]
        if bucket is None:
            self._data[bucket_index] = Map()

        current_size = len(self._data[bucket_index])
        self._data[bucket_index][key] = value
        if len(self._data[bucket_index]) > current_size:
            self._size += 1

    def _bucket_delitem(self, bucket_index, key):
        bucket = self._data[bucket_index]
        if bucket is None:
            raise KeyError('Traženi el. ne postoji.')

        del bucket[key]
        self._size -= 1

    def __iter__(self):
        for bucket in self._data:
            if bucket is not None:
                for key in bucket:
                    yield key

    def items(self):
        for bucket in self._data:
            if bucket is not None:
                for key, value in bucket.items():
                    yield key, value


if __name__ == '__main__':
    pass
