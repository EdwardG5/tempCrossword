from wordClass import Word
from trie import nodesInTrie, listToTrie
from helpers import fileToWordList
import sys
from constants import Constants
from readyWordClassList import setRanks, readyWordList

#---------------------------------------------------------------------------#

# Set whether you want just 1 solution (1 = 1 solution, 0 = all solutions (could be thousands))
oneSolution = 1
# Set which dictionary you want to use
dictName = "wordLists/dict1k.txt"

#---------------------------------------------------------------------------#

# wordList is the list of words remaining to be matched 
# root is the root of the trie (varying lengths) - storing words to be matched against
# wordClass list * trie -> str list list
def solveHelper(wordList, root):
	
	# Base case: Success. No more words to match
	if not wordList:
		# print("Complete solution found")
		return [[]]
	
	# Recursive case
	else:
		word = wordList.pop() # currentWord. Next word to be filled in
		solutions = match(word, 0, root, wordList, root)

		# Return wordlist to original state
		wordList.append(word)
		
		return solutions

# word : wordClass is the word to be matched against
# cL : int is the index, int, of the next letter to be matched
# node : trie is the current position in the trie
# wordList is the remaining set of words to match 
# root : trie is the base node of the trie (to pass onwards)
# Solution lists contain what the current word is 
def match(word, cL, node, wordList, root):
	# Base case: trie matched against word: terminate
	if cL == word.length():
		# Node is word
		if node.word:
			# Modify node values appropriately
			solution = node.whichWord()
			word.setChars([Constants.defaultEmptyChar]+list(solution))
			# Propagate changes to other connected nodes
			word.propagate()
			# Find solutions to remainder of wordList
			solutions = solveHelper(wordList, root)
			# Total solution found
			if solutions:
				for x in solutions:
					x.append(solution)
			# Undo changes to downstream words
			word.undoPropagate()
			word.clear()
			return solutions
			# Collision occurs down the line
			#else:
			#	return []
		
		# Node is not word
		else:
			return []
	
	# Recursive case
	else:
		# Next character set
		if word.set(cL+1): 
			# Find next starting node
			nextNode = node[word._chars[cL+1]]
			# No solution
			if (nextNode == None) or (nextNode.maxLength() < word.length()): 
				return []
			# Continue with search
			else:
				solutions = match(word, cL+1, nextNode, wordList, root)
				return solutions
		
		# Next character blank
		else:
			# Iterate through all 26 possibilities (casing on whether or not they are long enough to be an option)
			solutions = []
			for nextNode in node:
				# No solution
				if (nextNode == None) or (nextNode.maxLength() < word.length()): 
					continue
				# Continue with search
				else:
					#solutions += match(word, cL+1, nextNode, wordList, root)
					newSolution = match(word, cL+1, nextNode, wordList, root)
					if newSolution: 
						solutions += newSolution
						if oneSolution: 
							break
			return solutions

#---------------------------------------------------------------------------#

# Logic: 
# 1) Sort wordlist (word list) into the optimal processing order
# 2) Set ranks and initialize modify and notModify characteristics
# 3) Convert list to stack
# 4) Pass wordstack and trie to solve 

# Success: LifoQueue * trie -> string list list
# solve(wordList, root) => list containing a list of all solution lists e.g. [["hi", "die"], ["hi", "bye"]]. Failure returns an empty list
# Note: solution list is backwards relative to given list
# wordClass list -> str list list
def solve(wordList):
	global dictName
	root = listToTrie(fileToWordList(dictName))
	readyWordList(wordList)
	wordList.reverse() # convert to stack
	solutions = solveHelper(wordList, root)
	return solutions

#---------------------------------------------------------------------------#

def gridTest():
	dictionary = ["ba", "abad", "aba", "adb"]
	# dictionary = fileToWordList("SwedDict.txt") # Modify which dictionary you want to use
	# Make sure entries are properly formatted
	for x in range(len(dictionary)):
		dictionary[x] = dictionary[x].lower()
	dictionary = list(set(dictionary))
	# Create trie structure
	root = listToTrie(dictionary)
	# Create square 3x3 grid (clockwise)
	word1 = Word(3, 2, 0, 1)
	word2 = Word(3, 2, 0, 2)
	word3 = Word(3, 2, 0, 3)
	word4 = Word(3, 2, 0, 4)
	word1._pointers[1], word1._indices[1] = (word4, 1)
	word1._pointers[3], word1._indices[3] = (word2, 1)
	word2._pointers[1], word2._indices[1] = (word1, 3)
	word2._pointers[3], word2._indices[3] = (word3, 3)
	word3._pointers[3], word3._indices[3] = (word2, 3)
	word3._pointers[1], word3._indices[1] = (word4, 3)
	word4._pointers[1], word4._indices[1] = (word1, 1)
	word4._pointers[3], word4._indices[3] = (word3, 1)
	words = [word1, word2, word3, word4]
	# Solve grid crossword
	# solutions = solve(words)
	assert(nodesInTrie(root) == 9)

def hcTest():
	word1 = Word(2, 2, 0, 1)
	word2 = Word(2, 2, 0, 2)
	word3 = Word(2, 2, 0, 3)
	word4 = Word(2, 2, 0, 4)
	word1._pointers[1], word1._indices[1] = (word4, 1)
	word1._pointers[2], word1._indices[2] = (word2, 1)
	word2._pointers[1], word2._indices[1] = (word1, 2)
	word2._pointers[2], word2._indices[2] = (word3, 2)
	word3._pointers[2], word3._indices[2] = (word2, 2)
	word3._pointers[1], word3._indices[1] = (word4, 2)
	word4._pointers[1], word4._indices[1] = (word1, 1)
	word4._pointers[2], word4._indices[2] = (word3, 1)
	wordList = [word1, word2, word3, word4]
	solutions = solve(wordList)
	assert(solutions[0] == ['am', 'me', 'me', 'am'])

def tTest():
	word41 = Word(4, 1, 0, 1)
	word42 = Word(3, 2, 0, 2)
	word43 = Word(5, 1, 0, 3)
	word41._pointers[1], word41._indices[1] = (word42, 1)
	word42._pointers[1], word42._indices[1] = (word41, 1)
	word42._pointers[3], word42._indices[3] = (word43, 2)
	word43._pointers[2], word43._indices[2] = (word42, 3)
	wordList3 = [word41, word42, word43]
	solutions13 = solve(wordList3)
	assert(solutions13[0] == ['other', 'act', 'able'])

#---------------------------------------------------------------------------#

if __name__ == "__main__":
	gridTest()
	hcTest()
	tTest()
	print("Success: All tests passed")

