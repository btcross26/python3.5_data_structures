import random

class BloomFilter(object):
    def __init__(self, size, hashvector_length = 2, seed = None):
        self._size = int(size)
        self._bit_array = [False] * self._size            
        if seed is not None:
            random.seed(seed)
        self._A = [random.random() for _ in range(hashvector_length)]
        
    def put(self, value):
        if isinstance(value, str):
            value = hash(value)
        for A in self._A:
            temp = A * value
            temp -= int(temp)
            index = int(self._size * temp)
            self._bit_array[index] = True
                    
    def has_hashvector(self, value):
        if isinstance(value, str):
            value = hash(value)
        for A in self._A:
            temp = A * value
            temp -= int(temp)
            index = int(self._size * temp)
            if not self._bit_array[index]:
                return False
        return True
