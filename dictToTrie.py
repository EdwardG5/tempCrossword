from nodeClass import Node

# (Helper for listToTrie)
# Insert one word into a trie structure. Modifies in place.
# node structure * str -> None
def insertWordInTrie(root, word):
	char = word[0]
	if root[char] == None:
		root[char] = Node(root, char, False)
	if len(word) == 1:
		root[char]._word = True
	else:
		insertWordInTrie(root[char], word[1:])

# Creates a new trie with every word in a given word list. Returns root of a trie.
# str list -> node structure (trie)
def listToTrie(wordList):
	root = Node(None, "", False)
	for word in wordList:
		insertWordInTrie(root, word)
	return root

# Recursively converts a trie into a list of words. Function accepts a prefix representing current trie position.
# node * str -> str list
def trieToList(root, prefix=""):
    strings = []
    if root._word: 
        strings.append(prefix+root._letter)
    for node in root:
        if node:
            result = trieToList(node, prefix=prefix+root._letter)
            strings += result
    return strings

# Determines whether a word is in the trie.
# str * node -> bool
def wordInTrie(word, node):
    for char in word:
        if node[char] != None:
            node = node[char]
        else:
            return False
    return node._word

# Counts the number of nodes in the trie (each representing one letter) + 1 (for the root)
# node -> int
def nodesInTrie(root):
    if root == None:
        return 0
    else:
        count = 1
        for x in root:
            count += nodesInTrie(x)
        return count

# Returns a list of the number of words of each length
# str list -> (int : int) dict
def findLens(wordList):
    lengths = {n: 0 for n in range(1+max(list(map(len, wordList))))}
    for word in wordList: 
        lengths[len(word)] += 1
    return lengths
