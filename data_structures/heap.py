class EmptyError(Exception):
    '''
    Exception raised when delete or peek operations are called on an
    empty heap.
    '''
    pass

class MinArrayHeap(object):
    '''
    Array-based minimum heap.
    '''
    def __init__(self):
        '''
        Private Instance Attributes:
            _keylist : list
                Stores keys currently in heap instance.
        '''
        self._keylist = list()
        
    def __str__(self):
        return '<{:s} at {:s}>'.format(type(self).__name__, hex(id(self)))
        
    def __repr__(self):
        return self.__str__()
        
    def __iter__(self):
        for value in self._keylist:
            yield value
            
    def __list__(self):
        return list(self._keylist)
        
    def __len__(self):
        return len(self._keylist)
        
    def _compare(self, key1, key2):
        '''
        Returns True if <arg>:key1 < <arg>:key2, False otherwise.
        '''
        return key1 < key2
        
    def _float_up(self, index):
        '''
        Key value located in self._keylist at index <arg>:index is floated
        towards the zero index as to maintain the heap invariant property.
        '''
        while index > 0 and self._compare(self._keylist[index], self._keylist[(index - 1) >> 1]):
            i = (index - 1) >> 1
            self._keylist[index], self._keylist[i] = self._keylist[i], self._keylist[index]
            index = i
            
    def _float_down(self, index):
        '''
        Key value located in self._keylist at index <arg>:index is floated
        towards the end of self._keylist as to maintain the heap invariant
        property.
        '''
        while len(self._keylist) > (index << 1) + 1:
            i = (index << 1) + 1
            if len(self._keylist) > i + 1 and self._compare(self._keylist[i + 1], self._keylist[i]):
                if self._compare(self._keylist[i + 1], self._keylist[index]):
                    self._keylist[index], self._keylist[i + 1] = self._keylist[i + 1], self._keylist[index]
                    index = i + 1
                else:
                    break
            elif self._compare(self._keylist[i], self._keylist[index]):
                self._keylist[index], self._keylist[i] = self._keylist[i], self._keylist[index]
                index = i
            else:
                break
                
    def peek(self):
        '''
        Returns the value of the head key in the heap without removing
        the key. Raises and EmptyError exception if the heap is empty.
        '''
        if not self._keylist:
            raise EmptyError('cannot call method peek() on empty heap instance')
        return self._keylist[0]
        
    def push(self, key):
        '''
        Adds <arg>:key to the heap instance.
        '''
        self._keylist.append(key)
        self._float_up(len(self._keylist) - 1)
        
    def push_multiple(self, keys):
        '''
        Pushes the key values in the iterable <arg>:keys onto a heap
        instance.
        '''
        for key in keys:
            self.push(key)
        
    def pop(self):
        '''
        Removes and returns the value at the head of the heap while
        maintaining the heap invariant.
        '''
        if not self._keylist:
            raise EmptyError('cannot call method pop() on empty heap instance')
        value = self.peek()
        self._delete(0)
        return value
        
    def pushpop(self, key):
        '''
        Pushes <arg>:key onto the heap and then proceeds to pop and return
        the key at the head of the heap.
        '''
        self.push(key)
        return self.pop()
        
    def _delete(self, index):
        '''
        Private method to delete the key at index <arg>:index of self._keylist.
        '''
        if index == 0 and len(self._keylist) == 1:
            self._keylist.pop()
        else:
            i = len(self._keylist) - 1
            self._keylist[index], self._keylist[i] = self._keylist[i], self._keylist[index]
            self._keylist.pop()
            self._float_down(index)
        
    def delete(self, key):
        '''
        Deletes <arg>:key from the heap instance. If the heap does not contain
        <arg>:key, raises a KeyError exception.
        '''
        try:
            index = self._keylist.index(key)
            self._delete(index)
            return
        except:
            pass
        raise KeyError(str(key))

    def clear(self):
        '''
        Empties the heap instance.
        '''
        self._keylist.clear()
    
class MaxArrayHeap(MinArrayHeap):
    '''
    Array-based maximum heap. Derived class of MinArrayHeap.
    '''
    def _compare(self, key1, key2):
        '''
        Returns True if <arg>:key1 > <arg>:key2, False otherwise.
        '''
        return key1 > key2 

class HeapNode(object):
    '''
    Node object for tree-based heap implementation.
    '''
    def __init__(self, key, parent = None, previous = None):
        self.key = key
        self.parent = parent
        self.left = None
        self.right = None
        self.p = previous
        self.n = None
        
class MinTreeHeap(object):
    '''
    Tree-based minimum heap.
    '''
    def __init__(self):
        '''
        Private Instance Attributes:
            _root : HeapNode
                Root node of heap instance
                
            _insert_parent : HeapNode
                Parent of next inserted HeapNode
                
            _back : HeapNode
                Last inserted HeapNode of the heap instance
                
            _size : int
                Current size of the heap instance
        '''
        self._root = None
        self._insert_parent = None
        self._back = None
        self._size = 0
        
    def __str__(self):
        return '<{:s} at {:s}>'.format(type(self).__name__, hex(id(self)))
        
    def __repr__(self):
        return self.__str__()
        
    def __iter__(self):
        node = self._root
        while node is not None:
            yield node.key
            node = node.n
            
    def __list__(self):
        return [value for value in self.__iter__()]
        
    def __len__(self):
        return self._size
        
    def _compare(self, key1, key2):
        '''
        Returns True is <arg>:key1 < <arg>:key2, False otherwise.
        '''
        return key1 < key2
        
    def _float_up(self, node):
        '''
        Key value located in <arg>:node is floated towards the root of the
        tree as to maintain the heap invariant property.
        '''
        while node.parent is not None and self._compare(node.key, node.parent.key):
            node.key, node.parent.key = node.parent.key, node.key
            node = node.parent
            
    def _float_down(self, node):
        '''
        Key value located in <arg>:node is floated towards the leaves of the
        tree as to maintain the heap invariant property.
        '''
        while node.left is not None:
            if node.right is not None and self._compare(node.right.key, node.left.key):
                if self._compare(node.right.key, node.key):
                    node.key, node.right.key = node.right.key, node.key
                    node = node.right
                else:
                    break
            elif self._compare(node.left.key, node.key):
                node.key, node.left.key = node.left.key, node.key
                node = node.left
            else:
                break    
                
    def peek(self):
        '''
        Returns the value of the head key in the heap without removing
        the key. Raises and EmptyError exception if the heap is empty.
        '''
        if self._root is None:
            raise EmptyError('cannot call method peek() on empty heap instance')
        return self._root.key
        
    def push(self, key):
        '''
        Adds <arg>:key to the heap instance.
        '''
        node = HeapNode(key, previous = self._back)
        if self._root is None:
            self._root = node
            self._insert_parent = node
            self._back = node
        else:
            node.parent = self._insert_parent
            if self._insert_parent.left is None:
                self._insert_parent.left = node
            else:
                self._insert_parent.right = node
                self._insert_parent = self._insert_parent.n
            self._back.n = node
            node.p = self._back
            self._back = node
            self._float_up(node)
        self._size += 1
        
    def push_multiple(self, keys):
        '''
        Pushes the key values in the iterable <arg>:keys onto a heap
        instance.
        '''
        for key in keys:
            self.push(key)
        
    def pop(self):
        '''
        Removes and returns the value at the head of the heap while
        maintaining the heap invariant.
        '''
        try:
            value = self.peek()
            self._delete(self._root)
            return value
        except:
            pass
        raise EmptyError('cannot call method pop() on empty heap instance')
        
    def pushpop(self, key):
        '''
        Pushes <arg>:key onto the heap and then proceeds to pop and return
        the key at the head of the heap.
        '''
        self.push(key)
        return self.pop()
        
    def _delete(self, node):
        '''
        Private method to delete the key in <arg>:node from the heap tree
        instance.
        '''
        if node is self._root and self._size == 1:
            self._root = None
            self._insert_parent = None
            self._back = None
        else:
            node.key, self._back.key = self._back.key, node.key
            if self._back is self._back.parent.left:
                self._back.parent.left = None
            else:
                self._back.parent.right = None
            self._back.p.n = None
            self._back = self._back.p
            self._float_down(node)                       
            if self._insert_parent is not self._root and self._insert_parent.p.right is None:
                self._insert_parent = self._insert_parent.p
        self._size -= 1
        
    def delete(self, key):
        '''
        Deletes <arg>:key from the heap instance. If the heap does not contain
        <arg>:key, raises a KeyError exception.
        '''
        node = self._root
        while node is not None:
            if node.key == key:
                break
            node = node.n
        if node is None:
            raise KeyError(str(key))
        else:
            self._delete(node)

    def clear(self):
        '''
        Empties the heap instance.
        '''
        self._root = None
        self._insert_parent = None
        self._back = None
        self._size = 0
                
class MaxTreeHeap(MinTreeHeap):
    '''
    Tree-based maximum heap. Derived class of MinTreeHeap.
    '''
    def _compare(self, key1, key2):
        '''
        Returns True if <arg>:key1 > <arg>:key2, False otherwise.
        '''
        return key1 > key2

            