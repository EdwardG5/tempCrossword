from nodeClass import Node

# (Helper for listToTrie)
# Insert one word into a trie structure. Modifies in place.
# node structure * str -> None
def insertWordInTrie(root, word):
	char = word[0]
	if root[char] == None:
		root[char] = Node(root, char, False)
	if len(word) == 1:
		root[char].word = True
	else:
		insertWordInTrie(root[char], word[1:])

# Creates a new trie with every word in a given word list. Returns root of a trie.
# str list -> node structure (trie)
def listToTrie(wordList):
	root = Node(None, "", False)
	for word in wordList:
		insertWordInTrie(root, word)
	return root

# Recursively converts a trie into a list of words.
# node -> str list
def trieToList(root):
    strings = []
    if root.word: 
        strings.append(root.whichWord())
    for node in root:
        if node:
            strings += trieToList(node)
    return strings

# Determines whether a word is in the trie.
# str * node -> bool
def wordInTrie(word, node):
    for char in word:
        if node[char] != None:
            node = node[char]
        else:
            return False
    return node.word

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