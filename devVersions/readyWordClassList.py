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

# Turn a wcList into a list of WordIds (w1, w2, w3, ...) -> ((1, "Above"), (2, "Down"), ...)
def extractIds(wcList):
	ids = []
	for word in wcList:
		ids.append(word._id)
	return ids