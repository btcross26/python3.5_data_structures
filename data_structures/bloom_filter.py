import random

class BloomFilter(object):
    '''
    Simple BloomFilter implementation that utilizes random hash functions
    of the multiplicative type.
    '''
    
    def __init__(self, size, hashvector_length = 2, seed = None):
        '''
        Constructor Arguments
        ---------------------
        size: int
            Size of the bitvector to use in the implementation.
            
        hashvector_length: int (default: 2)
            Number of hash functions to use in determining a values
            hashvector.
            
        seed: hashable or None (default: None)
            A hashable value that can be used to set the random seed that is
            used in determining the randomized hash functions.
        '''
        self._size = int(size)
        self._bit_array = [False] * self._size          
        if seed is not None:
            random.seed(seed)
        self._A = [random.random() for i in range(hashvector_length)]
        self._num_inserts = 0
        
    def insert(self, value):
        '''
        Insert <arg>:value into the bloom filter. <arg>:value must be
        hashable.
        '''
        if not isinstance(value, int) and not isinstance(value, float):
            value = hash(value)
        for A in self._A:
            temp = A * value
            temp -= int(temp)
            index = int(self._size * temp)
            self._bit_array[index] = True
        self._num_inserts += 1
            
    def num_inserts(self):
        '''
        Returns the number of inserts that have been made into the instance.
        '''
        return self._num_inserts
        
    def bit_density(self):
        '''
        Returns the percentage of bits in the underlying bit vector that have
        been set to True.
        '''
        return sum(self._bit_array) / self._size
                    
    def has_hashvector(self, value):
        '''
        Returns True if the hashvector of <arg>:value is present in the
        instance bit vector. Otherwise, returns False.
        '''
        if not isinstance(value, int) and not isinstance(value, float):
            value = hash(value)
        for A in self._A:
            temp = A * value
            temp -= int(temp)
            index = int(self._size * temp)
            if not self._bit_array[index]:
                return False
        return True
