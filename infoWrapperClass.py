from preprocessWordList import *
import itertools
from dictToTrie import listToTrie

#---------------------------------------------------------------------------#

# Note: sorts the passed list
class infoWrapper:
	# word list : string list
	def __init__(self, wordList):
		# sort by length
		wordList.sort(key=len)
		self._wordList = wordList
		self._patternDict = listToPatternDict2(wordList)
		self._avDict = summDictToavDict(freqDictTosummDict(patternDictTofreqDict(self._patternDict)))
		self._tries = [None] + [listToTrie(words) for key, words in itertools.groupby(wordList, len)]

def createInfoWrapper(dictName):
	# load word list
	dictionary = fileToWords(dictName)
	return infoWrapper(dictionary)

#---------------------------------------------------------------------------#