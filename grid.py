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