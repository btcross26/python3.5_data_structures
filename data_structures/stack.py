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
    def __init__(self, maxsize = None):
        self._maxsize = maxsize
        self._stack = DoubleLinkedList()
        
    def __repr__(self):
        return "Stack(maxsize={:s})".format(str(self._maxsize))
        
    def __iter__(self):
        for value in reversed(self._stack):
            yield value
        
    def __len__(self):
        return len(self._stack)
        
    def push(self, value):
        if self._maxsize is not None and len(self) == self._maxsize:
            raise FullError("<method>:push called on full Stack")
        self._stack.append(value)
        
    def pop(self, value):
        if self.empty():
            raise EmptyError("<method>:pop called on empty Stack")
        return self._stack.popback()
        
    def empty(self, value):
        return len(self) == 0
