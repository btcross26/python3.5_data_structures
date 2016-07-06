class UnionFind(object):
    '''
    UnionFind implemented using weighted-quick-unionfind method.
    '''
    def __init__(self, n):
        self.count = n
        self.id = list(range(n))
        self.size = [1] * n
        
    def union(self, node1, node2):
        node1 = self.find(node1)
        node2 = self.find(node2)
        if node1 == node2:
            return
        if self.size[node1] < self.size[node2]:
            self.id[node1] = node2
            self.size[node2] += self.size[node1]
        else:
            self.id[node2] = node1
            self.size[node1] += self.size[node2]
        self.count -= 1
        
    def find(self, node):
        while node != self.id[node]:
            node = self.id[node]
        return node
        
    def connected(self, node1, node2):
        return self.find(node1) == self.find(node2)
        
    def cluster_count(self):
        return self.count