import unittest
from nodeClass import Node

class TestNodeClass(unittest.TestCase):

    # Test indexing capabilities of node. __getitem__ and __setitem__
    def test_indexing(self):
        n = Node(None, 'a', False)
        n['a'] = n
        n[1] = n
        self.assertIs(n[0], n['a'])
        self.assertIs(n[1], n['b'])

    # Test correct looping capabilitiies __iter__
    def test_iterating(self):
        n1 = Node(None, 'r', False)
        n2 = Node(None, 'a', True)
        n3 = Node(None, 'c', True)
        n1['a'] = n2
        n1['c'] = n3
        le = [n2, None, n3]+[None for x in range(23)] # Expected
        l = []
        for x in n1:
            l.append(x)
        self.assertEqual(le, l)

    # Test correct __eq__ method
    def test_eq(self):
        # Grandparent, parent, child, baby (level 0, 1, 2, 3)
        # Tree 1
        gp1 = Node(None, 'a', False)
        p1 = Node(None, 'b', False)
        c11 = Node(None, 'c', False)
        c12 = Node(None, 'd', False)
        b11 = Node(None, 'e', False)
        b12 = Node(None, 'f', False)
        gp1[0] = p1
        p1[0], p1[1] = c11, c12
        c11[0], c11[1] = b11, b12
        # Tree 2
        gp2 = Node(None, 'a', False)
        p2 = Node(None, 'b', False)
        c21 = Node(None, 'c', False)
        c22 = Node(None, 'd', False)
        b21 = Node(None, 'e', False)
        b22 = Node(None, 'f', False)
        gp2[0] = p2
        p2[0], p2[1] = c21, c22
        c21[0], c21[1] = b21, b22
        # Checks
        self.assertEqual(gp1, gp2)
        c21._letter = 'z'
        self.assertNotEqual(gp1, gp2)

if __name__ == "__main__":
    unittest.main()