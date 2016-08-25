from . import DoubleLinkedList

class EmptyError(Exception):
    '''
    Exception raised when pop operations are called on an empty stack.
    '''
    pass
    
class FullError(Exception):
    '''
    Exception raised when push operation is called on a full stack with
    specified maxsize constructor argument.
    '''
    pass
    
class Stack(object):
    '''
    Class Stack implements stack functionality using an underlying instance
    of a DoubleLinkedList.
    '''
    def __init__(self, maxsize = None):
        '''
        Constructor Arguments
        ---------------------
        maxsize: int
            Maximum capacity of the stack instance.
        '''
        self._maxsize = maxsize
        self._stack = DoubleLinkedList()
        
    def __str__(self):
        return list(self).__str__()
        
    def __repr__(self):
        return "Stack(maxsize={:s})".format(str(self._maxsize))
        
    def __iter__(self):
        for value in reversed(self._stack):
            yield value
        
    def __len__(self):
        return len(self._stack)
        
    def max_capacity(self):
        '''
        Returns the max capacity of the Stack instance if specified. If the
        max capacity if not limited, returns -1.
        '''
        if self._maxsize is not None:
            return self._maxsize
        else:
            return -1
        
    def push(self, value):
        '''
        Pushes value onto the Stack instance. If the maximum capacity of the
        stack is limited, raises a FullError.
        '''
        if self._maxsize is not None and len(self) == self._maxsize:
            raise FullError("<method>:push called on full Stack")
        self._stack.append(value)
        
    def pop(self):
        '''
        Pops and returns the next Stack instance value. If the Stack instance
        is empty, raised an EmptyError.
        '''
        if self.empty():
            raise EmptyError("<method>:pop called on empty Stack")
        return self._stack.popback()
        
    def empty(self):
        '''
        Returns True if the Stack instance is empty, False otherwise.
        '''
        return len(self) == 0
