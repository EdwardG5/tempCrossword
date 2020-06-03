#---------------------------------------------------------------------------#

# Let's the file see the files in the parent folder
import sys
sys.path.append('..')

#---------------------------------------------------------------------------#

from nodeClass import *
from wordClass import *
from index import index
from readyWordClassList import readyWordList, listToLifoQueue

#---------------------------------------------------------------------------#

# Set whether you want just 1 solution (1 = 1 solution, 0 = all solutions (could be thousands))
oneSolution = 1

#---------------------------------------------------------------------------#

# wordList is the list of words remaining to be matched 
# root is the root of the trieWrapper - storing words to be matched against (list with index i trie containing words of length i)
# returns a list of solutions to the wordList 
# if none exists, 
def solveHelper(wordList, trieList, patternDict):
	
	# Base case: Success. No more words to match
	if wordList.empty():
		# print("Complete solution found")
		return [[]]
	
	# Recursive case
	else:
		##################
		# Check whether solution is possible (check existence in patternDict)
		wordListL = []
		while not wordList.empty():
			wordListL.append(wordList.get(block=False))
		for word in wordListL:
			if word.string() not in patternDict:
				# Restore list
				while wordListL:
					wordList.put(wordListL.pop())
				# Exit
				return []
		# Restore list
		while wordListL:
			wordList.put(wordListL.pop())
		##################
		# Solution possible
		word = wordList.get(block=False) # currentWord. Next word to be filled in
		solutions = match(word, 0, trieList[word.length()], wordList, trieList, patternDict) # Pass try of appropriate length
		# Return wordlist to original state
		wordList.put(word)
		return solutions

# word is the word to be matched against: class word
# cL is the index, int, of the next letter to be matched
# node is the current position in the trie
# wordList is the remaining set of words to match 
# root is the root of the trie (to pass onwards)
# Solution lists contain what the current word is 
def match(word, cL, node, wordList, root, patternDict):
	# Base case: trie matched against word: terminate
	if cL == word.length():

			# Modify node values appropriately
			solution = node.whichWord()
			word.setChars([Constants.defaultEmptyChar]+list(solution))
			# Propagate changes to other connected nodes
			word.propagate()
			# Find solutions to remainder of wordList
			solutions = solveHelper(wordList, root, patternDict)
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
				solutions = match(word, cL+1, nextNode, wordList, root, patternDict)
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
					newSolution = match(word, cL+1, nextNode, wordList, root, patternDict)
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
# iW = infoWrapper
def solve3(wordList, iW):
	readyWordList(wordList) # set ranks and such in situ
	wordList = listToLifoQueue(wordList) # convert to stack
	solutions = solveHelper(wordList, iW._tries, iW._patternDict) 
	return solutions

#---------------------------------------------------------------------------#
