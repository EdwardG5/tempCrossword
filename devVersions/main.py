#---------------------------------------------------------------------------#

# Let's the file see the files in the parent folder
import sys
sys.path.append('..')

#---------------------------------------------------------------------------#

from infoWrapperClass import createInfoWrapper
from dictToTrie import listToTrie
from wordClass import Word
from crosswordSolverV1 import solve1
from crosswordSolverV2 import solve2

#---------------------------------------------------------------------------#

# Set which dictionary you want to use
dictName = "wordLists/dict1k.txt"

#---------------------------------------------------------------------------#

# Need to generate tries
# iW
# Download words from file
# Create word lists

# Simple examples
def correctnessTest():

	# Example 1: 2x2 Grid
	word21 = Word(2, 2, 0, 1)
	word22 = Word(2, 2, 0, 2)
	word23 = Word(2, 2, 0, 3)
	word24 = Word(2, 2, 0, 4)
	word21._pointers[1], word21._indices[1] = (word24, 1)
	word21._pointers[2], word21._indices[2] = (word22, 1)
	word22._pointers[1], word22._indices[1] = (word21, 2)
	word22._pointers[2], word22._indices[2] = (word23, 2)
	word23._pointers[2], word23._indices[2] = (word22, 2)
	word23._pointers[1], word23._indices[1] = (word24, 2)
	word24._pointers[1], word24._indices[1] = (word21, 1)
	word24._pointers[2], word24._indices[2] = (word23, 1)
	wordList1 = [word21, word22, word23, word24]

	# Example 2: 3x3 Grid, Hole in middle
	word31 = Word(3, 2, 0, 1)
	word32 = Word(3, 2, 0, 2)
	word33 = Word(3, 2, 0, 3)
	word34 = Word(3, 2, 0, 4)
	word31._pointers[1], word31._indices[1] = (word34, 1)
	word31._pointers[3], word31._indices[3] = (word32, 1)
	word32._pointers[1], word32._indices[1] = (word31, 3)
	word32._pointers[3], word32._indices[3] = (word33, 3)
	word33._pointers[3], word33._indices[3] = (word32, 3)
	word33._pointers[1], word33._indices[1] = (word34, 3)
	word34._pointers[1], word34._indices[1] = (word31, 1)
	word34._pointers[3], word34._indices[3] = (word33, 1)
	wordList2 = [word31, word32, word33, word34]

	# Example 3: 435
	word41 = Word(4, 1, 0, 1)
	word42 = Word(3, 2, 0, 2)
	word43 = Word(5, 1, 0, 3)
	word41._pointers[1], word41._indices[1] = (word42, 1)
	word42._pointers[1], word42._indices[1] = (word41, 1)
	word42._pointers[3], word42._indices[3] = (word43, 2)
	word43._pointers[2], word43._indices[2] = (word42, 3)
	wordList3 = [word41, word42, word43]

	print("Checkpoint 1")
	# Create necessary parameters
	iW = createInfoWrapper("../wordLists/dict1k.txt")
	bigTrie = listToTrie(iW._wordList)
	
	print("Checkpoint 2")
	# Try the solvers
	solutions11 = solve1(wordList1, bigTrie)
	solutions12 = solve1(wordList2, bigTrie)
	solutions13 = solve1(wordList3, bigTrie)

	print("Checkpoint 3")
	solutions21 = solve2(wordList1, iW)
	solutions22 = solve2(wordList2, iW)
	solutions23 = solve2(wordList3, iW)

	print()
	print("Solutions 11:", solutions11)
	print("Solutions 12:", solutions12)
	print("Solutions 13:", solutions13)
	print("Solutions 21:", solutions21)
	print("Solutions 22:", solutions22)
	print("Solutions 23:", solutions23)


def main():
	pass

#---------------------------------------------------------------------------#

correctnessTest()

main()
