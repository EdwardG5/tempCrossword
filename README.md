# Crossword
Crossword solver with GUI allowing users to create custom board. Multi-language support: works with arbitrary word lists. Built entirely in Python. GUI powered by TKinter. 

#---------------------------------------------------------------------------#

Files: 
- display: GUI interface
- displayVSEAN: Legacy GUI interface. 
- crosswordSolver.py: algorithmic brains. # Note: solution list is backwards relative to given list
- wordClass: data structure to represent words
- nodeClass: data structure to build tries
- fileToList: method to read words from file. Called from crosswordSolver
- index: calculate index in pointer lists (wordClass) from ascii value
- hardCodedExamples: boards -> word structures hardcoded 
- constant.py: Constants class containing GUI settings, as well as board settings (e.g. character representing empty space, blocked). 

#---------------------------------------------------------------------------#

From command line: 

crosswordSolver as independent application: 
- modify parameters at beginning 
- modify main function at the very end 
python3 crosswordSolver.py 

GUI:
- modify parameters at beginning of crosswordSolver
- empty main (-> pass) in crosswordSolver
- modify parameters at beginning of display
python3 display.py 

#---------------------------------------------------------------------------#

Pending issues: 
1) display is not correctly translating boards into the word structures. : RESOLVED
2) display is not correctly displaying the found solutions (maybe - unclear since the solutions don't make sense right now: see 1)
3) The logic flow is right now concentrated in crosswordSolver. It makes more sense to have this in display - or in a separate file calling both GUI and logic controls. Right now e.g. the dictionary is converted into a trie every time submit is hit - this is something that should only be done once. 

#---------------------------------------------------------------------------#

Work to be done (in addition to bug fixes (see pending issues)): 

GUI:
- after altering dimensions, let user hit enter rather than having to click submit : RESOLVED
- after modifying the board, let user hit enter rather than having to click submit : RESOLVED
(action determined by what area is currently selected)
- Allow user to select word list used
- (extension: allow user to upload their own wordlist)
- allow user to view multiple solutions: prev next buttons allowing them to flip through the set of solutions 
- display the number of solutions found
- reset button to clear board of all modifications : RESOLVED
- title of window is tk not crosswordSolver : RESOLVED

Logic: 
- Pre-process word list -> decide the best order in which to evaluate them while solving (open problem, best approach not known)

Ambitious (after everything else):
- Upload this to the internet. Create a widget or website etc. 
- Use machine learning in combination with past usage to determine more optimal heuristics

