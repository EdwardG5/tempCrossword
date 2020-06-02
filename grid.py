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
	return len(newGrid[row][col]) == 0 or (len(newGrid[row][col]) == 1 and newGrid[row][col][0][1] != "Across")
# Square not part of down
def nPOD(grid, row, col):
	return len(newGrid[row][col]) == 0 or (len(newGrid[row][col]) == 1 and newGrid[row][col][0][1] != "Down")
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
# Populate across
def pA(grid, row, col, index):
	try:
		while notBlocked(grid[row][col]):
			grid[row][col].append((index, "Across"))
			col += 1
	except:
		pass
# Populate down
def pD(grid, row, col, index):
	try:
		while notBlocked(grid[row][col]):
			grid[row][col].append((index, "Down"))
			row += 1
	except:
		pass

# -----------------------------------------------------------------

# Rules: 
# a square is the start of a word if not blocked AND: 
# 		   	At the top or leftmost edge of grid
# 		OR 	Up/Left square is blocked
# AND across/down is not blocked (len >= 2)

# The below functions require that grid is at least 2 across and down. 

# Populate grid with word identifies (number, "Down"/"Across")
# char list list -> (char OR (index, "Up"/"Down") list)
# In the latter case, the list can be of length 1 or 2 (part of one or two words)
def wordIdentifiers(grid):
	index = 1
	newGrid = removeLetters(grid, replace=[])
	height, width = len(newGrid), len(newGrid[0])
	for row in range(height):
		for col in range(width):
			if notBlocked(newGrid[row][col]):
				startOfAcross = False
				startOfDown = False
				# Across
				if (col == 0 or lB(newGrid, row, col)) and nA(newGrid, row, col):
					startOfAcross = True
					pA(newGrid, row, col, index)
				# Down
				if (row == 0 or uB(newGrid, row, col)) and nD(newGrid, row, col):
					startOfDown = True
					pD(newGrid, row, col, index)
				if startOfAcross or startOfDown:
					index += 1
	return newGrid

# Identify the squares starting words
# char list list -> (char OR int) list list
def startIdentifiers(grid):
	index = 1
	newGrid = removeLetters(grid)
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
					newGrid[row][col] = index
					index += 1
	return newGrid

# Convert a grid into a list of fully linked word class objects
def gridToWordClassList(grid):
	pass

# Convert a list of word class objects into a char grid
def wordClassListToGrid(wL):
	pass







if __name__ == "__main__":
	
	example1 = [['a', 'a', 'd', '#'], ['#', 's', '#', 'a'], ['#', '#', 'k', ' ']]
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
	example1LettersRemoved = [[' ', ' ', ' ', '#'], ['#', ' ', '#', ' '], ['#', '#', ' ', ' ']]
	example1StartIdentifiers = [[1, 2, ' ', '#'], ['#', ' ', '#', 3], ['#', '#', 4, ' ']] 
	example1WordIdentifiers = [[[(1, 'Across')], [(1, 'Across'), (2, 'Down')], [(1, 'Across')], '#'], ['#', [(2, 'Down')], '#', [(3, 'Down')]], ['#', '#', [(4, 'Across')], [(3, 'Down'), (4, 'Across')]]]
	fullNYTLettersRemoved = [[' ', ' ', ' ', ' ', '#', '#', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' '], ['#', '#', '#', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', '#', '#', '#'], [' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' '], ['#', '#', '#', ' ', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', '#', '#', '#'], [' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', '#', '#', ' ', ' ', ' ', ' ']]
	fullNYTStartIdentifiers = [[1, 2, 3, 4, '#', '#', 5, 6, 7, 8, '#', 9, 10, 11, 12], [13, ' ', ' ', ' ', '#', 14, ' ', ' ', ' ', ' ', '#', 15, ' ', ' ', ' '], [16, ' ', ' ', ' ', '#', 17, ' ', ' ', ' ', ' ', '#', 18, ' ', ' ', ' '], [19, ' ', ' ', ' ', 20, ' ', ' ', '#', 21, ' ', 22, ' ', ' ', ' ', ' '], ['#', '#', '#', 23, ' ', ' ', ' ', 24, '#', 25, ' ', ' ', ' ', ' ', ' '], [26, 27, 28, ' ', ' ', ' ', '#', 29, 30, ' ', ' ', '#', 31, ' ', ' '], [32, ' ', ' ', ' ', ' ', '#', 33, ' ', ' ', ' ', ' ', 34, '#', '#', '#'], [35, ' ', ' ', ' ', '#', 36, ' ', ' ', ' ', ' ', '#', 37, 38, 39, 40], ['#', '#', '#', 41, 42, ' ', ' ', ' ', ' ', '#', 43, ' ', ' ', ' ', ' '], [44, 45, 46, '#', 47, ' ', ' ', ' ', '#', 48, ' ', ' ', ' ', ' ', ' '], [49, ' ', ' ', 50, ' ', ' ', '#', 51, 52, ' ', ' ', ' ', '#', '#', '#'], [53, ' ', ' ', ' ', ' ', ' ', 54, '#', 55, ' ', ' ', ' ', 56, 57, 58], [59, ' ', ' ', ' ', '#', 60, ' ', 61, ' ', ' ', '#', 62, ' ', ' ', ' '], [63, ' ', ' ', ' ', '#', 64, ' ', ' ', ' ', ' ', '#', 65, ' ', ' ', ' '], [66, ' ', ' ', ' ', '#', 67, ' ', ' ', ' ', '#', '#', 68, ' ', ' ', ' ']]
	fullNYTWordIdentifiers = [[[(1, 'Across'), (1, 'Down')], [(1, 'Across'), (2, 'Down')], [(1, 'Across'), (3, 'Down')], [(1, 'Across'), (4, 'Down')], '#', '#', [(5, 'Across'), (5, 'Down')], [(5, 'Across'), (6, 'Down')], [(5, 'Across'), (7, 'Down')], [(5, 'Across'), (8, 'Down')], '#', [(9, 'Across'), (9, 'Down')], [(9, 'Across'), (10, 'Down')], [(9, 'Across'), (11, 'Down')], [(9, 'Across'), (12, 'Down')]], [[(1, 'Down'), (13, 'Across')], [(2, 'Down'), (13, 'Across')], [(3, 'Down'), (13, 'Across')], [(4, 'Down'), (13, 'Across')], '#', [(14, 'Across'), (14, 'Down')], [(5, 'Down'), (14, 'Across')], [(6, 'Down'), (14, 'Across')], [(7, 'Down'), (14, 'Across')], [(8, 'Down'), (14, 'Across')], '#', [(9, 'Down'), (15, 'Across')], [(10, 'Down'), (15, 'Across')], [(11, 'Down'), (15, 'Across')], [(12, 'Down'), (15, 'Across')]], [[(1, 'Down'), (16, 'Across')], [(2, 'Down'), (16, 'Across')], [(3, 'Down'), (16, 'Across')], [(4, 'Down'), (16, 'Across')], '#', [(14, 'Down'), (17, 'Across')], [(5, 'Down'), (17, 'Across')], [(6, 'Down'), (17, 'Across')], [(7, 'Down'), (17, 'Across')], [(8, 'Down'), (17, 'Across')], '#', [(9, 'Down'), (18, 'Across')], [(10, 'Down'), (18, 'Across')], [(11, 'Down'), (18, 'Across')], [(12, 'Down'), (18, 'Across')]], [[(1, 'Down'), (19, 'Across')], [(2, 'Down'), (19, 'Across')], [(3, 'Down'), (19, 'Across')], [(4, 'Down'), (19, 'Across')], [(19, 'Across'), (20, 'Down')], [(14, 'Down'), (19, 'Across')], [(5, 'Down'), (19, 'Across')], '#', [(7, 'Down'), (21, 'Across')], [(8, 'Down'), (21, 'Across')], [(21, 'Across'), (22, 'Down')], [(9, 'Down'), (21, 'Across')], [(10, 'Down'), (21, 'Across')], [(11, 'Down'), (21, 'Across')], [(12, 'Down'), (21, 'Across')]], ['#', '#', '#', [(4, 'Down'), (23, 'Across')], [(20, 'Down'), (23, 'Across')], [(14, 'Down'), (23, 'Across')], [(5, 'Down'), (23, 'Across')], [(23, 'Across'), (24, 'Down')], '#', [(8, 'Down'), (25, 'Across')], [(22, 'Down'), (25, 'Across')], [(9, 'Down'), (25, 'Across')], [(10, 'Down'), (25, 'Across')], [(11, 'Down'), (25, 'Across')], [(12, 'Down'), (25, 'Across')]], [[(26, 'Across'), (26, 'Down')], [(26, 'Across'), (27, 'Down')], [(26, 'Across'), (28, 'Down')], [(4, 'Down'), (26, 'Across')], [(20, 'Down'), (26, 'Across')], [(14, 'Down'), (26, 'Across')], '#', [(24, 'Down'), (29, 'Across')], [(29, 'Across'), (30, 'Down')], [(8, 'Down'), (29, 'Across')], [(22, 'Down'), (29, 'Across')], '#', [(10, 'Down'), (31, 'Across')], [(11, 'Down'), (31, 'Across')], [(12, 'Down'), (31, 'Across')]], [[(26, 'Down'), (32, 'Across')], [(27, 'Down'), (32, 'Across')], [(28, 'Down'), (32, 'Across')], [(4, 'Down'), (32, 'Across')], [(20, 'Down'), (32, 'Across')], '#', [(33, 'Across'), (33, 'Down')], [(24, 'Down'), (33, 'Across')], [(30, 'Down'), (33, 'Across')], [(8, 'Down'), (33, 'Across')], [(22, 'Down'), (33, 'Across')], [(33, 'Across'), (34, 'Down')], '#', '#', '#'], [[(26, 'Down'), (35, 'Across')], [(27, 'Down'), (35, 'Across')], [(28, 'Down'), (35, 'Across')], [(4, 'Down'), (35, 'Across')], '#', [(36, 'Across'), (36, 'Down')], [(33, 'Down'), (36, 'Across')], [(24, 'Down'), (36, 'Across')], [(30, 'Down'), (36, 'Across')], [(8, 'Down'), (36, 'Across')], '#', [(34, 'Down'), (37, 'Across')], [(37, 'Across'), (38, 'Down')], [(37, 'Across'), (39, 'Down')], [(37, 'Across'), (40, 'Down')]], ['#', '#', '#', [(4, 'Down'), (41, 'Across')], [(41, 'Across'), (42, 'Down')], [(36, 'Down'), (41, 'Across')], [(33, 'Down'), (41, 'Across')], [(24, 'Down'), (41, 'Across')], [(30, 'Down'), (41, 'Across')], '#', [(43, 'Across'), (43, 'Down')], [(34, 'Down'), (43, 'Across')], [(38, 'Down'), (43, 'Across')], [(39, 'Down'), (43, 'Across')], [(40, 'Down'), (43, 'Across')]], [[(44, 'Across'), (44, 'Down')], [(44, 'Across'), (45, 'Down')], [(44, 'Across'), (46, 'Down')], '#', [(42, 'Down'), (47, 'Across')], [(36, 'Down'), (47, 'Across')], [(33, 'Down'), (47, 'Across')], [(24, 'Down'), (47, 'Across')], '#', [(48, 'Across'), (48, 'Down')], [(43, 'Down'), (48, 'Across')], [(34, 'Down'), (48, 'Across')], [(38, 'Down'), (48, 'Across')], [(39, 'Down'), (48, 'Across')], [(40, 'Down'), (48, 'Across')]], [[(44, 'Down'), (49, 'Across')], [(45, 'Down'), (49, 'Across')], [(46, 'Down'), (49, 'Across')], [(49, 'Across'), (50, 'Down')], [(42, 'Down'), (49, 'Across')], [(36, 'Down'), (49, 'Across')], '#', [(24, 'Down'), (51, 'Across')], [(51, 'Across'), (52, 'Down')], [(48, 'Down'), (51, 'Across')], [(43, 'Down'), (51, 'Across')], [(34, 'Down'), (51, 'Across')], '#', '#', '#'], [[(44, 'Down'), (53, 'Across')], [(45, 'Down'), (53, 'Across')], [(46, 'Down'), (53, 'Across')], [(50, 'Down'), (53, 'Across')], [(42, 'Down'), (53, 'Across')], [(36, 'Down'), (53, 'Across')], [(53, 'Across'), (54, 'Down')], '#', [(52, 'Down'), (55, 'Across')], [(48, 'Down'), (55, 'Across')], [(43, 'Down'), (55, 'Across')], [(34, 'Down'), (55, 'Across')], [(55, 'Across'), (56, 'Down')], [(55, 'Across'), (57, 'Down')], [(55, 'Across'), (58, 'Down')]], [[(44, 'Down'), (59, 'Across')], [(45, 'Down'), (59, 'Across')], [(46, 'Down'), (59, 'Across')], [(50, 'Down'), (59, 'Across')], '#', [(36, 'Down'), (60, 'Across')], [(54, 'Down'), (60, 'Across')], [(60, 'Across'), (61, 'Down')], [(52, 'Down'), (60, 'Across')], [(48, 'Down'), (60, 'Across')], '#', [(34, 'Down'), (62, 'Across')], [(56, 'Down'), (62, 'Across')], [(57, 'Down'), (62, 'Across')], [(58, 'Down'), (62, 'Across')]], [[(44, 'Down'), (63, 'Across')], [(45, 'Down'), (63, 'Across')], [(46, 'Down'), (63, 'Across')], [(50, 'Down'), (63, 'Across')], '#', [(36, 'Down'), (64, 'Across')], [(54, 'Down'), (64, 'Across')], [(61, 'Down'), (64, 'Across')], [(52, 'Down'), (64, 'Across')], [(48, 'Down'), (64, 'Across')], '#', [(34, 'Down'), (65, 'Across')], [(56, 'Down'), (65, 'Across')], [(57, 'Down'), (65, 'Across')], [(58, 'Down'), (65, 'Across')]], [[(44, 'Down'), (66, 'Across')], [(45, 'Down'), (66, 'Across')], [(46, 'Down'), (66, 'Across')], [(50, 'Down'), (66, 'Across')], '#', [(36, 'Down'), (67, 'Across')], [(54, 'Down'), (67, 'Across')], [(61, 'Down'), (67, 'Across')], [(52, 'Down'), (67, 'Across')], '#', '#', [(34, 'Down'), (68, 'Across')], [(56, 'Down'), (68, 'Across')], [(57, 'Down'), (68, 'Across')], [(58, 'Down'), (68, 'Across')]]]
	
	assert(removeLetters(example1) == example1LettersRemoved)
	assert(wordIdentifiers(example1) == example1WordIdentifiers)
	assert(startIdentifiers(example1) == example1StartIdentifiers)

	assert(removeLetters(fullNYT) == fullNYTLettersRemoved)
	assert(wordIdentifiers(fullNYT) == fullNYTWordIdentifiers)
	assert(startIdentifiers(fullNYT) == fullNYTStartIdentifiers)
	
	print("Success: All tests passed")













































