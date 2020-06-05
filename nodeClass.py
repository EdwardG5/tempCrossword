class Node:

	def __init__(self, parent, letter, word):
		self._parent = parent			# Pointer to parent
		self._letter = letter			# Current letter
		self.word = word 				# Bool (Yes or no)
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
		return f"({self._letter},{self.word})"

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
			attrs = ["_letter", "_depth", "word", "_height", "_maxLength"]
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
