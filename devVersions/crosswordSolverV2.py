from nodeClass import *
from wordClass import *
from dictToTrie import *
from index import index
from queue import LifoQueue
from fileToList import *
import sys

#---------------------------------------------------------------------------#

# Set whether you want just 1 solution (1 = 1 solution, 0 = all solutions (could be thousands))
oneSolution = 1

#---------------------------------------------------------------------------#

# wordList is the list of words remaining to be matched 
# root is the root of the trieWrapper - storing words to be matched against (list with index i trie containing words of length i)
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
		solutions = match(word, 0, root.trie(word.length()), wordList, root) # Pass try of appropriate length
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

			# Modify node values appropriately
			solution = node.whichWord()
			word.setChars([""]+list(solution))
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
	
	# Recursive case
	else:
		# Next character set
		if word.set(cL+1): 
			# Find next starting node
			nextNode = node.childL(word._chars[cL+1])
			# No solution
			if nextNode == None: 
				return []
			# Continue with search
			else:
				solutions = match(word, cL+1, nextNode, wordList, root)
				return solutions
		
		# Next character blank
		else:
			# Iterate through all 26 possibilities (casing on whether or not they are long enough to be an option)
			solutions = []
			for x in range(26):
				# Find next starting node
				nextNode = node.childN(x)
				# No solution
				if nextNode == None: 
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
def solve(wordList):
	root = readyTrieWrapper(dictName) # dictName is a string filename
	readyWordList(wordList) # set ranks and such insitu
	wordList = listToLifoQueue(wordList) # convert to stack
	solutions = solveHelper(wordList, root) 
	return solutions

#---------------------------------------------------------------------------#