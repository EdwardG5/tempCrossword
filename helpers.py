"""
Helpers: 

Random functions that don't really fit in anywhere else. 
"""

# Not used
# Returns a list of the number of words of each length
# str list -> (int : int) dict
def findLens(wordList):
    lengths = {n: 0 for n in range(1+max(list(map(len, wordList))))}
    for word in wordList: 
        lengths[len(word)] += 1
    return lengths


# Accepts a fileName/filePath and returns a list of the (valid) strings in that file
# ENSURES: the returned list is clean, well formatted, all lowercase, no duplicates
# str -> str list
def fileToWordList(fileRoute):
	fp = open(fileRoute)
	words = fp.read().split()
	fp.close()
	words = filter(lambda x: isinstance(x, str) and x.isalpha(), words)
	words = map(lambda x: x.lower(), words)
	words = list(set(words))
	return words
