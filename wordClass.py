# For some reason, I decided to make everything to do with the words 1 indexed

class Word:
	
	def __init__(self, length, constrained, setChars, index):
		self._index = index										# Unique word index
		self._length = length								    # Length of the word
		self._constrained = constrained						    # The number of characters linked to other characters
		self._set = setChars									# The number of characters already set
		self._chars = ["" for x in range(length+1)] 			# A position for each character in the word + 1 initial blank to allow easy use with depth
		self._pointers = [None for x in range(length+1)]		# Pointers to other word who ith character is linked to word's ith character (pointer to word, index in word)
		self._indices = [0 for x in range(length+1)]			# Indices corresponding to pointers
		self._rank = 0											# Rank = order in which the words are evaluated, starting at 1. 0 = uninitialised
		self._modify = [0 for x in range(self.length()+1)] 		# For propogate: 0 = don't modify, 1 = modify. pointers which point to items downstream
		self._notModify = [0 for x in range(self.length()+1)] 	# For clear: (don't clear chars set by upstream words) 0 = don't modify, 1 = modify. pointers which point to items downstream

	# Edward's
	def __repr__(self):
		return f"({self._index}, {self._length})"

	# Sean's
	# def __repr__(self):
    #    string = f"""{self.chars[1:]}, Word {self.index}, Length {self.length}, {self.constrained} constraints with {self.set} set characters"""
    #    return string

	def length(self):
		return self._length

	def initializeModify(self):
		for x in range(self.length()+1):
			if self._pointers[x]:
				if compareRanks(self, self._pointers[x]) == -1:
					self._modify[x] = 1

	def initializeNotModify(self):
		for x in range(self.length()+1):
			if self._pointers[x]:
				if compareRanks(self, self._pointers[x]) == 1:
					self._notModify[x] = 1

	# Modify all the connected words - fill in the connected blank
	def propagate(self):
		for x in range(self.length()+1):
			if self._modify[x]:
				self._pointers[x].setChar(self._indices[x], self._chars[x])

	# undoPropagate for items downstream (leave upstream (lower rank) untouched)
	def undoPropagate(self):
		for x in range(self.length()+1):
			if self._modify[x]:
				self._pointers[x].setChar(self._indices[x], "")

	# clear (leaving upstream set characters be)
	def clear(self):
		for x in range(self.length()+1):
			if not self._notModify[x]:
				self.setChar(x, "")

	# Whether or not letter x has been assigned a letter or if it is a blank
	def set(self, x):
		return not self._chars[x] == ""

	def showPointers(self):
		print(self._pointers)

	def setIndex(self, index):
		self._index = index

	def setLength(self, length):
		self._length = length

	def setConstrained(self, constrained):
		self._constrained = constrained

	def setSetChars(self, setChars):
		self._set = setChars

	def setChar(self, index, char):
		self._chars[index] = char

	def setChars(self, chars):
		self._chars = chars

	def setPointer(self, index, pointer):
		self._pointers[index] = pointer
		
	def setPointers(self, pointers):
		self._pointers = pointers

	def getRank(self):
		return self._rank

	def setRank(self, rank):
		self._rank = rank

	def setIndices(self, index, choice):
		self._indices[index] = choice

# -1 = w1 < w2, 0 = w1 = w2, 1 = w1 > w2
def compareRanks(word1, word2):
	r1 = word1.getRank()
	r2 = word2.getRank()
	if r1 < r2:
		return -1
	elif r1 == r2:
		return 0
	else:
		return 1

