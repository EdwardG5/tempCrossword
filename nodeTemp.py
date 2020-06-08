from nodeClass import Node
from copy import copy

def terminal(root):
    return all(not i for i in root)

def solGen(root, prefix=[]):
    prefix.append(root._letter)
    if terminal(root):
        yield prefix
    else:
        for i in root:
            if i:
                yield from solGen(i, copy(prefix))

# # Create tree (1 - 2 - 4)
# p1 = Node(None, "hello", False)
# c1 = Node(p1, "apple", False)
# c2 = Node(p1, "abs", False)
# b1 = Node(c1, "pear", False)
# b2 = Node(c1, "pan", False)
# b3 = Node(c2, "dum", False)
# b4 = Node(c2, "dummer", False)
# p1[0] = c1
# p1[1] = c2
# c1[0] = b1
# c1[1] = b2
# c2[0] = b3
# c2[1] = b4

# solutions = solGen(p1)
# for i in solutions:
#     print(i)

# ['hello', 'apple', 'pear']
# ['hello', 'apple', 'pan']
# ['hello', 'abs', 'dum']
# ['hello', 'abs', 'dummer']