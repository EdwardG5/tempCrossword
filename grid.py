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

# Data type to store information about a word in the context of a particular square
# Id = 1, 2, 3, ..
# Dir = "Above", "Down"
# Len = Length of the word
# Constrained = Number of letters of that word which are linked to other words
# Pos = ith letter, starting at 1
SquareWordInfo = namedtuple('SquareWordInfo', ['id', 'dir', 'len', 'pos'])

# Count the length of the word starting at row, col, going in direction dire
# grid : any type of grid
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
			info = SquareWordInfo(ith, "Across", length, pos)
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
			info = SquareWordInfo(ith, "Down", length, pos)
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
		grid[row][col].append(ith)
	except:
		pass

# Produces a grid with ith numbers in the squares starting crossword words. Used for drawing
# small numbers. 
populateWithIth = startingSquaresOne(f, replace=Constants.defaultEmptyChar)

# -----------------------------------------------------------------

def fA(mDict, row, col, ith):
	mDict[(ith, "Across")] = (row, col)

def fD(mDict, row, col, ith):
	mDict[(ith, "Down")] = (row, col)

# Produces a dict e.g. {(1, "Above") : (row, col), (1, "Down") : (row, col), ...}
startPosDict = startingSquaresGlobal(fA, fD, {})

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

# Convert a grid into a list of fully linked word class objects
# str list list -> wordClass list
def gridToWordClassList(grid):
	infoGrid = populateWithInfo(grid)
	startPosDict = startPositionsDict(grid)
	wcDict = {}
	# Create words
	for row, col in startPosDict.values():
		for wordInfo in infoGrid[row][col]:
			wid, wdir, wlen = wordInfo.id, wordInfo.dir, wordInfo.length
			wconstrained = gConstrained(grid, wdir, *startPosDict[(wid, wdir)])
			wcDict[(wid, wdir)] = Word(wlen, wconstrained, 0, (wid, wdir))
	# Link words
	for word in wcDict:
		row, col = startPosDict[word._id]
		wdir = word[1]
		rowIncr = 1 if wdir == "Across" else 0
		colIncr = 1-rowIncr
		for i in range(word._length):
			# Two words intersecting
			if len(infoGrid[row][col]) == 2:
				words = infoGrid[row][col]
				otherWordInfo = words[0] if (word._id == (words[1].id, words[1].dir)) else words[1]
				owid, owpos = (otherWordInfo.id, otherWordInfo.pos), otherWordInfo.pos
				word._pointers[i+1], word._indices[i+1] = (wcDict[owid], owpos)
			row += rowIncr
			col += colIncr
	return list(wcDict.values())

# -----------------------------------------------------------------

# Simple correctness test case:

example1 = [['a', 'a', 'd', '#'], ['#', 's', '#', 'a'], ['#', '#', 'k', ' ']]

wordClassList = gridToWordClassList(example1)

word0 = wordClassList[0]
word1 = wordClassList[1]
word2 = wordClassList[2]
word3 = wordClassList[3]

assert(word0._pointers[2] == word1)
assert(word0._indices[2] == 1)
assert(word1._pointers[1] == word0)
assert(word1._indices[1] == 2)
assert(word2._pointers[2] == word3)
assert(word2._indices[2] == 2)
assert(word3._pointers[2] == word2)
assert(word3._indices[2] == 2)















# example1 = [['a', 'a', 'd', '#'], ['#', 's', '#', 'a'], ['#', '#', 'k', ' ']]

# def f(mList, row, col, ith):
# 	mList.append('z')

# x = []
# startPosList = startingSquaresGlobal(f, f, x)

# a = startPosList(example1)
# print(a)
# b = startPosList(example1)
# print(b)

# input()





# from crosswordSolver import solve
# solutions = solve(wordClassList)


# # Convert a list of word class objects into a char grid
# def wordClassListToGrid(wL):
# 	pass

# if __name__ == "__main__":
	
# 	example1 = [['a', 'a', 'd', '#'], ['#', 's', '#', 'a'], ['#', '#', 'k', ' ']]
# 	# Photo stored in Desktop
# 	fullNYT = [	['h', 'e', 'l', 'l', '#', '#', 'w', 'e', 'l', 'l', '#', 'a', 'm', 'p', 's'],
# 				['o', 'w', 'i', 'e', '#', 's', 'o', 'd', 'o', 'i', '#', 'c', 'a', 'l', 'l'], 
# 				['b', 'a', 'n', 'g', '#', 't', 'r', 'u', 't', 'v', '#', 'c', 'r', 'a', 'y'], 
# 				['o', 'n', 'e', 'w', 'o', 'o', 'd', '#', 's', 'e', 't', 'r', 'r', 't', 'e'], 
# 				['#', '#', '#', 'a', 'm', 'i', 's', 'h', '#', 'b', 'r', 'a', 'c', 'e', 's'], 
# 				['a', 'd', 'e', 'x', 'e', 'c', '#', 'a', 'l', 'l', 'a', '#', 'a', 'n', 't'], 
# 				['b', 'a', 'l', 'i', 'n', '#', 'g', 'l', 'o', 'o', 'p', 's', '#', '#', '#'], 
# 				['c', 'h', 'i', 'n', '#', 's', 'o', 'f', 't', 'g', '#', 'p', 'o', 'o', 'h'], 
# 				['#', '#', '#', 'g', 'a', 'l', 'o', 'o', 't', '#', 't', 'i', 'a', 'r', 'a'], 
# 				['i', 'r', 's', '#', 'b', 'o', 'f', 'f', '#', 'j', 'u', 'n', 'k', 'e', 't'], 
# 				['t', 'e', 'e', 's', 'u', 'p', '#', 'f', 'r', 'a', 'n', 'c', '#', '#', '#'], 
# 				['s', 'w', 'e', 'a', 't', 'i', 't', '#', 'a', 'd', 'a', 'y', 'a', 'g', 'o'], 
# 				['s', 'i', 'n', 'g', '#', 't', 'i', 'n', 'g', 'e', '#', 'c', 'h', 'o', 'p'], 
# 				['a', 'r', 'i', 'a', '#', 'c', 'r', 'e', 'e', 'd', '#', 'l', 'o', 'n', 'e'], 
# 				['d', 'e', 'n', 's', '#', 'h', 'e', 'a', 'r', '#', '#', 'e', 'y', 'e', 'd'] ]
# 	example1LettersRemoved = [[' ', ' ', ' ', '#'], ['#', ' ', '#', ' '], ['#', '#', ' ', ' ']]
# 	example1StartIdentifiers = [[1, 2, ' ', '#'], ['#', ' ', '#', 3], ['#', '#', 4, ' ']] 
# 	example1WordIdentifiers = [[[(1, 'Across')], [(1, 'Across'), (2, 'Down')], [(1, 'Across')], '#'], ['#', [(2, 'Down')], '#', [(3, 'Down')]], ['#', '#', [(4, 'Across')], [(3, 'Down'), (4, 'Across')]]]
# 	fullNYTLettersRemoved = [[' ', ' ', ' ', ' ', '#', '#', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' '], ['#', '#', '#', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', '#', '#', '#'], [' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' '], ['#', '#', '#', ' ', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', '#', '#', '#'], [' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', '#', '#', ' ', ' ', ' ', ' ']]
# 	fullNYTStartIdentifiers = [[1, 2, 3, 4, '#', '#', 5, 6, 7, 8, '#', 9, 10, 11, 12], [13, ' ', ' ', ' ', '#', 14, ' ', ' ', ' ', ' ', '#', 15, ' ', ' ', ' '], [16, ' ', ' ', ' ', '#', 17, ' ', ' ', ' ', ' ', '#', 18, ' ', ' ', ' '], [19, ' ', ' ', ' ', 20, ' ', ' ', '#', 21, ' ', 22, ' ', ' ', ' ', ' '], ['#', '#', '#', 23, ' ', ' ', ' ', 24, '#', 25, ' ', ' ', ' ', ' ', ' '], [26, 27, 28, ' ', ' ', ' ', '#', 29, 30, ' ', ' ', '#', 31, ' ', ' '], [32, ' ', ' ', ' ', ' ', '#', 33, ' ', ' ', ' ', ' ', 34, '#', '#', '#'], [35, ' ', ' ', ' ', '#', 36, ' ', ' ', ' ', ' ', '#', 37, 38, 39, 40], ['#', '#', '#', 41, 42, ' ', ' ', ' ', ' ', '#', 43, ' ', ' ', ' ', ' '], [44, 45, 46, '#', 47, ' ', ' ', ' ', '#', 48, ' ', ' ', ' ', ' ', ' '], [49, ' ', ' ', 50, ' ', ' ', '#', 51, 52, ' ', ' ', ' ', '#', '#', '#'], [53, ' ', ' ', ' ', ' ', ' ', 54, '#', 55, ' ', ' ', ' ', 56, 57, 58], [59, ' ', ' ', ' ', '#', 60, ' ', 61, ' ', ' ', '#', 62, ' ', ' ', ' '], [63, ' ', ' ', ' ', '#', 64, ' ', ' ', ' ', ' ', '#', 65, ' ', ' ', ' '], [66, ' ', ' ', ' ', '#', 67, ' ', ' ', ' ', '#', '#', 68, ' ', ' ', ' ']]
# 	fullNYTWordIdentifiers = [[[(1, 'Across'), (1, 'Down')], [(1, 'Across'), (2, 'Down')], [(1, 'Across'), (3, 'Down')], [(1, 'Across'), (4, 'Down')], '#', '#', [(5, 'Across'), (5, 'Down')], [(5, 'Across'), (6, 'Down')], [(5, 'Across'), (7, 'Down')], [(5, 'Across'), (8, 'Down')], '#', [(9, 'Across'), (9, 'Down')], [(9, 'Across'), (10, 'Down')], [(9, 'Across'), (11, 'Down')], [(9, 'Across'), (12, 'Down')]], [[(1, 'Down'), (13, 'Across')], [(2, 'Down'), (13, 'Across')], [(3, 'Down'), (13, 'Across')], [(4, 'Down'), (13, 'Across')], '#', [(14, 'Across'), (14, 'Down')], [(5, 'Down'), (14, 'Across')], [(6, 'Down'), (14, 'Across')], [(7, 'Down'), (14, 'Across')], [(8, 'Down'), (14, 'Across')], '#', [(9, 'Down'), (15, 'Across')], [(10, 'Down'), (15, 'Across')], [(11, 'Down'), (15, 'Across')], [(12, 'Down'), (15, 'Across')]], [[(1, 'Down'), (16, 'Across')], [(2, 'Down'), (16, 'Across')], [(3, 'Down'), (16, 'Across')], [(4, 'Down'), (16, 'Across')], '#', [(14, 'Down'), (17, 'Across')], [(5, 'Down'), (17, 'Across')], [(6, 'Down'), (17, 'Across')], [(7, 'Down'), (17, 'Across')], [(8, 'Down'), (17, 'Across')], '#', [(9, 'Down'), (18, 'Across')], [(10, 'Down'), (18, 'Across')], [(11, 'Down'), (18, 'Across')], [(12, 'Down'), (18, 'Across')]], [[(1, 'Down'), (19, 'Across')], [(2, 'Down'), (19, 'Across')], [(3, 'Down'), (19, 'Across')], [(4, 'Down'), (19, 'Across')], [(19, 'Across'), (20, 'Down')], [(14, 'Down'), (19, 'Across')], [(5, 'Down'), (19, 'Across')], '#', [(7, 'Down'), (21, 'Across')], [(8, 'Down'), (21, 'Across')], [(21, 'Across'), (22, 'Down')], [(9, 'Down'), (21, 'Across')], [(10, 'Down'), (21, 'Across')], [(11, 'Down'), (21, 'Across')], [(12, 'Down'), (21, 'Across')]], ['#', '#', '#', [(4, 'Down'), (23, 'Across')], [(20, 'Down'), (23, 'Across')], [(14, 'Down'), (23, 'Across')], [(5, 'Down'), (23, 'Across')], [(23, 'Across'), (24, 'Down')], '#', [(8, 'Down'), (25, 'Across')], [(22, 'Down'), (25, 'Across')], [(9, 'Down'), (25, 'Across')], [(10, 'Down'), (25, 'Across')], [(11, 'Down'), (25, 'Across')], [(12, 'Down'), (25, 'Across')]], [[(26, 'Across'), (26, 'Down')], [(26, 'Across'), (27, 'Down')], [(26, 'Across'), (28, 'Down')], [(4, 'Down'), (26, 'Across')], [(20, 'Down'), (26, 'Across')], [(14, 'Down'), (26, 'Across')], '#', [(24, 'Down'), (29, 'Across')], [(29, 'Across'), (30, 'Down')], [(8, 'Down'), (29, 'Across')], [(22, 'Down'), (29, 'Across')], '#', [(10, 'Down'), (31, 'Across')], [(11, 'Down'), (31, 'Across')], [(12, 'Down'), (31, 'Across')]], [[(26, 'Down'), (32, 'Across')], [(27, 'Down'), (32, 'Across')], [(28, 'Down'), (32, 'Across')], [(4, 'Down'), (32, 'Across')], [(20, 'Down'), (32, 'Across')], '#', [(33, 'Across'), (33, 'Down')], [(24, 'Down'), (33, 'Across')], [(30, 'Down'), (33, 'Across')], [(8, 'Down'), (33, 'Across')], [(22, 'Down'), (33, 'Across')], [(33, 'Across'), (34, 'Down')], '#', '#', '#'], [[(26, 'Down'), (35, 'Across')], [(27, 'Down'), (35, 'Across')], [(28, 'Down'), (35, 'Across')], [(4, 'Down'), (35, 'Across')], '#', [(36, 'Across'), (36, 'Down')], [(33, 'Down'), (36, 'Across')], [(24, 'Down'), (36, 'Across')], [(30, 'Down'), (36, 'Across')], [(8, 'Down'), (36, 'Across')], '#', [(34, 'Down'), (37, 'Across')], [(37, 'Across'), (38, 'Down')], [(37, 'Across'), (39, 'Down')], [(37, 'Across'), (40, 'Down')]], ['#', '#', '#', [(4, 'Down'), (41, 'Across')], [(41, 'Across'), (42, 'Down')], [(36, 'Down'), (41, 'Across')], [(33, 'Down'), (41, 'Across')], [(24, 'Down'), (41, 'Across')], [(30, 'Down'), (41, 'Across')], '#', [(43, 'Across'), (43, 'Down')], [(34, 'Down'), (43, 'Across')], [(38, 'Down'), (43, 'Across')], [(39, 'Down'), (43, 'Across')], [(40, 'Down'), (43, 'Across')]], [[(44, 'Across'), (44, 'Down')], [(44, 'Across'), (45, 'Down')], [(44, 'Across'), (46, 'Down')], '#', [(42, 'Down'), (47, 'Across')], [(36, 'Down'), (47, 'Across')], [(33, 'Down'), (47, 'Across')], [(24, 'Down'), (47, 'Across')], '#', [(48, 'Across'), (48, 'Down')], [(43, 'Down'), (48, 'Across')], [(34, 'Down'), (48, 'Across')], [(38, 'Down'), (48, 'Across')], [(39, 'Down'), (48, 'Across')], [(40, 'Down'), (48, 'Across')]], [[(44, 'Down'), (49, 'Across')], [(45, 'Down'), (49, 'Across')], [(46, 'Down'), (49, 'Across')], [(49, 'Across'), (50, 'Down')], [(42, 'Down'), (49, 'Across')], [(36, 'Down'), (49, 'Across')], '#', [(24, 'Down'), (51, 'Across')], [(51, 'Across'), (52, 'Down')], [(48, 'Down'), (51, 'Across')], [(43, 'Down'), (51, 'Across')], [(34, 'Down'), (51, 'Across')], '#', '#', '#'], [[(44, 'Down'), (53, 'Across')], [(45, 'Down'), (53, 'Across')], [(46, 'Down'), (53, 'Across')], [(50, 'Down'), (53, 'Across')], [(42, 'Down'), (53, 'Across')], [(36, 'Down'), (53, 'Across')], [(53, 'Across'), (54, 'Down')], '#', [(52, 'Down'), (55, 'Across')], [(48, 'Down'), (55, 'Across')], [(43, 'Down'), (55, 'Across')], [(34, 'Down'), (55, 'Across')], [(55, 'Across'), (56, 'Down')], [(55, 'Across'), (57, 'Down')], [(55, 'Across'), (58, 'Down')]], [[(44, 'Down'), (59, 'Across')], [(45, 'Down'), (59, 'Across')], [(46, 'Down'), (59, 'Across')], [(50, 'Down'), (59, 'Across')], '#', [(36, 'Down'), (60, 'Across')], [(54, 'Down'), (60, 'Across')], [(60, 'Across'), (61, 'Down')], [(52, 'Down'), (60, 'Across')], [(48, 'Down'), (60, 'Across')], '#', [(34, 'Down'), (62, 'Across')], [(56, 'Down'), (62, 'Across')], [(57, 'Down'), (62, 'Across')], [(58, 'Down'), (62, 'Across')]], [[(44, 'Down'), (63, 'Across')], [(45, 'Down'), (63, 'Across')], [(46, 'Down'), (63, 'Across')], [(50, 'Down'), (63, 'Across')], '#', [(36, 'Down'), (64, 'Across')], [(54, 'Down'), (64, 'Across')], [(61, 'Down'), (64, 'Across')], [(52, 'Down'), (64, 'Across')], [(48, 'Down'), (64, 'Across')], '#', [(34, 'Down'), (65, 'Across')], [(56, 'Down'), (65, 'Across')], [(57, 'Down'), (65, 'Across')], [(58, 'Down'), (65, 'Across')]], [[(44, 'Down'), (66, 'Across')], [(45, 'Down'), (66, 'Across')], [(46, 'Down'), (66, 'Across')], [(50, 'Down'), (66, 'Across')], '#', [(36, 'Down'), (67, 'Across')], [(54, 'Down'), (67, 'Across')], [(61, 'Down'), (67, 'Across')], [(52, 'Down'), (67, 'Across')], '#', '#', [(34, 'Down'), (68, 'Across')], [(56, 'Down'), (68, 'Across')], [(57, 'Down'), (68, 'Across')], [(58, 'Down'), (68, 'Across')]]]
	
# 	assert(removeLetters(example1) == example1LettersRemoved)
# 	assert(wordIdentifiers(example1) == example1WordIdentifiers)
# 	assert(startIdentifiers(example1) == example1StartIdentifiers)

# 	assert(removeLetters(fullNYT) == fullNYTLettersRemoved)
# 	assert(wordIdentifiers(fullNYT) == fullNYTWordIdentifiers)
# 	assert(startIdentifiers(fullNYT) == fullNYTStartIdentifiers)
	
# 	wordClassList = gridToWordClassList(example1)
# 	solutions = solve(wordClassList)
# 	print("Yay : )")

# 	print("Success: All tests passed")













































