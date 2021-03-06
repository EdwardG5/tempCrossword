"""
I have appended FIX to areas that need attention. 

I have added DEV to areas which are added on a whim to casually implement quickly desired functionality with little regard for precise mechanics/visual appeal.

"""

from tkinter import *
import string
from constants import Constants
from grid import populateWithIth, gridToWordClassList, wordClassListToGrid
from crosswordSolver import solve
from time import sleep

# FIXME
from grid import printGrid

# This is linked to an IntVar in app.mainarea via app. Used for global queries
gridDrawn = False

class SideBar(Frame):

	def __init__(self, master):

		self.master = master
		Frame.__init__(self, master)

		# Make easily visible
		# self['bg'] = 'red'

		# Create attributes
		self.width = StringVar()
		self.widthL = Label(self, text='Width:')
		self.widthE = Entry(self, textvariable=self.width)
		self.height = StringVar()
		self.heightL = Label(self, text='Height:')
		self.heightE = Entry(self, textvariable=self.height)
		self.drawGrid = Button(self, text='Draw Grid', command=self._draw_grid)
		self.solve = Button(self, text='Solve', command=self._solve)
		self.clear = Button(self, text='Clear', command=self._clear)

		# Enable input validation
		self._vcmd = (self.register(self._vcmd), "%P")
		self.widthE.config(validate='key', validatecommand=self._vcmd, invalidcommand=self.bell)
		self.heightE.config(validate='key', validatecommand=self._vcmd, invalidcommand=self.bell)

		# Create key bindings: click via enter
		self.drawGrid.bind("<Return>", self.drawGrid['command'])
		self.solve.bind("<Return>", self.solve['command'])
		self.clear.bind("<Return>", self.clear['command'])

		# Place on screen
		self.widthL.grid(row=1, column=0, sticky='nesw', pady=10, padx=10)
		self.widthE.grid(row=1, column=1, sticky='nesw', pady=10, padx=10)
		self.heightL.grid(row=2, column=0, sticky='nesw', pady=10, padx=10)
		self.heightE.grid(row=2, column=1, sticky='nesw', pady=10, padx=10)
		self.drawGrid.grid(row=3, column=0, columnspan=2, pady=10, padx=10)
		self.solve.grid(row=4, column=0, columnspan=2, pady=10, padx=10)
		self.clear.grid(row=5, column=0, columnspan=2, pady=10, padx=10)
		self.grid_rowconfigure(0, weight=1)
		self.grid_rowconfigure(6, weight=1)

		# Initialize appearances
		self._init_appearance()

	def _vcmd(self, P):
		return len(P) == 0 or P.isnumeric()

	def _init_appearance(self):

		# Global settings 
		widgets = [self.widthL, self.widthE, self.heightL, self.heightE, self.drawGrid, self.solve, self.clear]
		self.master.init_appearance(widgets)

		# Local settings
		self.widthL['anchor'] = 'w'
		self.heightL['anchor'] = 'w'
		self.widthL['width'] = 5
		self.heightL['width'] = 5
		self.widthE['width'] = 10
		self.heightE['width'] = 10

	def _disable_entry_widgets(self):
		self.widthE['state'] = 'disabled'
		self.heightE['state'] = 'disabled'

	def _enable_entry_widgets(self):
		self.widthE['state'] = 'normal'
		self.heightE['state'] = 'normal'

	def _draw_grid(self):
		self.focus_force() # This moves focus to the frame. Fixes bug of focus remaining on disabled entry
		self._disable_entry_widgets()
		self.drawGrid['state'] = 'disabled'
		self.solve['state'] = 'normal'
		self.clear['state'] = 'normal'
		self.master.drawGrid()

	def _solve(self):
		self.focus_force() # This moves focus to the frame. Fixes bug of focus remaining on disabled entry
		self._disable_entry_widgets()
		self.drawGrid['state'] = 'disabled'
		self.solve['state'] = 'disabled'
		self.clear['state'] = 'normal'
		self.master.solve()

	def _clear(self):
		self.focus_force() # This moves focus to the frame. Deselects any selected widget
		self._enable_entry_widgets()
		self.drawGrid['state'] = 'normal'
		self.solve['state'] = 'disabled'
		self.clear['state'] = 'disabled'
		self.width.set('')
		self.height.set('')
		self.master.clear()

	def getWidth(self):
		return int(self.width.get())

	def getHeight(self):
		return int(self.height.get())

class MainArea(Canvas):

	def __init__(self, master):

		self.master = master
		Canvas.__init__(self, master, takefocus=1)

		# Make easily visible 
		#self['bg'] = 'blue'

		self.margins = 50 # margins = user setting describing width of smallest (x or direction) margins around grid

		# Binding virtual event for arrow navigation on grid
		self.event_add("<<arrow>>", "<Left>", "<Right>", "<Up>", "<Down>")

		# Add binding for resize event
		self.bind("<Configure>", lambda event: self._resize())

		# All of the below attributes are completely wiped + reset when drawBoard() is called. 
		# They are written in the current forms below in order to illustrate and explain their use. 

		self.width = 5 # Width of grid
		self.height = 5 # Height of grid

		self.xMargins = None # xMargins + yMargins = the actual margins around the grid (no necessarily equal - each at least 50)
		self.yMargins = None
		self.cellDims = None # Size of a single square in the grid 
		self.bwidth = None # Size of the border on squares (thickness)

		# The following only make sense in the context of a drawn grid
		self.selected = ()	# (row, col, tagId) of selected square in grid 
		# Color of grid squares. 0 = white, 1 = black
		self.squareColors = [[0]*self.width for i in range(self.height)]
		self.squareColorIds = [[None]*self.width for i in range(self.height)] # Canvas ids of squares
		# Letters stored in grid
		self.letters = [[Constants.defaultEmptyChar]*self.width for i in range(self.height)] #The grid of letters
		self.letterIds = [[None]*self.width for i in range(self.height)] # Canvas ids of the letters
		# Letters stored in grid
		self.numbers = [[None]*self.width for i in range(self.height)] #The grid of numbers
		self.numberIds = [[None]*self.width for i in range(self.height)] # Canvas ids of the numbers

		# Not currently used
		# the canvas ids of the word numbers (top right, crossword identifiers)
		# self.fillIds2 = [[None]*self.width for i in range(self.height)] #The ids of the numbers
		# self.locations = {} # This is used for the solving logic and subsequent placement (FIX: should delete - logic should not be in here)

		# Start empty, disabled
		self.gridDrawn = BooleanVar(value=False) # Boolean indicating whether a grid is being displayed
		self.disable()

	# Initializes and sets all keyboard and mouse bindings.
	# Note: All bound functions rely/assume that there is a grid drawn at present
	def _create_bindings(self):
		self.bind("<Button-1>", self._canvas_on_click)
		self.bind("<Double-Button-1>", self._canvas_on_2click)
		self.bind("<<arrow>>", self._canvas_on_arrows)
		self.bind("<space>", lambda event: self._toggle_selected())
		self.bind("<Key>", self._canvas_on_key_press)
		self.bind("<BackSpace>", lambda event: self._empty_selected())
		self.bind("<Escape>", self._esc)

	# Removes all keyboard and mouse bindings.
	def _remove_bindings(self):
		for b in self.bind():
			if b == '<Configure>':
				continue
			self.unbind(b)

	# Allows user to navigate on grid using arrow keys. 
	# If no square selected, defaults to top left
	# If at border + attempt to move off, nothing happens
	def _canvas_on_arrows(self, event):
		cmd = event.keysym
		# No square currently selected. Defaults to top left.
		if not self.selected:
			self.selected = (0, 0, self.squareColorIds[0][0])
			self._add_focus()
		else:
			row = self.selected[0]
			col = self.selected[1]
			# On an edge - attempted move not possible
			if (cmd == "Up" and row == 0) or (cmd == "Down" and row == self.height-1) or \
				(cmd == "Left" and col == 0) or (cmd == "Right" and col == self.width-1):
				pass
			else:
				self._remove_focus()
				nrow = row+(-1 if cmd == "Up" else (1 if cmd == "Down" else 0))
				ncol = col+(-1 if cmd == "Left" else (1 if cmd == "Right" else 0))
				self.selected = (nrow, ncol, self.squareColorIds[nrow][ncol])
				self._add_focus()

	# Removes red border from the selected square
	def _remove_focus(self):
		if self.selected:
			self.itemconfig(self.selected[2], outline='black')
			self.selected = ()

	# Adds a red border to the selected square
	def _add_focus(self):
		if self.selected:
			self.tag_raise(self.selected[2])
			self.itemconfig(self.selected[2], outline='red')
			row, col = self.selected[0], self.selected[1]
			if self.letterIds[row][col]:	
				self.tag_raise(self.letterIds[row][col])
			if self.numberIds[row][col]:
				self.tag_raise(self.numberIds[row][col])

	# Determines whether a click is within the grid, and if so what square was clicked. Returns a relevant tuple
	# Note: pure function
	def _clicked_square(self, event):
		if ((event.x in range(self.xMargins, self.xMargins+self.cellDims*self.width)) and 
			(event.y in range(self.yMargins, self.yMargins+self.cellDims*self.height))):
			row = (event.y-self.yMargins)//self.cellDims
			col = (event.x-self.xMargins)//self.cellDims
			return (row, col, self.squareColorIds[row][col])
		else:
			return ()

	# Toggles fill of square. Also empties letter if it exists. 
	def _toggle_cell(self, row, col):
		self._empty_cell(row, col)
		cellId = self.squareColorIds[row][col]
		self.itemconfig(cellId, fill = 
			("white" if self.itemcget(cellId, "fill") == "black" else "black"))
		self.squareColors[row][col] = not self.squareColors[row][col]

	# Toggles fill of selected square. Also empties letter if it exists. 
	def _toggle_selected(self):
		row, col = self.selected[0], self.selected[1]
		self._toggle_cell(row, col)

	# Determines relevant square (if any) + adds/removes focus
	def _canvas_on_click(self, event):
		self.focus_set() # Moves focus to canvas (doesn't happen automatically - not considered an input widget)
		clickedSquare = self._clicked_square(event)
		if clickedSquare:
			# Square already in focus
			if clickedSquare == self.selected:
				self._remove_focus()
			# Square not in focus
			else:
				self._remove_focus()
				self.selected = clickedSquare
				self._add_focus()
		else:
			self._remove_focus()

	# Determines relevant square (if any) + toggles color
	def _canvas_on_2click(self, event):
		clickedSquare = self._clicked_square(event)
		if clickedSquare:
			self.selected = clickedSquare
			self._toggle_selected()

	# If a selected cell contains a letter (implies color = white) then remove letter
	def _empty_cell(self, row, col):
		if self.letterIds[row][col]:
			self.delete(self.letterIds[row][col])
			self.letterIds[row][col] = None
			self.letters[row][col] = Constants.defaultEmptyChar

	# If a selected cell contains a letter (implies color = white) then remove letter
	def _empty_selected(self):
		if self.selected:
			row, col = self.selected[0], self.selected[1]
			self._empty_cell(row, col)

	# Adds a letter to a particular square
	def _add_letter(self, char, row, col):
		textSize = int(self.cellDims//1.2)
		self.letterIds[row][col] = self.create_text(self.xMargins+(col+0.5)*self.cellDims,
													self.yMargins+(row+0.5)*self.cellDims,
													text = char,
													font = f"({Constants.font[0]} {textSize}", 
													disabledfill = "#a3a3a3") # Gray, copied from app.mainarea.widthE
		self.letters[row][col] = char
	
	# Adds a letter to a particular square
	def _add_number(self, number, row, col):
		textSize = int(self.cellDims//1.2)
		numberSize = int(textSize//3)
		self.numberIds[row][col] = self.create_text(self.xMargins+(col+0.75)*self.cellDims,
													self.yMargins+(row+0.25)*self.cellDims,
													text = number,
													font = f"({Constants.font[0]} {numberSize}", 
													fill = "#a3a3a3") # Gray, copied from app.mainarea.widthE
		self.numbers[row][col] = number

	# Reset the numbers and numbers ID arrays
	def _resetNumbers(self):
		self.numbers = [[None]*self.width for i in range(self.height)]
		self.numberIds = [[None]*self.width for i in range(self.height)]

	# If square selected, toggles to white and adds letter
	def _canvas_on_key_press(self, event):
		if self.selected and event.char and ((event.char in string.ascii_lowercase) or (event.char in string.ascii_uppercase)):
			# Reset cell
			self._empty_selected()
			row, col = self.selected[0], self.selected[1]
			if self.squareColors[row][col]:
				self._toggle_selected()
			# Add letter to cell
			self._add_letter(event.char.lower(), row, col)

	# Removes focus from any grid square and moves focus to the canvas at large
	def _esc(self, event):
		self._remove_focus()
		self.selected = ()
		# Focus on canvas
		self.focus_set()

	# Destroys all items on the canvas
	def _destroy(self):
		for item in self.find_all():
			self.delete(item)

	# Handler for resize event. 
	# Also used to redraw board. If no argument is passed, redraw exactly as it was.
	# If a grid representation is passed, redraw the board with these letters instead.
	def _resize(self, newFill=[]):
		if self.gridDrawn.get():
			# Store initial configuration
			iselected = self.selected
			istate = self['state']
			iwidth = self.width
			iheight = self.height
			igrid = self.getRepresentation()
			inumbers = self.numbers
			# Reset canvas
			self.clear()
			# Redraw board
			if not newFill: 	# Keep the same
				self.drawBoard(width=iwidth, height=iheight, fill=igrid)
			else:				# Change fill
				self.drawBoard(width=iwidth, height=iheight, fill=newFill)
			# Restore + redraw numbers
			self.numbers = inumbers
			self.drawNumbers()
			# Redo configurations
			if iselected:
				row, col = iselected[0], iselected[1]
				self.selected = (row, col, self.squareColorIds[row][col])
				self._add_focus()
			if istate == 'normal':
				self.enable()
			elif istate == 'disabled':
				self.disable()

	# Set numbers
	def setNumbers(self):
		self.numbers = populateWithIth(self.getRepresentation())

	# Draw numbers
	# Note: Numbers must be initialised before this (usual call sequence is setNumbers() drawNumbers())
	def drawNumbers(self):
		for row in range(self.height):
			for col in range(self.width):
				number = self.numbers[row][col]
				if isinstance(number, int):
					self._add_number(number, row, col)

	# Destroy bindings + make letters gray
	def disable(self):
		self['state'] = 'disabled'
		self._remove_focus()
		self._remove_bindings()

	# Enabled user input + make appearance normal black + creates bindings
	def enable(self):
		self['state'] = 'normal'
		self._create_bindings()

	# Resets the entire canvas
	def clear(self):
		# Need to reset all attributes to defaults, and destroy all elements, set gridDrawn = 0
		self.gridDrawn.set(False)
		self._destroy()
		self.disable()
		# Reset stateful information. Allows for GC
		self.selected = ()
		self.squareColorIds = None
		self.squareColors = None
		self.letters = None
		self.letterIds = None
		self.numbers = None
		self.numberIds = None

	# Remove the numbers from the board
	def clearNumbers(self):
		for row in self.numberIds:
			for cid in row:
				if cid:
					self.delete(cid)
		self._resetNumbers()

	# Draw a grid with dimensions self.width x self.height
	def drawBoard(self, width=5, height=5, fill=[]):

		# Shouldn't be necessary but incase user forgot to clear board
		self.clear()

		# Initialising state (see __init__)

		self.gridDrawn.set(True)
		self.enable()

		self.width = width
		self.height = height

		self.selected = ()
		self.squareColors = [[0]*self.width for i in range(self.height)]
		self.squareColorIds = [[None]*self.width for i in range(self.height)]
		self.letters = [[Constants.defaultEmptyChar]*self.width for i in range(self.height)]
		self.letterIds = [[None]*self.width for i in range(self.height)]
		
		# Reset numbers
		self._resetNumbers()

		# Begin drawing board

		self.master.update()
		canvasWidth = self.winfo_width()
		canvasHeight = self.winfo_height()

		# Calculate width and height of cells
		tempCellWidth = min(100,((canvasWidth-2*self.margins)//self.width))
		tempCellHeight = min(100,((canvasHeight-2*self.margins)//self.height))
		# Choose the smallest of these (make square)
		self.cellDims = min(tempCellWidth,tempCellHeight)

		# Calculate the actual amount of space above and below, left and right, of actual grid
		self.xMargins = (canvasWidth-self.cellDims*self.width)//2
		self.yMargins = (canvasHeight-self.cellDims*self.height)//2

		# Calculate border width
		self.bwidth = max(1,min(3,self.cellDims//20))

		# Actually draw the grid
		for row in range(self.height):
			for col in range(self.width):
				item = self.create_rectangle(self.xMargins+col*self.cellDims, 
											   self.yMargins+row*self.cellDims,
											   self.xMargins+(col+1)*self.cellDims, 
											   self.yMargins+(row+1)*self.cellDims,
											   width=self.bwidth)
				self.squareColorIds[row][col] = item

		# Modify grid with supplied values - if passed
		if fill:
			assert(self.height == len(fill))
			assert(self.width == len(fill[0]))
			for row in range(self.height):
				for col in range(self.width):
					char = fill[row][col]
					if char == Constants.defaultEmptyChar:
						pass
					elif char == Constants.defaultBlockedChar:
						self._toggle_cell(row, col)
					elif char and ((char in string.ascii_lowercase) or (char in string.ascii_uppercase)):
						self._add_letter(char, row, col)

	# Get the representation of the current board
	def getRepresentation(self):
		grid = [[Constants.defaultEmptyChar for col in range(self.width)] for row in range(self.height)]
		for row in range(self.height):
			for col in range(self.width):
				grid[row][col] = self.letters[row][col]
				if self.squareColors[row][col]:
					grid[row][col] = Constants.defaultBlockedChar
		return grid

	# Redraw the board (same configuration - enabled/disabled, numbers etc)
	# Change fill if argument passed.
	def redraw(self, newFill=[]):
		if newFill:
			self._resize(newFill)
		else:
			self._resize()

class BottomBar(Frame):

	def __init__(self, master):

		self.master = master
		Frame.__init__(self, master)

		# Make easily visible
		# self['bg'] = 'green'

		# Create attributes
		self.currentSolution = 0
		self.gotoSolution = StringVar()
		self.totalSolutions = 0
		self.text = StringVar()

		self.prevB = Button(self, text='Prev', command=self.prev)
		self.nextB = Button(self, text='Next', command=self.next)
		self.gotoL = Label(self, text='Goto:')
		self.gotoE = Entry(self, textvariable=self.gotoSolution, width=6)
		self._update_text()
		self.label = Label(self, textvariable=self.text)

		# Enable input validation
		self._vcmd = (self.register(self._vcmd), "%P")
		self.gotoE.config(validate='key', validatecommand=self._vcmd, invalidcommand=self.bell)
		
		# Enable goto
		self.gotoE.bind("<Return>", lambda event: self._goto())

		# Place on screen
		self.prevB.grid(row=0, column=1, sticky='nesw', pady=20, padx=0)
		self.nextB.grid(row=0, column=2, sticky='nesw', pady=20, padx=0)
		self.gotoL.grid(row=0, column=4, sticky='nesw', pady=20, padx=0)
		self.gotoE.grid(row=0, column=5, sticky='nesw', pady=20, padx=0)
		self.label.grid(row=0, column=7, sticky='nesw', pady=20, padx=0)
		self.grid_rowconfigure(0, weight=1)
		self.grid_columnconfigure(0, weight=2)
		self.grid_columnconfigure(1, weight=0)
		self.grid_columnconfigure(2, weight=0)
		self.grid_columnconfigure(3, weight=1)
		self.grid_columnconfigure(4, weight=0)
		self.grid_columnconfigure(5, weight=0)
		self.grid_columnconfigure(6, weight=2)
		self.grid_columnconfigure(7, weight=0)

		# Initialize appearances
		self.reset()
		self._init_appearance()

	# Ensure entered text is a number
	def _vcmd(self, P):
		return len(P) == 0 or P.isnumeric()

	# Goto particular solution number
	def _goto(self):
		try:
			i = int(self.gotoSolution.get())
			if 1 <= i <= self.totalSolutions:
				self.currentSolution = i-1
				self._update_text()
				self.master.goto(self.currentSolution)
		except:
			pass

	# Updates the displayed text in label
	def _update_text(self):
		if self.totalSolutions == 0:
			p = '_'
			self.text.set(f"Solution 	{p:6} / {p:6}")
		else:
			self.text.set(f"Solution 	{self.currentSolution+1:6}	/ {self.totalSolutions:6}")

	def _init_appearance(self):

		# Global settings 
		widgets = [self.prevB, self.nextB, self.label, self.gotoL, self.gotoE]
		self.master.init_appearance(widgets)

		# Local settings

	# Called by outside functions. If provided with an argument
	# then set new totalSolutions + currentSolution = 1, otherwise 
	# default to 0 + interpret as grid having been cleared. 
	def reset(self, newTotal=0):
		# No solutions
		if newTotal == 0:
			self.currentSolution = 0
			self.totalSolutions = 0
			self.gotoSolution.set('')
			self._update_text()
			self.prevB['state'] = 'disabled'
			self.nextB['state'] = 'disabled'
			self.gotoL['state'] = 'disabled'
			self.gotoE['state'] = 'disabled'
			self.label['state'] = 'disabled'
		else:
			self.currentSolution = 0
			self.totalSolutions = newTotal
			self._update_text()
			self.prevB['state'] = 'normal'
			self.nextB['state'] = 'normal'
			self.gotoL['state'] = 'normal'
			self.gotoE['state'] = 'normal'
			self.label['state'] = 'normal'

	def prev(self):
		self.currentSolution = (self.currentSolution-1)%self.totalSolutions
		self._update_text()
		self.master.prev()

	def next(self):
		self.currentSolution = (self.currentSolution+1)%self.totalSolutions
		self._update_text()
		self.master.next()

	def get(self):
		return self.currentSolution

class Application(Tk):

	def __init__(self):

		Tk.__init__(self)

		# Variable to indicate whether a solve is in progress
		self.solving = False
		self.solutions = ([], []) 	# (listOfWordIds, list of solutions)
		self.index = 0 				# Solutions currently drawn

		# Set screen size + title + make adjustable
		self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}")
		self.title("CrosswordSolver")
		self.grid_columnconfigure(0, weight=0, minsize=150)
		self.grid_columnconfigure(1, weight=1, minsize=300)
		self.grid_rowconfigure(0, weight=1, minsize=150)
		self.grid_rowconfigure(1, weight=0)
		self['bg'] = 'black'

		# Initialize screen areas
		self.sidebar = SideBar(self)
		self.mainarea = MainArea(self)
		self.bottombar = BottomBar(self)
		self.sidebar.grid(column=0, row=0, rowspan=2, sticky='nsew', padx=1, pady=1) # The padding results in a black border around areas
		self.mainarea.grid(column=1, row=0, sticky='nsew', padx=1, pady=1)
		self.bottombar.grid(column=1, row=1, sticky='nsew', padx=1, pady=1)

		# Link global gridDrawn with mainarea.gridDrawn
		# This should strictly be used for queries - never modified
		global gridDrawn
		gridDrawn = self.mainarea.gridDrawn

		# Initialize appearance of sidebar
		self.sidebar._clear()

		# DEV ----------------
		# self.printGrid = Button(text="Print Grid", command=lambda:print(repr(self.mainarea.getRepresentation())))
		# self.printGrid.grid()
		# DEV ----------------

	def init_appearance(self, widgets):

		for w in widgets:
			# All
			w['font'] = Constants.font
			# Button specific
			if type(w) == Button:
				w['width'] = Constants.buttonWidth
	
	######################################################################
	# Functions with which to interact with application
	######################################################################

	# Called by mainarea.draw
	def drawGrid(self):
		if not self.solving:
			self.mainarea.drawBoard(self.sidebar.getWidth(), self.sidebar.getHeight(), fill=[])
		else:
			# FIX
			pass

	# Called by mainarea.solve
	def solve(self):
		currentBoard = self.mainarea.getRepresentation()
		self.mainarea.setNumbers()
		self.mainarea.drawNumbers()
		self.mainarea.disable()
		self.update()
		printGrid(currentBoard)
		self.solutions = solve(gridToWordClassList(currentBoard))
		self.bottombar.reset(len(self.solutions[1]))
		newBoard = wordClassListToGrid(currentBoard, self.solutions[1][0], self.solutions[0])
		self.mainarea.redraw(newBoard)

	# Called by mainarea.clear
	def clear(self):
		self.mainarea.clear()
		self.bottombar.reset()
		self.solutions = []

	######################################################################
	# Functions with which to display solutions
	######################################################################
	
	# Called by bottombar.prev
	def prev(self):
		currentBoard = self.mainarea.getRepresentation()
		self.index -= 1
		self.index %= len(self.solutions[1])
		newBoard = wordClassListToGrid(currentBoard, self.solutions[1][self.index], self.solutions[0])
		self.mainarea.redraw(newBoard)
	
	# Called by bottombar.next
	def next(self):
		currentBoard = self.mainarea.getRepresentation()
		self.index += 1
		self.index %= len(self.solutions[1])
		newBoard = wordClassListToGrid(currentBoard, self.solutions[1][self.index], self.solutions[0])
		self.mainarea.redraw(newBoard)

	# Called by bottombar.goto
	def goto(self, index):
		currentBoard = self.mainarea.getRepresentation()
		self.index = index
		newBoard = wordClassListToGrid(currentBoard, self.solutions[1][self.index], self.solutions[0])
		self.mainarea.redraw(newBoard)

app = Application()

app.mainloop()