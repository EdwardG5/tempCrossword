from timeit import timeit
from fileToList import fileToWords


class Node:

	def __init__(self, parent, letter, depth, word):
		self._parent = parent  # Pointer to parent
		self._letter = letter  # Current letter
		self._depth = depth		# Current depth (first letter is depth = 1)
		self._word = word 		# Bool (Yes or no)
		# Pointers to other child nodes
		self._pointers = [None for x in range(26)]
		self._height = 0 		# Longest path existing underneath this nodes
		# Longest word on whose path node is on (includes the current node)
		self._maxLength = depth

	def __repr__(self):
		return f"({self._letter},{self._word})"

	def __iter__(self):
		return iter(self._pointers)

	# Raises exception/Returns None on failure
	def __getitem__(self, i):
		if isinstance(i, int):
			return self._pointers[i]
		elif isinstance(i, str):
			return self._pointers[self._charToInt(i)]
		else:
			raise TypeError("Node indices must be int or char")

	def __setitem__(self, i, value):
		if isinstance(i, int):
			self._pointers[i] = value
		elif isinstance(i, str):
			self._pointers[self._charToInt(i)] = value
		else:
			raise TypeError("Node indices must be int or char")

	# Calculates an index from a corresponding char (e.g. 'a' = 0)
	@staticmethod
	def _charToInt(letter):
		return ord(letter.lower())-97

	# Return whether current node is a word: True/False
	def word(self):
		return self._word

	# Return word represented by node.
	def whichWord(self):
		node = self
		str = node._letter
		while node._parent:
			node = node._parent
			str += node._letter
		return str[::-1]

	# Note: Never used.
	# Return nth letter in the word (usual indexing)
	# Requires: n < current depth
	def nthLetter(self):
		# Implement
		pass

	# Note: Never used except for when created (also, you don't
	# Note: need to explicitly pass it: automatically fetch parent depth
	# Note: and increment).

	# Return the node's height
	def depth(self):
		return self._depth

	# Note: never called. Attribute is accessed directly (in dictToTrie)
	# Note: but no usage of the actual function.
	# Return the node's height
	def height(self):
		return self._height

	# Return max word length on node's path
	def maxLength(self):
		return self._maxLength

	def __eq__(self, other):
		# if other check asserts that other != None
		if other:
			attrs = ["_letter", "_depth", "_word", "_height", "_maxLength"]
			if all(getattr(self, attr) == getattr(other, attr) for attr in attrs):
				return all(self[i] == other[i] for i in range(26))
		return False


class Node2:

	def __init__(self, parent, letter, word):
		self._parent = parent			# Pointer to parent
		self._letter = letter			# Current letter
		self._word = word 				# Bool (Yes or no)
		# Pointers to other child nodes
		self._pointers = [None for x in range(26)]
		if parent:						# Current depth (first letter is depth = 1)
			self._depth = parent._depth+1
		else:
			self._depth = 0  # Root node
		self._height = 0 				# Longest path existing underneath this nodes
		# Longest string on whose path node is on (includes the current node)
		self._maxLength = self._depth
		self._update_parent()				# Update height and maxLength of parent

	def __repr__(self):
		return f"({self._letter},{self._word})"

	def __iter__(self):
		return iter(self._pointers)

	# Raises exception/Returns None on failure
	def __getitem__(self, i):
		if isinstance(i, int):
			return self._pointers[i]
		elif isinstance(i, str):
			return self._pointers[self._charToInt(i)]
		else:
			raise TypeError("Node indices must be int or char")

	def __setitem__(self, i, value):
		if isinstance(i, int):
			self._pointers[i] = value
		elif isinstance(i, str):
			self._pointers[self._charToInt(i)] = value
		else:
			raise TypeError("Node indices must be int or char")

	def __eq__(self, other):
		# if other check asserts that other != None
		if other:
			attrs = ["_letter", "_depth", "_word", "_height", "_maxLength"]
			if all(getattr(self, attr) == getattr(other, attr) for attr in attrs):
				return all(self[i] == other[i] for i in range(26))
		return False

	def _update_parent(self):
		parent = self._parent
		if parent:
			if self._height+1 > parent._height:
				parent._height = self._height+1
				parent._update_max_length()
				parent._update_parent()

	def _update_max_length(self):
		self._maxLength = self._depth+self._height

	# Calculates an index from a corresponding char (e.g. 'a' = 0)
	@staticmethod
	def _charToInt(letter):
		return ord(letter.lower())-97

	# Return whether current node is a word: True/False
	def word(self):
		return self._word

	# Return word represented by node.
	def whichWord(self):
		node = self
		str = node._letter
		while node._parent:
			node = node._parent
			str += node._letter
		return str[::-1]

	# Return max word length on node's path
	def maxLength(self):
		return self._maxLength


#------------------------------------------------------------------------------#

# Verify that node indexing and equality comparison has been implemented correctly

def test_indexing_v1():
	# Test indexing
	n = Node(None, 'a', 1, False)
	n['a'] = n
	n[1] = n
	assert(n[0] is n['a'])
	assert(n[1] is n['b'])
	return True


def test_indexing_v2():
	# Test indexing
	n = Node2(None, 'a', False)
	n['a'] = n
	n[1] = n
	assert(n[0] is n['a'])
	assert(n[1] is n['b'])
	return True


def test_eq_v1():
	# Grandparent, parent, child, baby (level 0, 1, 2, 3)
	# Tree 1
	gp1 = Node(None, 'a', 1, False)
	p1 = Node(None, 'b', 2, False)
	c11 = Node(None, 'c', 3, False)
	c12 = Node(None, 'd', 3, False)
	b11 = Node(None, 'e', 4, False)
	b12 = Node(None, 'f', 4, False)
	gp1[0] = p1
	p1[0], p1[1] = c11, c12
	c11[0], c11[1] = b11, b12
	# Tree 2
	gp2 = Node(None, 'a', 1, False)
	p2 = Node(None, 'b', 2, False)
	c21 = Node(None, 'c', 3, False)
	c22 = Node(None, 'd', 3, False)
	b21 = Node(None, 'e', 4, False)
	b22 = Node(None, 'f', 4, False)
	gp2[0] = p2
	p2[0], p2[1] = c21, c22
	c21[0], c21[1] = b21, b22
	# Checks
	assert(gp1 == gp2)
	c21._letter = 'z'
	assert(gp1 != gp2)
	return True


def test_eq_v2():
	# Grandparent, parent, child, baby (level 0, 1, 2, 3)
	# Tree 1
	gp1 = Node2(None, 'a', False)
	p1 = Node2(None, 'b', False)
	c11 = Node2(None, 'c', False)
	c12 = Node2(None, 'd', False)
	b11 = Node2(None, 'e', False)
	b12 = Node2(None, 'f', False)
	gp1[0] = p1
	p1[0], p1[1] = c11, c12
	c11[0], c11[1] = b11, b12
	# Tree 2
	gp2 = Node2(None, 'a', False)
	p2 = Node2(None, 'b', False)
	c21 = Node2(None, 'c', False)
	c22 = Node2(None, 'd', False)
	b21 = Node2(None, 'e', False)
	b22 = Node2(None, 'f', False)
	gp2[0] = p2
	p2[0], p2[1] = c21, c22
	c21[0], c21[1] = b21, b22
	# Checks
	assert(gp1 == gp2)
	c21._letter = 'z'
	assert(gp1 != gp2)
	return True


test_indexing_v1()
test_indexing_v2()
test_eq_v1()
test_eq_v2()

#------------------------------------------------------------------------------#

# For Node1

# Creates a new trie with every word in a given word list. Returns root of a trie.
# str list -> node structure (trie)

def listToTrieV1(wordList):
	root = Node(None, "", 0, False)
	for word in wordList:
		newNode = root
		depth = 0
		for char in word:
			depth += 1
			if newNode[char] == None:
				newNode[char] = Node(newNode, char, depth, False)
				newNode = newNode[char]
				testNode = newNode._parent
				while not (testNode is root):
				    for node in testNode:
				        if node != None:
				            if node._height+1 > testNode._height:
				                testNode._height = node._height+1
				                testNode._maxLength += 1
				    testNode = testNode._parent
			else:
				newNode = newNode[char]
		newNode._word = True
	return root

def listToTrieV2(wordList):
	root = Node(None, "", 0, False)
	for word in wordList:
		newNode = root
		depth = 0
		for char in word:
			depth += 1
			if newNode[char] == None:
				newNode[char] = Node(newNode, char, depth, False)
				newNode = newNode[char]
				current = newNode
				parent = current._parent
				while True: 
					if parent and current._height+1 > parent._height:
						parent._height = current._height+1
						parent._maxLength += 1
						current, parent = parent, parent._parent
					else:
						break

			else:
				newNode = newNode[char]
		newNode._word = True
	return root

#------------------------------------------------------------------------------#

# For Node2


def insertWordInTrie(root, word):
	char = word[0]
	if root[char] == None:
		root[char] = Node2(root, char, False)
	if len(word) == 1:
		root[char]._word = True
	else:
		insertWordInTrie(root[char], word[1:])

# Creates a new trie with every word in a given word list. Returns root of a trie.
# str list -> node structure (trie)


def listToTrie2(wordList):
	root = Node2(None, "", False)
	for word in wordList:
		insertWordInTrie(root, word)
	return root

#------------------------------------------------------------------------------#

"""
Overview: 

listToTrieV1: (slightly modified) original implementation
listToTrieV2: corrected implementation for original node structure
listToTrie2: implementation for new node structure

The difference between the old and new node structures is that the new node strucure 
1) removes useless methods which were never called anywhere
2) adds node addition logic to the class itself. Now a node containing a data element
	can be added to a trie without the user worrying about maintaining any of the height/
	depth/maxLength invariants. 

It also significantly simplifies implementation of the function listToTrie. The version for 
Node2 is recursive compared to the initial iterative one.
"""

words = fileToWords("wordLists/dict1k.txt")

root1 = listToTrieV1(words)
root2 = listToTrieV2(words)
root3 = listToTrie2(words)

# Correctness:

# Sean's original implementation of listToTrie incorrectly handled the edge case of the root node. 
# Did not properly modify its height and maxLength - and thus the below assertions fail. 
# assert(root1 == root2) 
# assert(root1 == root3)
assert(root2 == root3)
assert(root3 == root2)

# Performance: 

# Trie generation timing test:
# Node1 V1: 26.13407004
# Node1 V2: 11.04932314
# Node2: 	12.80068233
print(timeit("listToTrieV1(words)", number=500, globals=globals()))
print(timeit("listToTrieV2(words)", number=500, globals=globals()))
print(timeit("listToTrie2(words)", number=500, globals=globals()))



# # def compareNodeStructures

# def main():
# 	time1 = time.time()
# 	words = fileToWords("wordLists/dict10k.txt")
# 	time2 = time.time()


# if __name__ == "__main__":
# 	# FIXME:
# 	# Need to add far more comprehensive tests.
# 	test_indexing(Node)
# 	test_eq(Node)
# 	print("Success: all tests passed")
