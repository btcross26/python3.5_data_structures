class TreeNode(object):
    def __init__(self, key, parent = None, left = None, right = None):
        self.key = key
        self.parent = parent
        self.left = left
        self.right = right
        
    def __str__(self):
        return str(self.key)
        
    def __repr__(self):
        return self.__str__()
        
class BinaryTree(object):
    '''
    Binary search tree storing keys. Keys must be comparable objects.
    '''
    def __init__(self, keys = None):
        '''
        Constructor Arguments:
            keys : array-like
                List of keys to add to tree (optional)
        '''
        self.root = None
        keys = list() if keys is None else keys
        self.size = 0
        self.insert_multiple(keys)
            
    def __str__(self):
        return '<{:s} at {:s}>'.format(type(self).__name__, hex(id(self)))
        
    def __repr__(self):
        return self.__str__()
        
    def __len__(self):
        return self.size
            
    def __iter__(self):
        if self.root is None:
            return
            yield
        else:
            node = self._minimum(self.root)
            last_key = node.key
            yield node.key
            n = 1
            while n < self.size:
                if node.left and node.left.key > last_key:
                    node = node.left
                elif node.key > last_key:
                    n += 1
                    last_key = node.key
                    yield node.key
                elif node.right and node.right.key > last_key:
                    node = node.right
                else:
                    node = node.parent
            
    def __list__(self):
        return [value for value in self.__iter__()]
            
    def _search(self, key):
        '''
        Private method returns the node containing key if key is found,
        else returns None.
        
        Arguments:
            key : object
                Value to search for in the tree.
        '''
        node = self.root
        while node is not None and key != node.key:
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                break
        return node
        
    def clear(self):
        '''
        Removes all values from the tree.
        '''
        values = list(self)
        self.delete_multiple(values)
        self.root = None
        
    def empty(self):
        '''
        Returns True if the tree is empty, False otherwise.
        '''
        return self.size == 0
        
    def has_key(self, key):
        '''
        Returns True if the tree has the key, False otherwise.
        '''
        return self._search(key) is not None
        
    def height(self):
        '''
        Returns the height of a tree instance starting at the root of the
        tree. Returns 0 if the tree is empty.
        '''
        if self.root is None:
            return 0
        else:
            height = 0
            node_list = [self.root]
            while node_list:
                height += 1
                temp = list()
                for node in node_list:
                    if node.left:
                        temp.append(node.left)
                    if node.right:
                        temp.append(node.right)
                node_list = temp
        return height
        
    def _minimum(self, node):
        '''
        Private method that returns the minimum node of the tree with
        root equal to argument node.
        '''
        if node is None:
            return None
        else:
            while node.left is not None:
                node = node.left
            return node
            
    def minimum(self):
        '''
        Returns the minimum key in a tree instance (left most member key).
        '''
        node = self._minimum(self.root)
        return None if node is None else node.key
    
    def _maximum(self, node):
        '''
        Private method that returns the maximum node of the tree with
        root equal to the argument node.
        '''
        if node is None:
            return None
        else:
            while node.right is not None:
                node = node.right
            return node
            
    def maximum(self):
        '''
        Returns the maximum key in a tree instance (right most member key).
        '''
        node = self._maximum(self.root)
        return None if node is None else node.key
        
    def _successor(self, key):
        '''
        Private method that returns the successor node to the node
        containing value key in a tree instance. If key is not in any node,
        then None is returned.
        '''
        node = self._search(key)
        if node is None:
            return None
        elif node.right is not None:
            return self._minimum(node.right)
        temp = node.parent
        while temp is not None and node == temp.right:
            node = temp
            temp = node.parent
        return temp
        
    def successor(self, key):
        '''
        Returns the node value of the successor of the node containing
        value key in a tree instance. If key is not in any node, then
        a KeyError is raised.
        '''
        node = self._successor(key)
        if node is None:
            raise KeyError('BinaryTree object does not contain key:{:s}'.format(str(key)))
        else:
            return node.key
        
    def _predecessor(self, key):
        '''
        Private method that returns the predecessor node to the node
        containing value key in a tree instance. If key is not in any node,
        then None is returned.
        '''
        node = self._search(key)
        if node is None:
            return None
        elif node.left is not None:
            return self._maximum(node.left)
        temp = node.parent
        while temp is not None and node == temp.left:
            node = temp
            temp = node.parent
        return temp
                
    def predecessor(self, key):
        '''
        Returns the node value of the predecessor of the node containing
        value key in a tree instance. If key is not in any node, then
        a KeyError is raised.
        '''
        node = self._predecessor(key)
        if node is None:
            raise KeyError('BinaryTree object does not contain key:{:s}'.format(str(key)))
        else:
            return node.key
    
    def _create_node(self, key):
        '''
        A factory for creating nodes. This method can be over-ridden in
        derived classes to allow for new nodetypes. This makes it easier to
        create different types of data structures derived from trees
        without overhauling the base class insert method (e.g., a
        lookup table where keys are stored in a tree)
        '''
        return TreeNode(key)
                        
    def insert(self, key):
        '''
        Inserts a node containing value key into a tree instance. If no
        node containing key is located within the tree instance, then
        nothing happens.
        '''
        new_node = self._create_node(key)
        node1 = None
        node2 = self.root
        while node2 is not None:
            node1 = node2
            if key == node2.key:
                return
            elif key < node2.key:
                node2 = node2.left
            else:
                node2 = node2.right
        new_node.parent = node1
        if node1 is None:
            self.root = new_node
        elif key < node1.key:
            node1.left = new_node
        else:
            node1.right = new_node
        self.size += 1
                
    def insert_multiple(self, keylist):
        '''
        Inserts one node in a tree instance for each value contained in the
        iterable argument keylist. Calls on member method insert.
        '''
        for key in keylist:
            self.insert(key)
        
    def delete(self, key):
        '''
        Deletes a node containing value key into a tree instance. If no
        node containing key is located within the tree instance, then
        a KeyError is raised.
        '''
        node = self._search(key)
        if node is None:
            raise KeyError('BinaryTree object does not contain key:{:s}'.format(str(key)))
        if node.right is None and node.left is None:
            if node is self.root:
                self.root = None
            elif node.key < node.parent.key:
                node.parent.left = None
            else:
                node.parent.right = None                
        elif node.right is not None and node.left is None:
            if node is self.root:
                self.root = node.right
            elif node.key < node.parent.key:
                node.parent.left = node.right
            else:
                node.parent.right = node.right
            node.right.parent = node.parent
        elif node.right is None and node.left is not None:
            if node is self.root:
                self.root = node.left
            elif node.key < node.parent.key:
                node.parent.left = node.left
            else:
                node.parent.right = node.left
            node.left.parent = node.parent
        else:
            successor = self._successor(key)
            if node.right is not successor:
                successor.parent.left = None
                successor.right = node.right
                node.right.parent = successor
            successor.left = node.left
            successor.parent = node.parent
            if node is self.root:
                self.root = successor
        del node
        self.size -= 1
            
    def delete_multiple(self, keylist):
        '''
        Deletes one node in a tree instance for each value contained in the
        iterable argument keylist. Calls on member method 'delete'.
        '''
        try:
            for key in keylist:
                self.delete(key)
        except:
            raise
            
    def ge_key(self, key):
        pass
        
    def le_key(self, key):
        pass
            
class RedBlackNode(TreeNode):
    def __init__(self, key, color, parent = None, left = None, right = None):
        super().__init__(key, parent, left, right)
        if color not in ['r', 'b']:
            raise ValueError("arg color must be either 'r' or 'b'")
        self.color = color
    
class RedBlackTree(BinaryTree):
    def __init__(self, keys = None):
        super().__init__(keys)
        self.nil = RedBlackNode(None, 'b')
                        
    def _create_node(self, key):
        return RedBlackNode(key, 'r')
                
    def _left_rotate(self, node):
        y = node.right
        node.right = y.left
        if y.left is not None:
            y.left.parent = node
        y.parent = node.parent
        if node.parent is None:
            self.root = y
        elif node is node.parent.left:
            node.parent.left = y
        else:
            node.parent.right = y
        y.left = node
        node.parent = y
        
    def _right_rotate(self, node):
        y = node.left
        node.left = y.right
        if y.right is not None:
            y.right.parent = node
        y.parent = node.parent
        if node.parent is None:
            self.root = y
        elif node is node.parent.right:
            node.parent.right = y
        else:
            node.parent.left = y
        y.right = node
        node.parent = y
        
    def _rb_insert_fixup(self, node):
        while node is not self.root and node.parent.color == 'r':
            if node.parent is not self.root:
                if node.parent is node.parent.parent.left:
                    y = node.parent.parent.right
                    if y is not None and y.color == 'r':
                        node.parent.color = 'b'
                        y.color = 'b'
                        node.parent.parent.color = 'r'
                        node = node.parent.parent
                    else:
                        if node is node.parent.right:
                            node = node.parent
                            self._left_rotate(node)
                        node.parent.color = 'b'
                        node.parent.parent.color = 'r'
                        self._right_rotate(node.parent.parent)
                else:
                    y = node.parent.parent.left
                    if y is not None and y.color == 'r':
                        node.parent.color = 'b'
                        y.color = 'b'
                        node.parent.parent.color = 'r'
                        node = node.parent.parent
                    else:
                        if node is node.parent.left:
                            node = node.parent
                            self._right_rotate(node)
                        node.parent.color = 'b'
                        node.parent.parent.color = 'r'
                        self._left_rotate(node.parent.parent)
        self.root.color = 'b'
                        
    
    def insert(self, key):
        node = self._create_node(key)
        y = None
        x = self.root
        while x is not None:
            y = x
            if key == x.key:
                return
            elif key < x.key:
                x = x.left
            else:
                x = x.right
        node.parent = y
        if y is None:
            self.root = node
        elif node.key < y.key:
            y.left = node
        else:
            y.right = node
        self._rb_insert_fixup(node)
        self.size += 1
        
    def delete(self, keys):
        pass
