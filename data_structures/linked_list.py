# work in progress

class EmptyError(Exception):
    '''
    Exception raised when pop operations are called on an empty list.
    '''
    pass

class SingleLink(object):
    def __init__(self, value, next = None):
        self._value = value
        self._next = next
        
class SingleLinkedList(object):
    def __init__(self):
        self._root = None
        self._end = None
        self._size = 0
        
    def __str__(self):
        return list(self).__str__()
        
    def __repr__(self):
        return list(self).__repr__()
        
    def __iter__(self):
        link = self._root
        while link is not None:
            yield link._value
            link = link._next
            
    def __len__(self):
        return self._size
        
    def __getitem__(self, key):
        if self._size == 0:
            raise EmptyError("cannot index an empty linked list")
        if key == -1 or key == self._size - 1:
            return self._end._value
        else:
            for index, value in enumerate(self):
                if index == key:
                    return value
        raise IndexError("{:s}".format(str(key)))
                            
    def _create_new_link(self, value, next = None):
        return SingleLink(value, next)
                
    def append(self, value):
        new_link = self._create_new_link(value)
        if self._root is None:
            self._root = new_link
        else:
            self._end._next = new_link
        self._end = new_link
        self._size += 1
        
    def extend(self, value_list):
        for value in value_list:
            self.append(value)
        
    def prepend(self, value):
        new_link = self._create_new_link(value, self._root)
        self._root = new_link
        if self._end is None:
            self._end = new_link
        self._size += 1
            
    def front_extend(self, value_list):
        for value in reversed(value_list):
            self.prepend(value)
            
    def popfront(self):
        if self._root is None:
            raise EmptyError("<method>:popfront called on empty linked list")
        link = self._root
        if link is self._end:
            self._end = None
        self._root = self._root._next
        value = link._value
        del link
        self._size -= 1
        return value
        
    def index(self, value):
        for index, x in enumerate(self):
            if x == value:
                return index
        raise ValueError("{:s} is not in list".format(str(value)))
            
class DoubleLink(SingleLink):
    def __init__(self, value, next = None, previous = None):
        super(DoubleLink, self).__init__(value, next)
        self._previous = previous
        
class DoubleLinkedList(SingleLinkedList):
    def __init__(self):
        super(DoubleLinkedList, self).__init__()
        
    def _create_new_link(self, value, next = None, previous = None):
        return DoubleLink(value, next, previous)
        
    def append(self, value):
        link = self._end
        super(DoubleLinkedList, self).append(value)
        self._end._previous = link
        
    def prepend(self, value):
        super(DoubleLinkedList, self).prepend(value)
        if self._root._next:
            self._root._next._previous = self._root

    def popfront(self):
        value = super(DoubleLinkedList, self).popfront()
        if self._root:
            self._root._previous = None
        return value
        
    def popback(self):    
        if self._root is None:
            raise EmptyError("<method>:popback called on empty linked list")
        link = self._end
        if link is self._root:
            self._root = None
        else:
            link._previous._next = None
        self._end = link._previous
        value = link._value
        del link
        self._size -= 1
        return value
        
    def insert(self, index, value):
        if index >= self._size:
            self.append(value)
        elif index == 0:
            self.prepend(value)
        else:
            i = 1
            link = self._root._next
            while link is not None:
                if i == index:
                    plink = link._previous
                    proot = self._root
                    self._root = link
                    self.prepend(value)
                    self._root._previous = plink
                    plink._next = self._root
                    self._root = proot
                    break
                else:
                    link = link._next
                    i += 1
                
    def remove(self, value):
        link = self._root
        while link is not None:
            if link._value == value:
                if link._previous is not None:
                    link._previous._next = link._next
                if link._next is not None:
                    link._next._previous = link._previous
                if link is self._root:
                    self._root = link._next
                if link is self._end:
                    self._end = link._previous
                del link
                self._size -= 1
                return
            link = link._next
        raise ValueError("{:s} is not in list".format(str(value)))
        