from nodeClass import *
from index import index

# Creates a new trie with every word in a given word list. Returns root of a trie. 
# str list -> node structure (trie)
def listToTrie(wordList):
    root = Node(None,"",0,False)
    for word in wordList:
        newNode = root
        depth = 0
        for char in word:
            depth += 1
            if newNode._pointers[index(char)] == None:
                newNode._pointers[index(char)] = Node(newNode,char,depth,False)
                newNode = newNode._pointers[index(char)]
                testNode = newNode._parent
                while testNode != root:
                    testNode._height = testNode._height
                    for node in testNode._pointers:
                        if node != None: 
                            if node._height+1 > testNode._height:
                                testNode._height = node._height+1
                                testNode._maxLength += 1
                    testNode = testNode._parent
            else:
                newNode = newNode._pointers[index(char)]
        newNode._word = True
    return root

# Recursively converts a trie into a list of words. Function accepts a prefix representing current trie position.
# node * str -> str list
def trieToList(root, prefix = ""):
    strings = []
    if root._word: 
        strings += prefix+root._letter
    for node in root._pointers:
        if node != None:
            result = trieToList(node, prefix=prefix+root._letter)
            strings += result
    return strings

# Determines whether a word is in the trie.
# str * node -> bool
def wordInTrie(word, node):
    for char in word:
        if node._pointers[index(char)] != None:
            node = node._pointers[index(char)]
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
        for x in root._pointers:
            count += nodesInTrie(x)
        return count

# Returns a list of the number of words of each length
# str list -> (int : int) dict
def findLens(wordList):
    lengths = {n: 0 for n in range(1+max(list(map(len, wordList))))}
    for word in wordList: 
        lengths[len(word)] += 1
    return lengths

# FIX
def testing():
    # Write some proper test cases. 
    # I don't guarantee correct functioning
    pass

if __name__ == "__main__":
    testing()
