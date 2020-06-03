

class Node: 

	def __init__(self, parent, letter, depth, word):
		self._parent = parent	# Pointer to parent
		self._letter = letter	# Current letter
		self._depth = depth		# Current depth (first letter is depth = 1)
		self._word = word 		# Bool (Yes or no)
		self._pointers = [None for x in range(26)]	# Pointers to other child nodes
		self._height = 0 		# Longest path existing underneath this nodes
		self._maxLength = depth	# Longest word on whose path node is on (includes the current node)

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

	# Return nth letter in the word (usual indexing)
	# Requires: n < current depth
	def nthLetter(self):
		# Implement
		pass

	# Return the node's height
	def depth(self):
		return self._depth

	# Return the node's height
	def height(self):
		return self._height

	# Return max word length on node's path
	def maxLength(self):
		return self._maxLength

if __name__ == "__main__":
	# Test indexing
	n = Node(None, 'a', 1, False)
	n['a'] = n
	n[1] = n
	assert(n[0] == n['a'])
	assert(n[1] == n['b'])
	print("Success: all tests passed")

	# FIXME: 
	# Need to add far more comprehensive tests.





