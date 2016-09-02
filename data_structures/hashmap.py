import random
from . import DoubleLinkedList

class Hashmap(object):
    '''
    Simple hashmap object that utilizes a hashfunction of the multiplicative
    type and allows for custom sizing/resizing of the underlying array.
    Collisions are handled by simple chaining. The class can be considered a
    'friend' class (in c++ lingo) of DoubleLinkedList as it accesses DLL
    'private' attributes.
    '''
    def __init__(self, buckets = 8191, load_factor = 0.75, \
                 resizing_factor = 1.99, seed = None):
        '''
        Constructor Parameters
        ----------------------
        buckets: int
            Number of buckets to hash to in the underlying array.
            
        load_factor: float between 0.0 and 1.0
            Load factor at which to trigger a dynamic resizing. The load
            factor in this case is taken simply as the ratio of keys
            to buckets. (default 0.75)
        
        resizing_factor: float greater than 1.0
            Factor at which to increase the capacity of the underlying array.
            (default 1.99). Full transfer is performed at resizing.
            
        seed: hashable
            Seed for the random number generator used in setting the hash
            function. An identical seed can be used across runs to provide
            the same hash function.
        '''
        self._array = [None] * int(buckets)
        self._load_factor = load_factor
        self._resizing_factor = resizing_factor
        self._size = 0
        if seed is not None:
            random.seed(seed)
        self._A = random.random()
        
    def __len__(self):
        return self._size
        
    def __iter__(self):
        '''
        Yields items of a hashmap instance as tuple (key, value) pairs. This
        is the same as <method>:iteritems.
        '''
        for bucket in self._array:
            if bucket is not None:
                for value in bucket:
                    yield value
                             
    def iteritems(self):
        '''
        Yields items of a hashmap instance as tuple (key, value) pairs.
        '''
        for value in self:
            yield value
        
    def iterkeys(self):
        '''
        Yields keys of a hashmap instance.
        '''
        for value in self:
            yield value[0]
        
    def itervalues(self):
        '''
        Yields values of a hashmap instance.
        '''
        for value in self:
            yield value[1]
            
    def _resize(self):
        '''
        Resize the underlying array by a factor of _resizing_factor.
        '''
        old_array = self._array
        self._array = [None] * int(len(old_array) * self._resizing_factor)
        self._size = 0
        for index, bucket in enumerate(old_array):
            if bucket is not None:
                for value in bucket:
                    self.__setitem__(value[0], value[1])
                old_array[index] = None
        del old_array
                            
    def _finditem(self, key):
        '''
        Helper function that returns a (int, DoubleLink object) from a
        DoubleLinkedList if a (key, value) tuple pair is found in the list.
        The first int in the tuple corresponds to the bucket in which the
        key would be hashed in the underlying hashmap array. If no
        (key, value) pair is found, returns (int, None), where again int
        corresponds to the bucket in which the key would be hashed.
        '''
        temp = hash(key) * self._A
        index = int((temp - int(temp)) * len(self._array))
        if self._array[index] is not None:
            link = self._array[index]._root # accessing LL private attr
            while link is not None:
                k, value = link._value
                if k == key:
                    return index, link
                link = link._next
        return index, None
        
    def __getitem__(self, key):
        '''
        Returns the value corresponding to key in a hashmap instance. If no
        such key is found, raises a KeyError exception.
        '''
        _, itemlink = self._finditem(key)
        if itemlink is not None:
            return itemlink._value[1]
        else:
            raise KeyError("{:s}".format(str(key)))
                
    def __setitem__(self, key, value):
        '''
        Inserts a (key, value) tuple pair into a hashmap instance.
        '''
        bucket, itemlink = self._finditem(key)
        if itemlink is not None:
            itemlink._value = (key, value)
            return
        else:
            if self._array[bucket] is None:
                self._array[bucket] = DoubleLinkedList()
            self._array[bucket].append((key, value))
            self._size += 1
            if self._size / len(self._array) >= self._load_factor:
                self._resize()
                
    def __contains__(self, key):
        if self._finditem(key)[1] is None:
            return False
        else:
            return True
        
    def delete(self, key):
        '''
        Deletes the (key, value) tuple pair in a hashmap instance. If no such
        key exists in the hashmap, then raises a KeyError exception.
        '''
        bucket, itemlink = self._finditem(key)
        if itemlink is not None:
            self._array[bucket].remove(itemlink._value)
            if len(self._array[bucket]) == 0:
                self._array[bucket] = None
            self._size -= 1
        else:
            raise KeyError("{:s}".format(str(key)))
