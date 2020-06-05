from wordClass import *
from trie import nodesInTrie, listToTrie
from queue import LifoQueue
from helpers import fileToWordList
import sys
from constants import Constants

#---------------------------------------------------------------------------#

# Set whether you want just 1 solution (1 = 1 solution, 0 = all solutions (could be thousands))
oneSolution = 1
# Set which dictionary you want to use
dictName = "wordLists/dict1k.txt"

#---------------------------------------------------------------------------#

# Explanation for bool interpretation of other types
# http://anh.cs.luc.edu/python/hands-on/3.1/handsonHtml/boolean.html

# Explanation of the queue library
# https://docs.python.org/3/library/queue.html

#---------------------------------------------------------------------------#

def listToLifoQueue(words):
	length = len(words)
	lQ = LifoQueue()
	for x in range(len(words)):
		lQ.put(words[length-1-x])
	return lQ

#---------------------------------------------------------------------------#

# wordList is the list of words remaining to be matched 
# root is the root of the trie - storing words to be matched against
# returns a list of solutions to the wordList 
# if none exists, 
def solveHelper(wordList, root):
	
	# Base case: Success. No more words to match
	if wordList.empty():
		# print("Complete solution found")
		return [[]]
	
	# Recursive case
	else:
		word = wordList.get(block=False) # currentWord. Next word to be filled in
		solutions = match(word, 0, root, wordList, root)

		# Return wordlist to original state
		wordList.put(word)
		
		return solutions

# word is the word to be matched against: class word
# cL is the index, int, of the next letter to be matched
# node is the current position in the trie
# wordList is the remaining set of words to match 
# root is the root of the trie (to pass onwards)
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

# Set ranks of words in list (starting at 0)
def setRanks(wordList):
	for x in range(len(wordList)):
		wordList[x].setRank(x)

# Set ranks and initialize modify and notModify characteristics
# Modifies the words themselves (no copy created)
def readyWordList(wordList):
	setRanks(wordList)
	for x in wordList:
		x.initializeModify()
		x.initializeNotModify()

#---------------------------------------------------------------------------#

# e.g. dictName = "Dict.txt"
# Takes a dictionary name and returns the root of a trie storing dictionary
def readyTrie(dictName):
	dictionary = fileToWordList(dictName)
	for x in range(len(dictionary)):
		dictionary[x] = dictionary[x].lower()
	root = listToTrie(dictionary)
	return root

#---------------------------------------------------------------------------#

# Logic: 
# 1) Sort wordlist (word list) into the optimal processing order
# 2) Set ranks and initialize modify and notModify characteristics
# 3) Convert list to stack
# 4) Pass wordstack and trie to solve 

# Success: LifoQueue * trie -> string list list
# solve(wordList, root) => list containing a list of all solution lists e.g. [["hi", "die"], ["hi", "bye"]]. Failure returns an empty list
# Note: solution list is backwards relative to given list
def solve(wordList):
	root = readyTrie(dictName)
	readyWordList(wordList)
	wordList = listToLifoQueue(wordList)
	solutions = solveHelper(wordList, root)
	return solutions

#---------------------------------------------------------------------------#

def printNSolutions(solutions):
	for x in range(int(input())):
		print(solutions[x])

#---------------------------------------------------------------------------#

def main0():
	# dictionary = fileToWordList("Dict.txt")
	# for x in range(len(dictionary)):
	# 	dictionary[x] = dictionary[x].lower()
	# print(len(dictionary))
	# root = listToTrie(dictionary)
	words = [[0, 0, 0, 3*Constants.defaultEmptyChar], [2, 0, 1, 3*Constants.defaultEmptyChar]]
	wordList = convertWordsToClass(words, {})
	solutions = solve(wordList)
	assert(solutions == [['act', 'act']])

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
	solutions = solve(words)
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
	assert(solutions == [['am', 'me', 'me', 'am']])

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

# If you're running this file as a standalone application: 

def main():
	main0()
	gridTest()
	hcTest()
	tTest()
	print("Success: All tests passed")

if __name__ == "__main__":
	main()

