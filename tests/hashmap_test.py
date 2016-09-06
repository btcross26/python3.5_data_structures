import unittest
from data_structures import Hashmap

class HashmapTest(unittest.TestCase):        
    def test_insertion_and_deletion(self):
        hashmap = Hashmap(buckets = 10, load_factor = 0.75,
                          resizing_factor = 2.00)
                          
        # insertion
        for i in range(5):
            hashmap[i] = i
            self.assertEqual(i, hashmap[i], "insertion error")
            self.assertIn(i, hashmap, "__contains__ error")
            self.assertEqual(i + 1, len(hashmap), "insertion __len__ error")
                    
        # check that resizing has not occurred (load factor not yet achieved)
        self.assertEqual(len(hashmap._array), 10, "resizing mistakenly occurred")
        
        # deletion
        for i in range(4, -1, -1):
            hashmap.delete(i)
            self.assertRaises(KeyError, hashmap.__getitem__, i)
            self.assertNotIn(i, hashmap, "__contains__ error after deletion")
            self.assertEqual(i, len(hashmap), "deletion __len__ error")
        
    def test_resizing_effect_and_duplicate_insertion(self):
        hashmap = Hashmap(buckets = 5, load_factor = 0.75,
                          resizing_factor = 2.00)
                          
        # test initial array size
        self.assertEqual(len(hashmap._array), 5, "initial sizing error in __init__")
        
        # insert 4 elements to surpass load factor
        for i in range(4):
            hashmap[i] = i
        self.assertEqual(len(hashmap._array), 10, "resizing error 5 to 10")
        
        # duplicate insert elements plus 4 more to surpass load factor again
        for i in range(8):
            hashmap[i] = i
        self.assertEqual(len(hashmap._array), 20, "resizing error 10 to 20")
        
        # check __len__
        self.assertEqual(len(hashmap), 8, "__len__ error after resizing 10 to 20")
        
        # check all values in hashmap after resizing
        for i in range(8):
            self.assertIn(i, hashmap, "__contains__ error after resizing 10 to 20")
            
        # _array size should remain constant at deletion
        for i in range(8):
            hashmap.delete(i)
        self.assertEqual(len(hashmap._array), 20, "resize error after deletion")
        
    def test_iteration(self):
        hashmap = Hashmap(buckets = 10)
        kv_pairs = [(0, 0), (1, 2), (2, 4), (3, 6)]
        for i in range(4):
            hashmap[i] = 2 * i
            
        # test hashmap.__iter__
        alist = sorted([value for value in hashmap])
        self.assertEqual(alist, kv_pairs, "problem with __iter__ method")
        
        # test hashmap.iteritems
        alist = sorted([value for value in hashmap.iteritems()])
        self.assertEqual(alist, kv_pairs, "problem with iteritems method")
        
        # test hashmap.iterkeys
        keys = [key for key, value in kv_pairs]
        alist = sorted([value for value in hashmap.iterkeys()])
        self.assertEqual(alist, keys, "problem with iterkeys method")
        
        # test hashmap.itervalues
        values = [value for key, value in kv_pairs]
        alist = sorted([value for value in hashmap.itervalues()])
        self.assertEqual(alist, values, "problem with itervalues method")
            
if __name__ == "__main__":
    unittest.main()