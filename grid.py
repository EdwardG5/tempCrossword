"""
This file contains functions which act on crossword grids, in list format, directly.

E.g: 
[
[ "#", "#", "#", a], 
[ "#", "c", "a", b], 
[ "z", "a", " ", a], 
[ "z", "t", "#", a]
]
"""

from constants import Constants
from copy import copy
from wordClass import Word
from collections import namedtuple

"""
Option with more whitespace: 

def printGrid(grid):
	width = (len(grid[0])*2-1) # *2 for 'l ', -1 for end
	startStop = "--"+("-"*width)+"--" 
	emptyLine = "| "+(" "*width)+" |"
	print(startStop)
	print(emptyLine)
	for line in grid:
		print("| "+" ".join(line)+" |")
		print(emptyLine)
	print(startStop)
"""

def printGrid(grid):
	grid = list(map((lambda line: list(map(str, line))), grid))
	width = (len(grid[0])) # *2 for 'l ', -1 for end
	startStop = "-"+("-"*width)+"-" 
	print(startStop)
	for line in grid:
		print("|"+"".join(line)+"|")
	print(startStop)

# Removes all filled in letters leaving only blocked squares
# Replace specifies what to fill all non-blocked squares with (standard usage is Constants.defaultEmptyChar or [] (to store identifiers))
# Note: pure. It creates a new grid, rather than modifying the original.
# Note: every time it creates a copy of "replace", so passing in a mutable structure
# is no problem.
def removeLetters(grid, replace=Constants.defaultEmptyChar):
	convert = lambda l: l if l == Constants.defaultBlockedChar else copy(replace) # If you pass in a mutable type e.g. [] you need to ensure you don't pass the same object reference to each
	return list(map((lambda line: list(map(convert, line))), grid))

# -----------------------------------------------------------------
# Helper functions for identifier placers
# -----------------------------------------------------------------

# Square not blocked
def notBlocked(square):
	return square != Constants.defaultBlockedChar
# Square not part of across
def nPOA(grid, row, col):
	return len(grid[row][col]) == 0 or (len(grid[row][col]) == 1 and grid[row][col][0][1] != "Across")
# Square not part of down
def nPOD(grid, row, col):
	return len(grid[row][col]) == 0 or (len(grid[row][col]) == 1 and grid[row][col][0][1] != "Down")
# Next square across is clear
def nA(grid, row, col):
	try:
		return notBlocked(grid[row][col+1])
	except:
		return False
# Next square down is clear
def nD(grid, row, col):
	try:
		return notBlocked(grid[row+1][col])
	except:
		return False
# Left square is blocked 
def lB(grid, row, col):
	return not notBlocked(grid[row][col-1])
# Up square is blocked
def uB(grid, row, col):
	return not notBlocked(grid[row-1][col])

# -----------------------------------------------------------------

# Rules: 
# a square is the start of a word if not blocked AND: 
# 		   	At the top or leftmost edge of grid
# 		OR 	Up/Left square is blocked
# AND across/down is not blocked (len >= 2)

# - This function identifies squares in the grid which according to the above rules begin
# words in the crossword. It passes an ith : int identifying which ith word it is (left to right).
# This starts at 1 by default - you can modify.
# - fA * fD * replace -> grid -> newGrid
# - (grid * row * col * ith -> _) * (grid * row * col * ith -> _) * any -> char list list -> newGrid (blocked spaces
# are left unmodified, while other squares are filled with "any".)
# - The function begins by calling removeLetters, replacing non-blocked squares with the argument replace.
# Note: every time it creates a copy of "replace", so passing in a mutable structure is no problem.
# - The function identifies starting squares and then passed these squares together with the grid to fA
# and fD (in that order). Note that if a square starts both an across and down word, both fA and fD will
# be applied. Note that the same ith will be passed to both.

# startingSquaresOne one is similar except that it identifies squares which start across OR down, and applies
# the function passed only once. Note: in this case you have no contextual indication or whether Across/Down/both
# causes invocation of the function.

# Note: The below functions require that grid is at least 2 across and down. 

def startingSquares(fA, fD, replace, ith=1):
	def wrapper(grid, ith=ith):
		newGrid = removeLetters(grid, replace=replace)
		height, width = len(newGrid), len(newGrid[0])
		for row in range(height):
			for col in range(width):
				if notBlocked(newGrid[row][col]):
					startOfAcross = False
					startOfDown = False
					# Across
					if (col == 0 or lB(newGrid, row, col)) and nA(newGrid, row, col):
						startOfAcross = True
						fA(newGrid, row, col, ith)
					# Down
					if (row == 0 or uB(newGrid, row, col)) and nD(newGrid, row, col):
						startOfDown = True
						fD(newGrid, row, col, ith)
					if startOfAcross or startOfDown:
						ith += 1
		return newGrid
	return wrapper

def startingSquaresOne(f, replace, ith=1):
	def wrapper(grid, ith=ith):
		newGrid = removeLetters(grid, replace=replace)
		height, width = len(newGrid), len(newGrid[0])
		for row in range(height):
			for col in range(width):
				if notBlocked(newGrid[row][col]):
					startOfAcross = False
					startOfDown = False
					# Across
					if (col == 0 or lB(newGrid, row, col)) and nA(newGrid, row, col):
						startOfAcross = True
					# Down
					if (row == 0 or uB(newGrid, row, col)) and nD(newGrid, row, col):
						startOfDown = True
					if startOfAcross or startOfDown:
						f(newGrid, row, col, ith)
						ith += 1
		return newGrid
	return wrapper

# This function accepts fA, fD, and struct. 
# (struct * row * col * ith -> _) * (struct * row * col * ith -> _) * struct -> char list list -> struct
# Each function call is invoked on a copy of the struct passed. This allows you to store information in a
# 'global' structure e.g. a list, a dict, which is returned from the resulting function. 
def startingSquaresGlobal(fA, fD, struct, ith=1):
	struct = copy(struct) 	# Save a local copy of the passed struct (the user shouldn't modify the passed 
							# struct, but it they do things are messed up)
	def wrapper(grid, struct=struct, ith=ith):
		struct = copy(struct)
		newGrid = removeLetters(grid, replace=Constants.defaultEmptyChar)
		height, width = len(newGrid), len(newGrid[0])
		for row in range(height):
			for col in range(width):
				if notBlocked(newGrid[row][col]):
					startOfAcross = False
					startOfDown = False
					# Across
					if (col == 0 or lB(newGrid, row, col)) and nA(newGrid, row, col):
						startOfAcross = True
						fA(struct, row, col, ith)
					# Down
					if (row == 0 or uB(newGrid, row, col)) and nD(newGrid, row, col):
						startOfDown = True
						fD(struct, row, col, ith)
					if startOfAcross or startOfDown:
						ith += 1
		return struct
	return wrapper

# -----------------------------------------------------------------

# Unique word identifier (ith, direction)
WordId = namedtuple('WordId', ['ith', 'dir'])

# Data type to store information about a word in the context of a particular square
# Wid = WordId tuple, ith, dir, e.g. (1, "Across")
# Len = Length of the word
# Constrained = Number of letters of that word which are linked to other words
# Pos = ith letter, starting at 1
SquareWordInfo = namedtuple('SquareWordInfo', ['wid', 'len', 'pos'])

# -----------------------------------------------------------------

def gLen(grid, dire, row, col):
	count = 0
	try:
		while grid[row][col] != Constants.defaultBlockedChar:
			count += 1
			if dire == "Down":
				row += 1
			elif dire == "Across":
				col += 1
	except:
		pass
	return count

def fA(grid, row, col, ith):
	try:
		length = gLen(grid, "Across", row, col)
		pos = 1
		while notBlocked(grid[row][col]):
			wid = WordId(ith, "Across")
			info = SquareWordInfo(wid, length, pos)
			grid[row][col].append(info)
			col += 1
			pos += 1
	except:
		pass

def fD(grid, row, col, ith):
	try:
		length = gLen(grid, "Down", row, col)
		pos = 1
		while notBlocked(grid[row][col]):
			wid = WordId(ith, "Down")
			info = SquareWordInfo(wid, length, pos)
			grid[row][col].append(info)
			row += 1
			pos += 1
	except:
		pass

# Produces a grid with [] elements. The lists contain either one or two info grid tuples, 
# depending on whether that square is the intersection of two words or part of one. 
populateWithInfo = startingSquares(fA, fD, replace=[])

# -----------------------------------------------------------------

def f(grid, row, col, ith):
	try:
		grid[row][col] = ith
	except:
		pass

# Produces a grid with ith numbers in the squares starting crossword words. Used for drawing
# small numbers. 
# char list list -> char list list
populateWithIth = startingSquaresOne(f, replace=Constants.defaultEmptyChar)

# -----------------------------------------------------------------

def fA(mDict, row, col, ith):
	wid = WordId(ith, "Across")
	mDict[wid] = (row, col)

def fD(mDict, row, col, ith):
	wid = WordId(ith, "Down")
	mDict[wid] = (row, col)

# Produces a dict e.g. {(1, "Above") : (row, col), (1, "Down") : (row, col), ...}
# char list list -> Dict[wid] : int * int
startPositionsDict = startingSquaresGlobal(fA, fD, {})

# -----------------------------------------------------------------

# Count the length of the word starting at row, col, going in direction dire
# grid : grid produced by wordIdentifiers
def gConstrained(grid, dire, row, col):
	count = 0
	try:	
		while grid[row][col] != Constants.defaultBlockedChar:
			if len(grid[row][col]) == 2:
				count += 1
			if dire == "Down":
				row += 1
			elif dire == "Across":
				col += 1
	except:
		pass
	return count

# Given a list of SquareWordInfo tuples, returns the one whose id matches wid
def gMatchingId(l, wid):
	for info in l:
		if info.wid == wid:
			return info

# Given a list of SquareWordInfo tuples, returns the one whose id does not match wid
def gNotMatchingId(l, wid):
	for info in l:
		if info.wid == wid:
			pass
		else:
			return info

# Convert a grid into a list of fully linked word class objects
# str list list -> wordClass list
# FIXME: Right not it doesn't take into account letters that are already in the grid
def gridToWordClassList(grid):
	infoGrid = populateWithInfo(grid)
	startPosDict = startPositionsDict(grid)
	wcDict = {}
	# Create words
	for row, col in startPosDict.values():
		for wordInfo in infoGrid[row][col]:
			wid, wlen = wordInfo.wid, wordInfo.len
			wconstrained = gConstrained(grid, wid.dir, row, col)
			wcDict[wid] = Word(wlen, wconstrained, 0, wid)
	# Link words
	for wid, wcObject in wcDict.items():
		row, col = startPosDict[wid]
		colIncr = 1 if wid.dir == "Across" else 0
		rowIncr = 1-colIncr
		wordInfo = gMatchingId(infoGrid[row][col], wid)
		for i in range(wordInfo.len):
			# Substitute existing letter
			char = grid[row][col].lower()
			if char.isalpha():
				wcObject._chars[i+1] = char
			# Two words intersecting
			if len(infoGrid[row][col]) == 2:
				otherWordInfo = gNotMatchingId(infoGrid[row][col], wid)
				owid, owpos = otherWordInfo.wid, otherWordInfo.pos
				wcObject._pointers[i+1], wcObject._indices[i+1] = wcDict[owid], owpos
			col += colIncr
			row += rowIncr
	return list(wcDict.values())

# -----------------------------------------------------------------

# Substites a word into a grid, starting at row, col, in direction dir
def fillInWord(grid, word, direction, row, col):
	colIncr = 1 if direction == "Across" else 0
	rowIncr = 1-colIncr
	for letter in word:
		grid[row][col] = letter
		col += colIncr
		row += rowIncr

# Accepts a grid (in any state of completion), a solution list and a WordId list (corresponding order), 
# and transforms that into a filled in char grid.
# char list * WordId list -> char list list
def wordClassListToGrid(grid, solution, widList):
	newGrid = removeLetters(grid, replace=Constants.defaultEmptyChar)
	startPosDict = startPositionsDict(newGrid)
	for i, word in enumerate(solution):
		wid = widList[i]
		fillInWord(newGrid, word, wid.dir, *startPosDict[wid])
	return newGrid

# -----------------------------------------------------------------

if __name__ == "__main__":
	
	example1 = [[' ', 'a', ' ', '#'], ['#', 's', '#', 'a'], ['#', '#', 'k', ' ']]
	# Photo stored in Desktop
	fullNYT = [	['h', 'e', 'l', 'l', '#', '#', 'w', 'e', 'l', 'l', '#', 'a', 'm', 'p', 's'],
				['o', 'w', 'i', 'e', '#', 's', 'o', 'd', 'o', 'i', '#', 'c', 'a', 'l', 'l'], 
				['b', 'a', 'n', 'g', '#', 't', 'r', 'u', 't', 'v', '#', 'c', 'r', 'a', 'y'], 
				['o', 'n', 'e', 'w', 'o', 'o', 'd', '#', 's', 'e', 't', 'r', 'r', 't', 'e'], 
				['#', '#', '#', 'a', 'm', 'i', 's', 'h', '#', 'b', 'r', 'a', 'c', 'e', 's'], 
				['a', 'd', 'e', 'x', 'e', 'c', '#', 'a', 'l', 'l', 'a', '#', 'a', 'n', 't'], 
				['b', 'a', 'l', 'i', 'n', '#', 'g', 'l', 'o', 'o', 'p', 's', '#', '#', '#'], 
				['c', 'h', 'i', 'n', '#', 's', 'o', 'f', 't', 'g', '#', 'p', 'o', 'o', 'h'], 
				['#', '#', '#', 'g', 'a', 'l', 'o', 'o', 't', '#', 't', 'i', 'a', 'r', 'a'], 
				['i', 'r', 's', '#', 'b', 'o', 'f', 'f', '#', 'j', 'u', 'n', 'k', 'e', 't'], 
				['t', 'e', 'e', 's', 'u', 'p', '#', 'f', 'r', 'a', 'n', 'c', '#', '#', '#'], 
				['s', 'w', 'e', 'a', 't', 'i', 't', '#', 'a', 'd', 'a', 'y', 'a', 'g', 'o'], 
				['s', 'i', 'n', 'g', '#', 't', 'i', 'n', 'g', 'e', '#', 'c', 'h', 'o', 'p'], 
				['a', 'r', 'i', 'a', '#', 'c', 'r', 'e', 'e', 'd', '#', 'l', 'o', 'n', 'e'], 
				['d', 'e', 'n', 's', '#', 'h', 'e', 'a', 'r', '#', '#', 'e', 'y', 'e', 'd'] ]

	# Expected output

	example1LettersRemoved = [[' ', ' ', ' ', '#'], ['#', ' ', '#', ' '], ['#', '#', ' ', ' ']]
	example1PopulateWithIth = [[1, 2, ' ', '#'], ['#', ' ', '#', 3], ['#', '#', 4, ' ']]
	example1PopulateWithInfo = [[[SquareWordInfo(wid=WordId(ith=1, dir='Across'), len=3, pos=1)], 
									[SquareWordInfo(wid=WordId(ith=1, dir='Across'), len=3, pos=2), SquareWordInfo(wid=WordId(ith=2, dir='Down'), len=2, pos=1)], 
										[SquareWordInfo(wid=WordId(ith=1, dir='Across'), len=3, pos=3)], 
											'#'], 
								['#', 
									[SquareWordInfo(wid=WordId(ith=2, dir='Down'), len=2, pos=2)], 
										'#', 
											[SquareWordInfo(wid=WordId(ith=3, dir='Down'), len=2, pos=1)]], 
								['#', 
									'#', 
										[SquareWordInfo(wid=WordId(ith=4, dir='Across'), len=2, pos=1)], 
											[SquareWordInfo(wid=WordId(ith=3, dir='Down'), len=2, pos=2), SquareWordInfo(wid=WordId(ith=4, dir='Across'), len=2, pos=2)]]]
	example1StartPositionsDict = {WordId(ith=1, dir='Across'): (0, 0), WordId(ith=2, dir='Down'): (0, 1), WordId(ith=3, dir='Down'): (1, 3), WordId(ith=4, dir='Across'): (2, 2)}

	fullNYTLettersRemoved = [[' ', ' ', ' ', ' ', '#', '#', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' '], ['#', '#', '#', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', '#', '#', '#'], [' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' '], ['#', '#', '#', ' ', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', '#', '#', '#'], [' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', '#', '#', ' ', ' ', ' ', ' ']]
	fullNYTPopulateWithIth = [[1, 2, 3, 4, '#', '#', 5, 6, 7, 8, '#', 9, 10, 11, 12], [13, ' ', ' ', ' ', '#', 14, ' ', ' ', ' ', ' ', '#', 15, ' ', ' ', ' '], [16, ' ', ' ', ' ', '#', 17, ' ', ' ', ' ', ' ', '#', 18, ' ', ' ', ' '], [19, ' ', ' ', ' ', 20, ' ', ' ', '#', 21, ' ', 22, ' ', ' ', ' ', ' '], ['#', '#', '#', 23, ' ', ' ', ' ', 24, '#', 25, ' ', ' ', ' ', ' ', ' '], [26, 27, 28, ' ', ' ', ' ', '#', 29, 30, ' ', ' ', '#', 31, ' ', ' '], [32, ' ', ' ', ' ', ' ', '#', 33, ' ', ' ', ' ', ' ', 34, '#', '#', '#'], [35, ' ', ' ', ' ', '#', 36, ' ', ' ', ' ', ' ', '#', 37, 38, 39, 40], ['#', '#', '#', 41, 42, ' ', ' ', ' ', ' ', '#', 43, ' ', ' ', ' ', ' '], [44, 45, 46, '#', 47, ' ', ' ', ' ', '#', 48, ' ', ' ', ' ', ' ', ' '], [49, ' ', ' ', 50, ' ', ' ', '#', 51, 52, ' ', ' ', ' ', '#', '#', '#'], [53, ' ', ' ', ' ', ' ', ' ', 54, '#', 55, ' ', ' ', ' ', 56, 57, 58], [59, ' ', ' ', ' ', '#', 60, ' ', 61, ' ', ' ', '#', 62, ' ', ' ', ' '], [63, ' ', ' ', ' ', '#', 64, ' ', ' ', ' ', ' ', '#', 65, ' ', ' ', ' '], [66, ' ', ' ', ' ', '#', 67, ' ', ' ', ' ', '#', '#', 68, ' ', ' ', ' ']]
	fullNYTPopulateWithInfo = [[[SquareWordInfo(wid=WordId(ith=1, dir='Across'), len=4, pos=1), SquareWordInfo(wid=WordId(ith=1, dir='Down'), len=4, pos=1)], [SquareWordInfo(wid=WordId(ith=1, dir='Across'), len=4, pos=2), SquareWordInfo(wid=WordId(ith=2, dir='Down'), len=4, pos=1)], [SquareWordInfo(wid=WordId(ith=1, dir='Across'), len=4, pos=3), SquareWordInfo(wid=WordId(ith=3, dir='Down'), len=4, pos=1)], [SquareWordInfo(wid=WordId(ith=1, dir='Across'), len=4, pos=4), SquareWordInfo(wid=WordId(ith=4, dir='Down'), len=9, pos=1)], '#', '#', [SquareWordInfo(wid=WordId(ith=5, dir='Across'), len=4, pos=1), SquareWordInfo(wid=WordId(ith=5, dir='Down'), len=5, pos=1)], [SquareWordInfo(wid=WordId(ith=5, dir='Across'), len=4, pos=2), SquareWordInfo(wid=WordId(ith=6, dir='Down'), len=3, pos=1)], [SquareWordInfo(wid=WordId(ith=5, dir='Across'), len=4, pos=3), SquareWordInfo(wid=WordId(ith=7, dir='Down'), len=4, pos=1)], [SquareWordInfo(wid=WordId(ith=5, dir='Across'), len=4, pos=4), SquareWordInfo(wid=WordId(ith=8, dir='Down'), len=8, pos=1)], '#', [SquareWordInfo(wid=WordId(ith=9, dir='Across'), len=4, pos=1), SquareWordInfo(wid=WordId(ith=9, dir='Down'), len=5, pos=1)], [SquareWordInfo(wid=WordId(ith=9, dir='Across'), len=4, pos=2), SquareWordInfo(wid=WordId(ith=10, dir='Down'), len=6, pos=1)], [SquareWordInfo(wid=WordId(ith=9, dir='Across'), len=4, pos=3), SquareWordInfo(wid=WordId(ith=11, dir='Down'), len=6, pos=1)], [SquareWordInfo(wid=WordId(ith=9, dir='Across'), len=4, pos=4), SquareWordInfo(wid=WordId(ith=12, dir='Down'), len=6, pos=1)]], [[SquareWordInfo(wid=WordId(ith=1, dir='Down'), len=4, pos=2), SquareWordInfo(wid=WordId(ith=13, dir='Across'), len=4, pos=1)], [SquareWordInfo(wid=WordId(ith=2, dir='Down'), len=4, pos=2), SquareWordInfo(wid=WordId(ith=13, dir='Across'), len=4, pos=2)], [SquareWordInfo(wid=WordId(ith=3, dir='Down'), len=4, pos=2), SquareWordInfo(wid=WordId(ith=13, dir='Across'), len=4, pos=3)], [SquareWordInfo(wid=WordId(ith=4, dir='Down'), len=9, pos=2), SquareWordInfo(wid=WordId(ith=13, dir='Across'), len=4, pos=4)], '#', [SquareWordInfo(wid=WordId(ith=14, dir='Across'), len=5, pos=1), SquareWordInfo(wid=WordId(ith=14, dir='Down'), len=5, pos=1)], [SquareWordInfo(wid=WordId(ith=5, dir='Down'), len=5, pos=2), SquareWordInfo(wid=WordId(ith=14, dir='Across'), len=5, pos=2)], [SquareWordInfo(wid=WordId(ith=6, dir='Down'), len=3, pos=2), SquareWordInfo(wid=WordId(ith=14, dir='Across'), len=5, pos=3)], [SquareWordInfo(wid=WordId(ith=7, dir='Down'), len=4, pos=2), SquareWordInfo(wid=WordId(ith=14, dir='Across'), len=5, pos=4)], [SquareWordInfo(wid=WordId(ith=8, dir='Down'), len=8, pos=2), SquareWordInfo(wid=WordId(ith=14, dir='Across'), len=5, pos=5)], '#', [SquareWordInfo(wid=WordId(ith=9, dir='Down'), len=5, pos=2), SquareWordInfo(wid=WordId(ith=15, dir='Across'), len=4, pos=1)], [SquareWordInfo(wid=WordId(ith=10, dir='Down'), len=6, pos=2), SquareWordInfo(wid=WordId(ith=15, dir='Across'), len=4, pos=2)], [SquareWordInfo(wid=WordId(ith=11, dir='Down'), len=6, pos=2), SquareWordInfo(wid=WordId(ith=15, dir='Across'), len=4, pos=3)], [SquareWordInfo(wid=WordId(ith=12, dir='Down'), len=6, pos=2), SquareWordInfo(wid=WordId(ith=15, dir='Across'), len=4, pos=4)]], [[SquareWordInfo(wid=WordId(ith=1, dir='Down'), len=4, pos=3), SquareWordInfo(wid=WordId(ith=16, dir='Across'), len=4, pos=1)], [SquareWordInfo(wid=WordId(ith=2, dir='Down'), len=4, pos=3), SquareWordInfo(wid=WordId(ith=16, dir='Across'), len=4, pos=2)], [SquareWordInfo(wid=WordId(ith=3, dir='Down'), len=4, pos=3), SquareWordInfo(wid=WordId(ith=16, dir='Across'), len=4, pos=3)], [SquareWordInfo(wid=WordId(ith=4, dir='Down'), len=9, pos=3), SquareWordInfo(wid=WordId(ith=16, dir='Across'), len=4, pos=4)], '#', [SquareWordInfo(wid=WordId(ith=14, dir='Down'), len=5, pos=2), SquareWordInfo(wid=WordId(ith=17, dir='Across'), len=5, pos=1)], [SquareWordInfo(wid=WordId(ith=5, dir='Down'), len=5, pos=3), SquareWordInfo(wid=WordId(ith=17, dir='Across'), len=5, pos=2)], [SquareWordInfo(wid=WordId(ith=6, dir='Down'), len=3, pos=3), SquareWordInfo(wid=WordId(ith=17, dir='Across'), len=5, pos=3)], [SquareWordInfo(wid=WordId(ith=7, dir='Down'), len=4, pos=3), SquareWordInfo(wid=WordId(ith=17, dir='Across'), len=5, pos=4)], [SquareWordInfo(wid=WordId(ith=8, dir='Down'), len=8, pos=3), SquareWordInfo(wid=WordId(ith=17, dir='Across'), len=5, pos=5)], '#', [SquareWordInfo(wid=WordId(ith=9, dir='Down'), len=5, pos=3), SquareWordInfo(wid=WordId(ith=18, dir='Across'), len=4, pos=1)], [SquareWordInfo(wid=WordId(ith=10, dir='Down'), len=6, pos=3), SquareWordInfo(wid=WordId(ith=18, dir='Across'), len=4, pos=2)], [SquareWordInfo(wid=WordId(ith=11, dir='Down'), len=6, pos=3), SquareWordInfo(wid=WordId(ith=18, dir='Across'), len=4, pos=3)], [SquareWordInfo(wid=WordId(ith=12, dir='Down'), len=6, pos=3), SquareWordInfo(wid=WordId(ith=18, dir='Across'), len=4, pos=4)]], [[SquareWordInfo(wid=WordId(ith=1, dir='Down'), len=4, pos=4), SquareWordInfo(wid=WordId(ith=19, dir='Across'), len=7, pos=1)], [SquareWordInfo(wid=WordId(ith=2, dir='Down'), len=4, pos=4), SquareWordInfo(wid=WordId(ith=19, dir='Across'), len=7, pos=2)], [SquareWordInfo(wid=WordId(ith=3, dir='Down'), len=4, pos=4), SquareWordInfo(wid=WordId(ith=19, dir='Across'), len=7, pos=3)], [SquareWordInfo(wid=WordId(ith=4, dir='Down'), len=9, pos=4), SquareWordInfo(wid=WordId(ith=19, dir='Across'), len=7, pos=4)], [SquareWordInfo(wid=WordId(ith=19, dir='Across'), len=7, pos=5), SquareWordInfo(wid=WordId(ith=20, dir='Down'), len=4, pos=1)], [SquareWordInfo(wid=WordId(ith=14, dir='Down'), len=5, pos=3), SquareWordInfo(wid=WordId(ith=19, dir='Across'), len=7, pos=6)], [SquareWordInfo(wid=WordId(ith=5, dir='Down'), len=5, pos=4), SquareWordInfo(wid=WordId(ith=19, dir='Across'), len=7, pos=7)], '#', [SquareWordInfo(wid=WordId(ith=7, dir='Down'), len=4, pos=4), SquareWordInfo(wid=WordId(ith=21, dir='Across'), len=7, pos=1)], [SquareWordInfo(wid=WordId(ith=8, dir='Down'), len=8, pos=4), SquareWordInfo(wid=WordId(ith=21, dir='Across'), len=7, pos=2)], [SquareWordInfo(wid=WordId(ith=21, dir='Across'), len=7, pos=3), SquareWordInfo(wid=WordId(ith=22, dir='Down'), len=4, pos=1)], [SquareWordInfo(wid=WordId(ith=9, dir='Down'), len=5, pos=4), SquareWordInfo(wid=WordId(ith=21, dir='Across'), len=7, pos=4)], [SquareWordInfo(wid=WordId(ith=10, dir='Down'), len=6, pos=4), SquareWordInfo(wid=WordId(ith=21, dir='Across'), len=7, pos=5)], [SquareWordInfo(wid=WordId(ith=11, dir='Down'), len=6, pos=4), SquareWordInfo(wid=WordId(ith=21, dir='Across'), len=7, pos=6)], [SquareWordInfo(wid=WordId(ith=12, dir='Down'), len=6, pos=4), SquareWordInfo(wid=WordId(ith=21, dir='Across'), len=7, pos=7)]], ['#', '#', '#', [SquareWordInfo(wid=WordId(ith=4, dir='Down'), len=9, pos=5), SquareWordInfo(wid=WordId(ith=23, dir='Across'), len=5, pos=1)], [SquareWordInfo(wid=WordId(ith=20, dir='Down'), len=4, pos=2), SquareWordInfo(wid=WordId(ith=23, dir='Across'), len=5, pos=2)], [SquareWordInfo(wid=WordId(ith=14, dir='Down'), len=5, pos=4), SquareWordInfo(wid=WordId(ith=23, dir='Across'), len=5, pos=3)], [SquareWordInfo(wid=WordId(ith=5, dir='Down'), len=5, pos=5), SquareWordInfo(wid=WordId(ith=23, dir='Across'), len=5, pos=4)], [SquareWordInfo(wid=WordId(ith=23, dir='Across'), len=5, pos=5), SquareWordInfo(wid=WordId(ith=24, dir='Down'), len=7, pos=1)], '#', [SquareWordInfo(wid=WordId(ith=8, dir='Down'), len=8, pos=5), SquareWordInfo(wid=WordId(ith=25, dir='Across'), len=6, pos=1)], [SquareWordInfo(wid=WordId(ith=22, dir='Down'), len=4, pos=2), SquareWordInfo(wid=WordId(ith=25, dir='Across'), len=6, pos=2)], [SquareWordInfo(wid=WordId(ith=9, dir='Down'), len=5, pos=5), SquareWordInfo(wid=WordId(ith=25, dir='Across'), len=6, pos=3)], [SquareWordInfo(wid=WordId(ith=10, dir='Down'), len=6, pos=5), SquareWordInfo(wid=WordId(ith=25, dir='Across'), len=6, pos=4)], [SquareWordInfo(wid=WordId(ith=11, dir='Down'), len=6, pos=5), SquareWordInfo(wid=WordId(ith=25, dir='Across'), len=6, pos=5)], [SquareWordInfo(wid=WordId(ith=12, dir='Down'), len=6, pos=5), SquareWordInfo(wid=WordId(ith=25, dir='Across'), len=6, pos=6)]], [[SquareWordInfo(wid=WordId(ith=26, dir='Across'), len=6, pos=1), SquareWordInfo(wid=WordId(ith=26, dir='Down'), len=3, pos=1)], [SquareWordInfo(wid=WordId(ith=26, dir='Across'), len=6, pos=2), SquareWordInfo(wid=WordId(ith=27, dir='Down'), len=3, pos=1)], [SquareWordInfo(wid=WordId(ith=26, dir='Across'), len=6, pos=3), SquareWordInfo(wid=WordId(ith=28, dir='Down'), len=3, pos=1)], [SquareWordInfo(wid=WordId(ith=4, dir='Down'), len=9, pos=6), SquareWordInfo(wid=WordId(ith=26, dir='Across'), len=6, pos=4)], [SquareWordInfo(wid=WordId(ith=20, dir='Down'), len=4, pos=3), SquareWordInfo(wid=WordId(ith=26, dir='Across'), len=6, pos=5)], [SquareWordInfo(wid=WordId(ith=14, dir='Down'), len=5, pos=5), SquareWordInfo(wid=WordId(ith=26, dir='Across'), len=6, pos=6)], '#', [SquareWordInfo(wid=WordId(ith=24, dir='Down'), len=7, pos=2), SquareWordInfo(wid=WordId(ith=29, dir='Across'), len=4, pos=1)], [SquareWordInfo(wid=WordId(ith=29, dir='Across'), len=4, pos=2), SquareWordInfo(wid=WordId(ith=30, dir='Down'), len=4, pos=1)], [SquareWordInfo(wid=WordId(ith=8, dir='Down'), len=8, pos=6), SquareWordInfo(wid=WordId(ith=29, dir='Across'), len=4, pos=3)], [SquareWordInfo(wid=WordId(ith=22, dir='Down'), len=4, pos=3), SquareWordInfo(wid=WordId(ith=29, dir='Across'), len=4, pos=4)], '#', [SquareWordInfo(wid=WordId(ith=10, dir='Down'), len=6, pos=6), SquareWordInfo(wid=WordId(ith=31, dir='Across'), len=3, pos=1)], [SquareWordInfo(wid=WordId(ith=11, dir='Down'), len=6, pos=6), SquareWordInfo(wid=WordId(ith=31, dir='Across'), len=3, pos=2)], [SquareWordInfo(wid=WordId(ith=12, dir='Down'), len=6, pos=6), SquareWordInfo(wid=WordId(ith=31, dir='Across'), len=3, pos=3)]], [[SquareWordInfo(wid=WordId(ith=26, dir='Down'), len=3, pos=2), SquareWordInfo(wid=WordId(ith=32, dir='Across'), len=5, pos=1)], [SquareWordInfo(wid=WordId(ith=27, dir='Down'), len=3, pos=2), SquareWordInfo(wid=WordId(ith=32, dir='Across'), len=5, pos=2)], [SquareWordInfo(wid=WordId(ith=28, dir='Down'), len=3, pos=2), SquareWordInfo(wid=WordId(ith=32, dir='Across'), len=5, pos=3)], [SquareWordInfo(wid=WordId(ith=4, dir='Down'), len=9, pos=7), SquareWordInfo(wid=WordId(ith=32, dir='Across'), len=5, pos=4)], [SquareWordInfo(wid=WordId(ith=20, dir='Down'), len=4, pos=4), SquareWordInfo(wid=WordId(ith=32, dir='Across'), len=5, pos=5)], '#', [SquareWordInfo(wid=WordId(ith=33, dir='Across'), len=6, pos=1), SquareWordInfo(wid=WordId(ith=33, dir='Down'), len=4, pos=1)], [SquareWordInfo(wid=WordId(ith=24, dir='Down'), len=7, pos=3), SquareWordInfo(wid=WordId(ith=33, dir='Across'), len=6, pos=2)], [SquareWordInfo(wid=WordId(ith=30, dir='Down'), len=4, pos=2), SquareWordInfo(wid=WordId(ith=33, dir='Across'), len=6, pos=3)], [SquareWordInfo(wid=WordId(ith=8, dir='Down'), len=8, pos=7), SquareWordInfo(wid=WordId(ith=33, dir='Across'), len=6, pos=4)], [SquareWordInfo(wid=WordId(ith=22, dir='Down'), len=4, pos=4), SquareWordInfo(wid=WordId(ith=33, dir='Across'), len=6, pos=5)], [SquareWordInfo(wid=WordId(ith=33, dir='Across'), len=6, pos=6), SquareWordInfo(wid=WordId(ith=34, dir='Down'), len=9, pos=1)], '#', '#', '#'], [[SquareWordInfo(wid=WordId(ith=26, dir='Down'), len=3, pos=3), SquareWordInfo(wid=WordId(ith=35, dir='Across'), len=4, pos=1)], [SquareWordInfo(wid=WordId(ith=27, dir='Down'), len=3, pos=3), SquareWordInfo(wid=WordId(ith=35, dir='Across'), len=4, pos=2)], [SquareWordInfo(wid=WordId(ith=28, dir='Down'), len=3, pos=3), SquareWordInfo(wid=WordId(ith=35, dir='Across'), len=4, pos=3)], [SquareWordInfo(wid=WordId(ith=4, dir='Down'), len=9, pos=8), SquareWordInfo(wid=WordId(ith=35, dir='Across'), len=4, pos=4)], '#', [SquareWordInfo(wid=WordId(ith=36, dir='Across'), len=5, pos=1), SquareWordInfo(wid=WordId(ith=36, dir='Down'), len=8, pos=1)], [SquareWordInfo(wid=WordId(ith=33, dir='Down'), len=4, pos=2), SquareWordInfo(wid=WordId(ith=36, dir='Across'), len=5, pos=2)], [SquareWordInfo(wid=WordId(ith=24, dir='Down'), len=7, pos=4), SquareWordInfo(wid=WordId(ith=36, dir='Across'), len=5, pos=3)], [SquareWordInfo(wid=WordId(ith=30, dir='Down'), len=4, pos=3), SquareWordInfo(wid=WordId(ith=36, dir='Across'), len=5, pos=4)], [SquareWordInfo(wid=WordId(ith=8, dir='Down'), len=8, pos=8), SquareWordInfo(wid=WordId(ith=36, dir='Across'), len=5, pos=5)], '#', [SquareWordInfo(wid=WordId(ith=34, dir='Down'), len=9, pos=2), SquareWordInfo(wid=WordId(ith=37, dir='Across'), len=4, pos=1)], [SquareWordInfo(wid=WordId(ith=37, dir='Across'), len=4, pos=2), SquareWordInfo(wid=WordId(ith=38, dir='Down'), len=3, pos=1)], [SquareWordInfo(wid=WordId(ith=37, dir='Across'), len=4, pos=3), SquareWordInfo(wid=WordId(ith=39, dir='Down'), len=3, pos=1)], [SquareWordInfo(wid=WordId(ith=37, dir='Across'), len=4, pos=4), SquareWordInfo(wid=WordId(ith=40, dir='Down'), len=3, pos=1)]], ['#', '#', '#', [SquareWordInfo(wid=WordId(ith=4, dir='Down'), len=9, pos=9), SquareWordInfo(wid=WordId(ith=41, dir='Across'), len=6, pos=1)], [SquareWordInfo(wid=WordId(ith=41, dir='Across'), len=6, pos=2), SquareWordInfo(wid=WordId(ith=42, dir='Down'), len=4, pos=1)], [SquareWordInfo(wid=WordId(ith=36, dir='Down'), len=8, pos=2), SquareWordInfo(wid=WordId(ith=41, dir='Across'), len=6, pos=3)], [SquareWordInfo(wid=WordId(ith=33, dir='Down'), len=4, pos=3), SquareWordInfo(wid=WordId(ith=41, dir='Across'), len=6, pos=4)], [SquareWordInfo(wid=WordId(ith=24, dir='Down'), len=7, pos=5), SquareWordInfo(wid=WordId(ith=41, dir='Across'), len=6, pos=5)], [SquareWordInfo(wid=WordId(ith=30, dir='Down'), len=4, pos=4), SquareWordInfo(wid=WordId(ith=41, dir='Across'), len=6, pos=6)], '#', [SquareWordInfo(wid=WordId(ith=43, dir='Across'), len=5, pos=1), SquareWordInfo(wid=WordId(ith=43, dir='Down'), len=4, pos=1)], [SquareWordInfo(wid=WordId(ith=34, dir='Down'), len=9, pos=3), SquareWordInfo(wid=WordId(ith=43, dir='Across'), len=5, pos=2)], [SquareWordInfo(wid=WordId(ith=38, dir='Down'), len=3, pos=2), SquareWordInfo(wid=WordId(ith=43, dir='Across'), len=5, pos=3)], [SquareWordInfo(wid=WordId(ith=39, dir='Down'), len=3, pos=2), SquareWordInfo(wid=WordId(ith=43, dir='Across'), len=5, pos=4)], [SquareWordInfo(wid=WordId(ith=40, dir='Down'), len=3, pos=2), SquareWordInfo(wid=WordId(ith=43, dir='Across'), len=5, pos=5)]], [[SquareWordInfo(wid=WordId(ith=44, dir='Across'), len=3, pos=1), SquareWordInfo(wid=WordId(ith=44, dir='Down'), len=6, pos=1)], [SquareWordInfo(wid=WordId(ith=44, dir='Across'), len=3, pos=2), SquareWordInfo(wid=WordId(ith=45, dir='Down'), len=6, pos=1)], [SquareWordInfo(wid=WordId(ith=44, dir='Across'), len=3, pos=3), SquareWordInfo(wid=WordId(ith=46, dir='Down'), len=6, pos=1)], '#', [SquareWordInfo(wid=WordId(ith=42, dir='Down'), len=4, pos=2), SquareWordInfo(wid=WordId(ith=47, dir='Across'), len=4, pos=1)], [SquareWordInfo(wid=WordId(ith=36, dir='Down'), len=8, pos=3), SquareWordInfo(wid=WordId(ith=47, dir='Across'), len=4, pos=2)], [SquareWordInfo(wid=WordId(ith=33, dir='Down'), len=4, pos=4), SquareWordInfo(wid=WordId(ith=47, dir='Across'), len=4, pos=3)], [SquareWordInfo(wid=WordId(ith=24, dir='Down'), len=7, pos=6), SquareWordInfo(wid=WordId(ith=47, dir='Across'), len=4, pos=4)], '#', [SquareWordInfo(wid=WordId(ith=48, dir='Across'), len=6, pos=1), SquareWordInfo(wid=WordId(ith=48, dir='Down'), len=5, pos=1)], [SquareWordInfo(wid=WordId(ith=43, dir='Down'), len=4, pos=2), SquareWordInfo(wid=WordId(ith=48, dir='Across'), len=6, pos=2)], [SquareWordInfo(wid=WordId(ith=34, dir='Down'), len=9, pos=4), SquareWordInfo(wid=WordId(ith=48, dir='Across'), len=6, pos=3)], [SquareWordInfo(wid=WordId(ith=38, dir='Down'), len=3, pos=3), SquareWordInfo(wid=WordId(ith=48, dir='Across'), len=6, pos=4)], [SquareWordInfo(wid=WordId(ith=39, dir='Down'), len=3, pos=3), SquareWordInfo(wid=WordId(ith=48, dir='Across'), len=6, pos=5)], [SquareWordInfo(wid=WordId(ith=40, dir='Down'), len=3, pos=3), SquareWordInfo(wid=WordId(ith=48, dir='Across'), len=6, pos=6)]], [[SquareWordInfo(wid=WordId(ith=44, dir='Down'), len=6, pos=2), SquareWordInfo(wid=WordId(ith=49, dir='Across'), len=6, pos=1)], [SquareWordInfo(wid=WordId(ith=45, dir='Down'), len=6, pos=2), SquareWordInfo(wid=WordId(ith=49, dir='Across'), len=6, pos=2)], [SquareWordInfo(wid=WordId(ith=46, dir='Down'), len=6, pos=2), SquareWordInfo(wid=WordId(ith=49, dir='Across'), len=6, pos=3)], [SquareWordInfo(wid=WordId(ith=49, dir='Across'), len=6, pos=4), SquareWordInfo(wid=WordId(ith=50, dir='Down'), len=5, pos=1)], [SquareWordInfo(wid=WordId(ith=42, dir='Down'), len=4, pos=3), SquareWordInfo(wid=WordId(ith=49, dir='Across'), len=6, pos=5)], [SquareWordInfo(wid=WordId(ith=36, dir='Down'), len=8, pos=4), SquareWordInfo(wid=WordId(ith=49, dir='Across'), len=6, pos=6)], '#', [SquareWordInfo(wid=WordId(ith=24, dir='Down'), len=7, pos=7), SquareWordInfo(wid=WordId(ith=51, dir='Across'), len=5, pos=1)], [SquareWordInfo(wid=WordId(ith=51, dir='Across'), len=5, pos=2), SquareWordInfo(wid=WordId(ith=52, dir='Down'), len=5, pos=1)], [SquareWordInfo(wid=WordId(ith=48, dir='Down'), len=5, pos=2), SquareWordInfo(wid=WordId(ith=51, dir='Across'), len=5, pos=3)], [SquareWordInfo(wid=WordId(ith=43, dir='Down'), len=4, pos=3), SquareWordInfo(wid=WordId(ith=51, dir='Across'), len=5, pos=4)], [SquareWordInfo(wid=WordId(ith=34, dir='Down'), len=9, pos=5), SquareWordInfo(wid=WordId(ith=51, dir='Across'), len=5, pos=5)], '#', '#', '#'], [[SquareWordInfo(wid=WordId(ith=44, dir='Down'), len=6, pos=3), SquareWordInfo(wid=WordId(ith=53, dir='Across'), len=7, pos=1)], [SquareWordInfo(wid=WordId(ith=45, dir='Down'), len=6, pos=3), SquareWordInfo(wid=WordId(ith=53, dir='Across'), len=7, pos=2)], [SquareWordInfo(wid=WordId(ith=46, dir='Down'), len=6, pos=3), SquareWordInfo(wid=WordId(ith=53, dir='Across'), len=7, pos=3)], [SquareWordInfo(wid=WordId(ith=50, dir='Down'), len=5, pos=2), SquareWordInfo(wid=WordId(ith=53, dir='Across'), len=7, pos=4)], [SquareWordInfo(wid=WordId(ith=42, dir='Down'), len=4, pos=4), SquareWordInfo(wid=WordId(ith=53, dir='Across'), len=7, pos=5)], [SquareWordInfo(wid=WordId(ith=36, dir='Down'), len=8, pos=5), SquareWordInfo(wid=WordId(ith=53, dir='Across'), len=7, pos=6)], [SquareWordInfo(wid=WordId(ith=53, dir='Across'), len=7, pos=7), SquareWordInfo(wid=WordId(ith=54, dir='Down'), len=4, pos=1)], '#', [SquareWordInfo(wid=WordId(ith=52, dir='Down'), len=5, pos=2), SquareWordInfo(wid=WordId(ith=55, dir='Across'), len=7, pos=1)], [SquareWordInfo(wid=WordId(ith=48, dir='Down'), len=5, pos=3), SquareWordInfo(wid=WordId(ith=55, dir='Across'), len=7, pos=2)], [SquareWordInfo(wid=WordId(ith=43, dir='Down'), len=4, pos=4), SquareWordInfo(wid=WordId(ith=55, dir='Across'), len=7, pos=3)], [SquareWordInfo(wid=WordId(ith=34, dir='Down'), len=9, pos=6), SquareWordInfo(wid=WordId(ith=55, dir='Across'), len=7, pos=4)], [SquareWordInfo(wid=WordId(ith=55, dir='Across'), len=7, pos=5), SquareWordInfo(wid=WordId(ith=56, dir='Down'), len=4, pos=1)], [SquareWordInfo(wid=WordId(ith=55, dir='Across'), len=7, pos=6), SquareWordInfo(wid=WordId(ith=57, dir='Down'), len=4, pos=1)], [SquareWordInfo(wid=WordId(ith=55, dir='Across'), len=7, pos=7), SquareWordInfo(wid=WordId(ith=58, dir='Down'), len=4, pos=1)]], [[SquareWordInfo(wid=WordId(ith=44, dir='Down'), len=6, pos=4), SquareWordInfo(wid=WordId(ith=59, dir='Across'), len=4, pos=1)], [SquareWordInfo(wid=WordId(ith=45, dir='Down'), len=6, pos=4), SquareWordInfo(wid=WordId(ith=59, dir='Across'), len=4, pos=2)], [SquareWordInfo(wid=WordId(ith=46, dir='Down'), len=6, pos=4), SquareWordInfo(wid=WordId(ith=59, dir='Across'), len=4, pos=3)], [SquareWordInfo(wid=WordId(ith=50, dir='Down'), len=5, pos=3), SquareWordInfo(wid=WordId(ith=59, dir='Across'), len=4, pos=4)], '#', [SquareWordInfo(wid=WordId(ith=36, dir='Down'), len=8, pos=6), SquareWordInfo(wid=WordId(ith=60, dir='Across'), len=5, pos=1)], [SquareWordInfo(wid=WordId(ith=54, dir='Down'), len=4, pos=2), SquareWordInfo(wid=WordId(ith=60, dir='Across'), len=5, pos=2)], [SquareWordInfo(wid=WordId(ith=60, dir='Across'), len=5, pos=3), SquareWordInfo(wid=WordId(ith=61, dir='Down'), len=3, pos=1)], [SquareWordInfo(wid=WordId(ith=52, dir='Down'), len=5, pos=3), SquareWordInfo(wid=WordId(ith=60, dir='Across'), len=5, pos=4)], [SquareWordInfo(wid=WordId(ith=48, dir='Down'), len=5, pos=4), SquareWordInfo(wid=WordId(ith=60, dir='Across'), len=5, pos=5)], '#', [SquareWordInfo(wid=WordId(ith=34, dir='Down'), len=9, pos=7), SquareWordInfo(wid=WordId(ith=62, dir='Across'), len=4, pos=1)], [SquareWordInfo(wid=WordId(ith=56, dir='Down'), len=4, pos=2), SquareWordInfo(wid=WordId(ith=62, dir='Across'), len=4, pos=2)], [SquareWordInfo(wid=WordId(ith=57, dir='Down'), len=4, pos=2), SquareWordInfo(wid=WordId(ith=62, dir='Across'), len=4, pos=3)], [SquareWordInfo(wid=WordId(ith=58, dir='Down'), len=4, pos=2), SquareWordInfo(wid=WordId(ith=62, dir='Across'), len=4, pos=4)]], [[SquareWordInfo(wid=WordId(ith=44, dir='Down'), len=6, pos=5), SquareWordInfo(wid=WordId(ith=63, dir='Across'), len=4, pos=1)], [SquareWordInfo(wid=WordId(ith=45, dir='Down'), len=6, pos=5), SquareWordInfo(wid=WordId(ith=63, dir='Across'), len=4, pos=2)], [SquareWordInfo(wid=WordId(ith=46, dir='Down'), len=6, pos=5), SquareWordInfo(wid=WordId(ith=63, dir='Across'), len=4, pos=3)], [SquareWordInfo(wid=WordId(ith=50, dir='Down'), len=5, pos=4), SquareWordInfo(wid=WordId(ith=63, dir='Across'), len=4, pos=4)], '#', [SquareWordInfo(wid=WordId(ith=36, dir='Down'), len=8, pos=7), SquareWordInfo(wid=WordId(ith=64, dir='Across'), len=5, pos=1)], [SquareWordInfo(wid=WordId(ith=54, dir='Down'), len=4, pos=3), SquareWordInfo(wid=WordId(ith=64, dir='Across'), len=5, pos=2)], [SquareWordInfo(wid=WordId(ith=61, dir='Down'), len=3, pos=2), SquareWordInfo(wid=WordId(ith=64, dir='Across'), len=5, pos=3)], [SquareWordInfo(wid=WordId(ith=52, dir='Down'), len=5, pos=4), SquareWordInfo(wid=WordId(ith=64, dir='Across'), len=5, pos=4)], [SquareWordInfo(wid=WordId(ith=48, dir='Down'), len=5, pos=5), SquareWordInfo(wid=WordId(ith=64, dir='Across'), len=5, pos=5)], '#', [SquareWordInfo(wid=WordId(ith=34, dir='Down'), len=9, pos=8), SquareWordInfo(wid=WordId(ith=65, dir='Across'), len=4, pos=1)], [SquareWordInfo(wid=WordId(ith=56, dir='Down'), len=4, pos=3), SquareWordInfo(wid=WordId(ith=65, dir='Across'), len=4, pos=2)], [SquareWordInfo(wid=WordId(ith=57, dir='Down'), len=4, pos=3), SquareWordInfo(wid=WordId(ith=65, dir='Across'), len=4, pos=3)], [SquareWordInfo(wid=WordId(ith=58, dir='Down'), len=4, pos=3), SquareWordInfo(wid=WordId(ith=65, dir='Across'), len=4, pos=4)]], [[SquareWordInfo(wid=WordId(ith=44, dir='Down'), len=6, pos=6), SquareWordInfo(wid=WordId(ith=66, dir='Across'), len=4, pos=1)], [SquareWordInfo(wid=WordId(ith=45, dir='Down'), len=6, pos=6), SquareWordInfo(wid=WordId(ith=66, dir='Across'), len=4, pos=2)], [SquareWordInfo(wid=WordId(ith=46, dir='Down'), len=6, pos=6), SquareWordInfo(wid=WordId(ith=66, dir='Across'), len=4, pos=3)], [SquareWordInfo(wid=WordId(ith=50, dir='Down'), len=5, pos=5), SquareWordInfo(wid=WordId(ith=66, dir='Across'), len=4, pos=4)], '#', [SquareWordInfo(wid=WordId(ith=36, dir='Down'), len=8, pos=8), SquareWordInfo(wid=WordId(ith=67, dir='Across'), len=4, pos=1)], [SquareWordInfo(wid=WordId(ith=54, dir='Down'), len=4, pos=4), SquareWordInfo(wid=WordId(ith=67, dir='Across'), len=4, pos=2)], [SquareWordInfo(wid=WordId(ith=61, dir='Down'), len=3, pos=3), SquareWordInfo(wid=WordId(ith=67, dir='Across'), len=4, pos=3)], [SquareWordInfo(wid=WordId(ith=52, dir='Down'), len=5, pos=5), SquareWordInfo(wid=WordId(ith=67, dir='Across'), len=4, pos=4)], '#', '#', [SquareWordInfo(wid=WordId(ith=34, dir='Down'), len=9, pos=9), SquareWordInfo(wid=WordId(ith=68, dir='Across'), len=4, pos=1)], [SquareWordInfo(wid=WordId(ith=56, dir='Down'), len=4, pos=4), SquareWordInfo(wid=WordId(ith=68, dir='Across'), len=4, pos=2)], [SquareWordInfo(wid=WordId(ith=57, dir='Down'), len=4, pos=4), SquareWordInfo(wid=WordId(ith=68, dir='Across'), len=4, pos=3)], [SquareWordInfo(wid=WordId(ith=58, dir='Down'), len=4, pos=4), SquareWordInfo(wid=WordId(ith=68, dir='Across'), len=4, pos=4)]]]
	fullNYTStartPositionsDict = {WordId(ith=1, dir='Across'): (0, 0), WordId(ith=1, dir='Down'): (0, 0), WordId(ith=2, dir='Down'): (0, 1), WordId(ith=3, dir='Down'): (0, 2), WordId(ith=4, dir='Down'): (0, 3), WordId(ith=5, dir='Across'): (0, 6), WordId(ith=5, dir='Down'): (0, 6), WordId(ith=6, dir='Down'): (0, 7), WordId(ith=7, dir='Down'): (0, 8), WordId(ith=8, dir='Down'): (0, 9), WordId(ith=9, dir='Across'): (0, 11), WordId(ith=9, dir='Down'): (0, 11), WordId(ith=10, dir='Down'): (0, 12), WordId(ith=11, dir='Down'): (0, 13), WordId(ith=12, dir='Down'): (0, 14), WordId(ith=13, dir='Across'): (1, 0), WordId(ith=14, dir='Across'): (1, 5), WordId(ith=14, dir='Down'): (1, 5), WordId(ith=15, dir='Across'): (1, 11), WordId(ith=16, dir='Across'): (2, 0), WordId(ith=17, dir='Across'): (2, 5), WordId(ith=18, dir='Across'): (2, 11), WordId(ith=19, dir='Across'): (3, 0), WordId(ith=20, dir='Down'): (3, 4), WordId(ith=21, dir='Across'): (3, 8), WordId(ith=22, dir='Down'): (3, 10), WordId(ith=23, dir='Across'): (4, 3), WordId(ith=24, dir='Down'): (4, 7), WordId(ith=25, dir='Across'): (4, 9), WordId(ith=26, dir='Across'): (5, 0), WordId(ith=26, dir='Down'): (5, 0), WordId(ith=27, dir='Down'): (5, 1), WordId(ith=28, dir='Down'): (5, 2), WordId(ith=29, dir='Across'): (5, 7), WordId(ith=30, dir='Down'): (5, 8), WordId(ith=31, dir='Across'): (5, 12), WordId(ith=32, dir='Across'): (6, 0), WordId(ith=33, dir='Across'): (6, 6), WordId(ith=33, dir='Down'): (6, 6), WordId(ith=34, dir='Down'): (6, 11), WordId(ith=35, dir='Across'): (7, 0), WordId(ith=36, dir='Across'): (7, 5), WordId(ith=36, dir='Down'): (7, 5), WordId(ith=37, dir='Across'): (7, 11), WordId(ith=38, dir='Down'): (7, 12), WordId(ith=39, dir='Down'): (7, 13), WordId(ith=40, dir='Down'): (7, 14), WordId(ith=41, dir='Across'): (8, 3), WordId(ith=42, dir='Down'): (8, 4), WordId(ith=43, dir='Across'): (8, 10), WordId(ith=43, dir='Down'): (8, 10), WordId(ith=44, dir='Across'): (9, 0), WordId(ith=44, dir='Down'): (9, 0), WordId(ith=45, dir='Down'): (9, 1), WordId(ith=46, dir='Down'): (9, 2), WordId(ith=47, dir='Across'): (9, 4), WordId(ith=48, dir='Across'): (9, 9), WordId(ith=48, dir='Down'): (9, 9), WordId(ith=49, dir='Across'): (10, 0), WordId(ith=50, dir='Down'): (10, 3), WordId(ith=51, dir='Across'): (10, 7), WordId(ith=52, dir='Down'): (10, 8), WordId(ith=53, dir='Across'): (11, 0), WordId(ith=54, dir='Down'): (11, 6), WordId(ith=55, dir='Across'): (11, 8), WordId(ith=56, dir='Down'): (11, 12), WordId(ith=57, dir='Down'): (11, 13), WordId(ith=58, dir='Down'): (11, 14), WordId(ith=59, dir='Across'): (12, 0), WordId(ith=60, dir='Across'): (12, 5), WordId(ith=61, dir='Down'): (12, 7), WordId(ith=62, dir='Across'): (12, 11), WordId(ith=63, dir='Across'): (13, 0), WordId(ith=64, dir='Across'): (13, 5), WordId(ith=65, dir='Across'): (13, 11), WordId(ith=66, dir='Across'): (14, 0), WordId(ith=67, dir='Across'): (14, 5), WordId(ith=68, dir='Across'): (14, 11)}
	
	# Tests

	# Basic functions 

	assert(removeLetters(example1) == example1LettersRemoved)
	assert(populateWithIth(example1) == example1PopulateWithIth)
	assert(populateWithInfo(example1) == example1PopulateWithInfo)
	assert(startPositionsDict(example1) == example1StartPositionsDict)

	assert(removeLetters(fullNYT) == fullNYTLettersRemoved)
	assert(populateWithIth(fullNYT) == fullNYTPopulateWithIth)
	assert(populateWithInfo(fullNYT) == fullNYTPopulateWithInfo)
	assert(startPositionsDict(fullNYT) == fullNYTStartPositionsDict)

	# Correctness test case for gridToWordClassList
	
	wordClassList = gridToWordClassList(example1)
	word0 = wordClassList[0]
	word1 = wordClassList[1]
	word2 = wordClassList[2]
	word3 = wordClassList[3]

	# Correct linking
	assert(word0._pointers[2] == word1)
	assert(word0._indices[2] == 1)
	assert(word1._pointers[1] == word0)
	assert(word1._indices[1] == 2)
	assert(word2._pointers[2] == word3)
	assert(word2._indices[2] == 2)
	assert(word3._pointers[2] == word2)
	assert(word3._indices[2] == 2)

	# Correct letter substitution
	# example1 = [[' ', 'a', ' ', '#'], ['#', 's', '#', 'a'], ['#', '#', 'k', ' ']]
	assert(word0._chars[1] == Constants.defaultEmptyChar)
	assert(word0._chars[2] == 'a')
	assert(word0._chars[3] == Constants.defaultEmptyChar)
	assert(word1._chars[1] == 'a')
	assert(word1._chars[2] == 's')
	assert(word2._chars[1] == 'a')
	assert(word2._chars[2] == Constants.defaultEmptyChar)
	assert(word3._chars[1] == 'k')
	assert(word3._chars[2] == Constants.defaultEmptyChar)

	# Test case for wordClassListToGrid
	wids = [WordId(ith=4, dir='Across'), WordId(ith=3, dir='Down'), WordId(ith=2, dir='Down'), WordId(ith=1, dir='Across')]
	solution = ["in", "an", "ye", "bye"]
	expected = [['b', 'y', 'e', '#'], ['#', 'e', '#', 'a'], ['#', '#', 'i', 'n']]
	filledInGrid = wordClassListToGrid(example1, solution, wids)
	assert(filledInGrid == expected)

	print("Success: All tests passed")













































