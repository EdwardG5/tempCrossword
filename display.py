from tkinter import *

class SideBar(Frame):
	
	def __init__(self, master):
		Frame.__init__(self, master)
		self['bg'] = 'red'

class MainArea(Frame):
	
	def __init__(self, master):
		Frame.__init__(self, master)
		self['bg'] = 'blue'
		
class BottomBar(Frame):
	
	def __init__(self, master):
		
		self.master = master
		Frame.__init__(self, master)
		
		# Make easily visible
		self['bg'] = 'green'
		
		# Create attributes
		self.prev = Button(self, text='Prev', command=master.prev)
		self.next = Button(self, text='Next', command=master.next)
		self.currentSolution = 0
		self.totalSolutions = 0
		self.text = StringVar()
		self._update_text()
		self.label = Label(self, textvariable=self.text)

		# Place on screen
		self.prev.grid(row=0, column=1, sticky='nesw', pady=20, padx=5)
		self.next.grid(row=0, column=2, sticky='nesw', pady=20, padx=5)
		self.label.grid(row=0, column=4, sticky='nesw', pady=20, padx=5)
		self.grid_rowconfigure(0, weight=1)
		self.grid_columnconfigure(0, weight=1)
		self.grid_columnconfigure(1, weight=0)
		self.grid_columnconfigure(2, weight=0)
		self.grid_columnconfigure(3, weight=1)
		self.grid_columnconfigure(4, weight=0)


	# Updates the displayed text in label
	def _update_text(self):
		if self.totalSolutions == 0:
			p = '_'
			self.text.set(f"Solution 	{p:6} / {p:6}")
		else:
			self.text.set(f"Solution 	{self.currentSolution+1:6}	/ {self.totalSolutions:6}")


	# Called by outside functions. If provided with an argument
	# then set new totalSolutions, otherwise default to 0 + interpret
	# as grid having been cleared. 
	def reset(self, newTotal=0):
		# No solutions
		if newTotal == 0:
			self.currentSolution = 0
			self.totalSolutions = 0
			self._update_text()
			self.prev['state'] = 'disabled'
			self.next['state'] = 'disabled'
		else:
			self.currentSolution = 1
			self.totalSolutions = newTotal
			self._update_text()
			self.prev['state'] = 'normal'
			self.next['state'] = 'normal'


		
class Application(Tk):
	
	def __init__(self):
		
		Tk.__init__(self)
		
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

	def prev(self):
		pass

	def next(self):
		pass

app = Application()

app.mainloop()