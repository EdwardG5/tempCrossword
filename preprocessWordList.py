from wordClass import Word
import itertools
from fileToList import fileToWords
import os
import time
from crosswordSolver import readyWordList
from constants import Constants

#---------------------------------------------------------------------------#

# word: string, pattern: string 
# e.g. pattern = "a--bc-"
# string * string -> bool
# REQUIRES: len(word)=len(pattern)=len
def match(word, pattern, len):
	for x in range(len):
		if word[x] != pattern[x]:
			return False
	return True

def extractAllPatterns(word, length):
	# Explode into chars
	l = list(word)
	# Create options list
	for x in range(length):
		l[x] = [l[x], '-']
	# Create patterns
	patterns = list(itertools.product(*l))
	# Simplify to strings
	length = len(patterns)
	for x in range(length):
		patterns[x] = "".join(patterns[x])
	# Return
	return patterns

def listToPatternList(wordList):
	patterns = []
	for word in wordList:
		patterns += extractAllPatterns(word, len(word))
	return patterns

# Get patterns in mass
# Add to dict in mass
def listToPatternDict1(wordList):
	mDict = dict()
	# time1 = time.time()
	patterns = listToPatternList(wordList)
	# time2 = time.time()
	# pSize = 0
	# dSize = 0
	for p in patterns:
		# pSize += 1
		if p in mDict:
				mDict[p] += 1
		else:
				mDict[p] = 1
				# dSize += 1
	# print(pSize)
	# print(dSize)
	# time3 = time.time()
	# print("P1: ", time2-time1)
	# print("P2: ", time3-time2)
	return mDict


# Get patterns from each word
# Add to dict
# Scrap old pattern
def listToPatternDict2(wordList):
	mDict = dict()
	for word in wordList:
		patterns = extractAllPatterns(word, len(word))
		for p in patterns:
			if p in mDict:
					mDict[p] += 1
			else:
					mDict[p] = 1
	return mDict

#---------------------------------------------------------------------------#

# Analyses functions

def longestWord(wordList):
	return max(wordList, key=len)

def numSet(pattern):
	count = 0
	for x in pattern:
			if x!= Constants.defaultEmptyChar:
					count += 1
	return count

# patternDict["a--b-"] = 5 => "a--b-" has 5 solutions
# freqDict[(len, #set, #options)] = 5 => patterns of length
# len with #set chars which have #options occurs 5 times
def patternDictTofreqDict(patternDict):
	freqDict = {}
	# Collate results 
	for x in patternDict:
		if (len(x), numSet(x), patternDict[x]) not in freqDict:
				freqDict[(len(x), numSet(x), patternDict[x])] = 1
		else:
				freqDict[(len(x), numSet(x), patternDict[x])] += 1
	return freqDict

# summDict[(len, set)] = (total number of options, total frequency)
def freqDictTosummDict(freqDict):
	summDict = {}
	for x in freqDict:
		((len, numSet, num), freq) = (x, freqDict[x])
		if (len, numSet) in summDict:
				(tN, tF) = summDict[(len, numSet)] 
				summDict[(len, numSet)] = (tN+num*freq, tF+freq)
		else:
				summDict[(len, numSet)] = (num*freq, freq)
	return summDict

# summDict[(len, set)] = average number of options to match pattern
def summDictToavDict(summDict):
	avDict = {}
	for x in summDict:
		(tN, tF) = summDict[x]
		avDict[x] = int(tN/tF)
	return avDict

#---------------------------------------------------------------------------#

# Determine rating of wordList: roughly the worst case bound of word combinations
# analysed, biased to favour having smaller numbers appear earlier in the multiplication
# Smaller rating is better
# word class list -> int 
def ranking(wordList):
		# Prepare list for analysis (set ranks and modify characteristics)
		readyWordList(wordList)
		# Determine rating
		rating = 1
		for word in wordList:
			rating *= avDict[(word.length(), word.numSet())]
			rating = int(rating**1.2) # Bias to favor smaller numbers earlier 
			word.propagateSet()
		# Clear set attribute
		for word in wordList:
			word.clearSet()
		return rating

# Given a list of word structures, determines the optimal order in which to 
# process them. (smallest state space, most quickly eliminate options etc)
# REQUIRES: all words in input list are initially clear
def determineOrder(wordList, avDict):
	wordListPermutations = list(itertools.permutations(wordList))
	minRating = ranking(wordListPermutations[0])
	optimalPerm = wordListPermutations[0]
	for words in wordListPermutations:
		rating = ranking(words)
		if rating < minRating:
			minRating = rating
			optimalPerm = words
	return optimalPerm

#---------------------------------------------------------------------------#

# Lets test run how long this would take on an actual dictionary
def main():
	time1 = time.time()
	words = fileToWords("wordLists/dict10k.txt")
	time2 = time.time()
	print("First part done")
	dict1 = listToPatternDict1(words)
	time3 = time.time()
	print("Second part done")
	# dict2 = listToPatternDict2(words)
	time4 = time.time()
	print("Third part done")
	os.system('say "your program has finished"')
	print("file -> wordlist: ", time2-time1)
	print("dict1 generation: ", time3-time2)
	print("dict2 generation: ", time4-time3)
	"""
	Checking that everything works:
	word1 = Word(4, 1, 0, 1)
	word2 = Word(3, 2, 0, 2)
	word3 = Word(5, 1, 0, 3)
	word1._pointers[1], word1._indices = (word2, 1)
	word2._pointers[1], word2._indices = (word1, 1)
	word2._pointers[3], word2._indices = (word3, 2)
	word3._pointers[2], word3._indices = (word2, 3)
	words = [word1, word2, word3]
	wordList = fileToWords("wordLists/dict1k.txt")
	patternDict = listToPatternDict1(wordList)
	freqDict = patternDictTofreqDict(patternDict)
	summDict = freqDictTosummDict(freqDict)
	avDict = summDictToavDict(summDict)
	determineOrder(words, avDict)
	"""
	














