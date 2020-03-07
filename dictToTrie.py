from nodeClass import *
from index import index

#Converts a trie into a list of words
def trieToList(root, string = ""):
    if root._word: strings = [string+root._letter]
    else: strings = []
    for node in root._pointers:
        if node != None:
            result = trieToList(node,string = string+root._letter)
            strings += result
    return strings

#Creates a new trie with every word in a given dictionary, returns root
def listToTrie(dictionary):
    root = Node(None,"",0,False)
    for word in dictionary:
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

#Determines whether a word is in the trie, returns boolean
def wordInTrie(word,node):
    for char in word:
        if node._pointers[index(char)] != None:
            node = node._pointers[index(char)]
        else:
            return False
    return node._word

# Counts the number of nodes in the trie (each representing one letter) + 1 (for the root)
# Sean's originally did not include the root node (cause of discrepancy)
def nodesInTrie(root):
    if root == None:
        return 0
    else:
        count = 1
        for x in root._pointers:
            count += nodesInTrie(x)
        return count

#Returns a list of the number of words of each length
def findLens(dictionary):
    lengths = [0]*max(list(map(len,dictionary)))
    for word in dictionary: lengths[len(word)-1] += 1
    return lengths

def testing():
    dictionary = ["ab","b","acd"]
    root = listToTrie(dictionary)
    print(root)
    print(root._pointers[0]._pointers[1]._depth, root._pointers[0]._pointers[1]._height, root._pointers[0]._pointers[1]._maxLength)


#testing()