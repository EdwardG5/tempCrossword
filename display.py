from tkinter import *
import math, string
from wordClass import *
from crosswordSolver import solve

#---------------------------------------------------------------------------#

# 1 = suppressErrors, 0 = don't suppress errors

suppressErrors = 0 
# This code supresses error messages. Added by Edward 
# while developing the solver. Should delete immediately. 

import sys

class DevNull:
    def write(self, msg):
        pass

if suppressErrors:
    sys.stderr = DevNull()

#---------------------------------------------------------------------------#



root = Tk()
root.title = "Crosswords"

canvas = Canvas(root, width=1200, height=800, bg = "white")
canvas.grid(column = 2, row = 0, rowspan=40)

canvasHeight = 700
canvasWidth = 1020
sideBarWidth = 130
    
def isStart(board, x, y):
    result = [0,0]
    if board.fills[y][x] == 1: return result
    if (x-1 not in range(board.width) or board.fills[y][x-1] == 1):
        if (x+1 in range(board.width) and board.fills[y][x+1] == 0): result[0] = 1
    if (y-1 not in range(board.height) or board.fills[y-1][x] == 1):
        if (y+1 in range(board.height) and board.fills[y+1][x] == 0): result[1] = 1
    return result

def convertBoardToWords(board):
    words = []
    for row in range(board.height):
        for col in range(board.width):
            start = isStart(board,col,row)
            if start[0] == 1:
                tempCol = col
                if (tempCol in range(board.width) and board.fills[row][tempCol] == 0):
                    newWord = [col,row,0,""]
                while (tempCol in range(board.width) and board.fills[row][tempCol] == 0):
                    newWord[3] += board.letters[row][tempCol].lower()
                    tempCol += 1
                words.append(newWord)
            if start[1] == 1:
                tempRow = row
                newWord = [col,row,1,""]
                while (tempRow in range(board.height) and board.fills[tempRow][col] == 0):
                    newWord[3] += board.letters[tempRow][col].lower()
                    tempRow += 1
                words.append(newWord)
    return words
                


    #Returns a list of words from the user input

def wordsIntersect(word1, word2):
    if word1[2] == word2[2]: return False
    right = (word1 if word1[2]==0 else word2)
    down = (word1 if word1[2]==1 else word2)
    return (right[1] in range(down[1],down[1]+len(down[3]))) and (down[0] in range(right[0],right[0]+len(right[3])))

def convertWordsToClass(words, locations):
    index = 0
    classes = []
    for i in words:
        setChars = len(i[3])-i[3].count("-")
        locations[index] = [i[0],i[1],i[2]]
        classes.append(Word(len(i[3]),0,setChars,index))
        classes[index].setChars([""]+["" if c == "-" else c for c in i[3]])
        for j in words:
            if (i != j) and wordsIntersect(i,j): 
                classes[index].setConstrained(classes[index]._constrained + 1)
        index+=1
    for i in range(len(words)):
        for j in range(len(words)):
            if words[i] != words[j] and wordsIntersect(words[i],words[j]):
                if words[i][2]==0:
                    classes[i].setPointer(words[j][0]-words[i][0]+1,classes[j])
                    classes[i].setIndices(words[j][0]-words[i][0]+1,words[i][1])
                else:
                    classes[i].setPointer(words[j][1]-words[i][1]+1,classes[j])
                    classes[i].setIndices(words[j][1]-words[i][1]+1,words[i][0])
    return classes,locations
    
class wordBoard():
    def __init__(self,width,height,root,canvas,margins = 50):
        self.root = root
        self.canvas = canvas
        self.width = width
        self.height = height
        self.selected = None
        self.fills = [[0]*width for i in range(height)] #The fill of each square
        self.fillIds = [[None]*width for i in range(height)] #The ids of the text
        self.fillIds2 = [[None]*width for i in range(height)] #The ids of the numbers
        self.letters = [["-"]*width for i in range(height)] #The grid of letters
        self.elements = [[None]*width for i in range(height)] #The ids of every square
        self.ids = [] #Every object in the canvas in no particular order
        self.canvas.focus_set()
        self.canvas.bind("<Button-1>", self.canvasOnclick)
        self.canvas.bind("<Double-Button-1>", self.canvasOn2click)
        self.canvas.bind("<Key>", self.canvasOnKeyPress)
        self.canvas.bind("<BackSpace>", self.canvasOnDelete)
        self.margins = margins
        self.locations = {}
        self.xMargins = 0
        self.yMargins = 0
        self.cellDims = 100
        self.submitButton = Button(self.root, text = "Solve", width = 10,
                                bg = "grey", command = self.activateSolve)
        self.submitButton.grid(column=0,row = 25, columnspan = 2)

    def drawBoard(self):
        baseCellWidth = min(100,(canvasWidth-2*self.margins)//self.width)
        baseCellHeight = min(100,(canvasHeight-2*self.margins)//self.height)
        self.cellDims = min(baseCellWidth,baseCellHeight)
        self.xMargins = (canvasWidth-self.cellDims*self.width)//2
        self.yMargins = (canvasHeight-self.cellDims*self.height)//2
        print(self.width,self.height,baseCellWidth,baseCellHeight,self.cellDims)
        for row in range(self.height):
            for col in range(self.width):
                item = canvas.create_rectangle(self.xMargins+col*self.cellDims, 
                                               self.yMargins+row*self.cellDims,
                                               self.xMargins+(col+1)*self.cellDims, 
                                               self.yMargins+(row+1)*self.cellDims,
                                               width = max(1,min(3,self.cellDims//20)))
                self.ids.append(item)
                self.elements[row][col] = item


    def canvasOnclick(self,event):
        if ((event.x in range(self.xMargins,self.cellDims*self.width+self.xMargins)) and 
            (event.y in range(self.yMargins,self.cellDims*self.height+self.yMargins))):
            row = (event.y-self.yMargins)//self.cellDims
            col = (event.x-self.xMargins)//self.cellDims
            if self.selected == self.elements[row][col]:
                self.canvas.itemconfig(self.selected, outline = "black")
                self.selected == None
            else:
                self.canvas.itemconfig(self.selected, outline = "black")
                self.selected = self.elements[row][col]
                self.canvas.itemconfig(self.selected, outline = "red")

    def canvasOn2click(self,event):
        if ((event.x in range(self.xMargins,self.cellDims*self.width+self.xMargins)) and 
            (event.y in range(self.yMargins,self.cellDims*self.height+self.yMargins))):
            row = (event.y-self.yMargins)//self.cellDims
            col = (event.x-self.xMargins)//self.cellDims
            self.canvas.itemconfig(self.elements[row][col],
                                   fill = ("white" if self.canvas.itemcget(self.elements[row][col], "fill") == "black" else "black"))
            self.fills[row][col] = 1-self.fills[row][col]
    
    #Finds the row and column of a square given an id
    def findCoords(self, ID):
        for row in range(len(self.elements)):
            if ID in self.elements[row]:
                return row,self.elements[row].index(ID)

    #Adds a letter to a particular square
    def addLetter(self,char,row,col):
        if self.fillIds[row][col] != None:
            self.canvas.delete(self.fillIds[row][col])
        textSize = int(self.cellDims//1.2)
        self.fillIds[row][col] = canvas.create_text((col+0.5)*self.cellDims+self.xMargins,
                                                    (row+0.5)*self.cellDims+self.yMargins,
                                                    text = char,
                                                    font = f"Times {textSize}")
        self.ids.append(self.fillIds[row][col])
        self.letters[row][col] = char

    #Puts in letters
    def canvasOnKeyPress(self,event):
        if self.selected != None and ((event.char in string.ascii_lowercase) or (event.char in string.ascii_uppercase)):
            char = event.char
            row,col = self.findCoords(self.selected)
            self.addLetter(char,row,col)
            
    #Deletes Letters
    def canvasOnDelete(self,event):
        print("delete")
        if self.selected != None:
            row,col = self.findCoords(self.selected)
            self.canvas.delete(self.fillIds[row][col])
            self.fillIds[row][col] = None
            self.letters[row][col] = "-"

    #Resets the entire canvas, used when changing sizes
    def destroy(self):
        for item in self.ids:
            self.canvas.delete(item)

    #Creates the list of classes used by Edward
    def activateSolve(self):
        words = convertBoardToWords(self)
        #for i in words:
        #    print(i)
        print(words)
        #listOfWords,self.locations = convertWordsToClass(words, self.locations)
        listOfWords,self.locations = convertWordsToClass(words, self.locations)
        ##### I think this is the problem line
        # Yep
        solution = solve(listOfWords)[0]
        print(solution)
        for x in range(len(solution)):
            solution[x] = (solution[x], x)
        for word in listOfWords:
            print(word)
        #send list to Edward
        self.fillWithSolution(solution)

    def fillWithSolution(self,solution):
        nums = [0]
        for word in solution:
            x,y,direction = self.locations[word[1]]
            textSize = self.cellDims//4
            if self.fillIds2[y][x] == None:
                self.fillIds2[y][x] = canvas.create_text((x+0.2)*self.cellDims+self.xMargins,
                                                    (y+0.2)*self.cellDims+self.yMargins,
                                                    text = str(max(nums)+1),
                                                    font = f"Times {textSize}",
                                                    fill = "grey")
                nums.append(max(nums)+1)
            self.ids.append(self.fillIds2[y][x])
            for c in range(len(word[0])):
                self.addLetter(word[0][c],y+c*direction,x+c*(1-direction))

class Space():
    def __init__(self, root, canvas):
        self.root = root
        self.canvas = canvas
        self.currentBoard = None

        self.widthLabel = Label(self.root, text = "Width: ")
        self.widthLabel.grid(column = 0, row = 10)
        self.widthField = Entry(self.root, text = "")
        self.widthField.grid(column=1, row = 10)

        self.heightLabel = Label(self.root, text = "Height: ")
        self.heightLabel.grid(column = 0, row = 11)
        self.heightField = Entry(self.root, text = "")
        self.heightField.grid(column=1, row = 11)

        self.submitButton = Button(self.root, text = "Submit", width = 10,
                                bg = "grey", command = self.createCrossword)
        self.submitButton.grid(column=0,row = 12, columnspan = 2)

        board = wordBoard(5,5,self.root,canvas)
        board.drawBoard()
        self.currentBoard = board

    def submitCWDims(self):
        height = self.heightField.get()
        width = self.widthField.get()
        try: height = int(height)
        except: pass
        try: width = int(width)
        except: pass
        self.heightField.delete(0, 'end')
        self.widthField.delete(0, 'end') 
        return width,height

    def createCrossword(self):
        width,height = self.submitCWDims()
        print(self.currentBoard)
        if self.currentBoard != None:
            self.currentBoard.destroy()
        board = wordBoard(width,height,self.root,canvas)
        board.drawBoard()
        self.currentBoard = board

    def run(self):
        self.root.after(20, self.run)

space = Space(root,canvas)
space.run()
root.mainloop()