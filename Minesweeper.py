from tkinter import *
from tkinter import messagebox
import random

class Box(Canvas):
	'''A Box on the Minesweeper grid that can reveal or flag itself'''
	def __init__(self, master, mine, x, y):
		'''Setting up starting information about box'''
		Canvas.__init__(self,master,width=40,height=40,bg='white',\
						bd=3,relief=RAISED)
		self.mine = mine
		self.openned = False
		self.isflagged = False
		self.x = x
		self.y = y
		self.id = ''
	def can_reveal(self):
		'''Returns if the box is a mine'''
		if not self.isflagged:
			self.openned = True
		return self.mine 

	def flagged (self):
		'''Flags a box by putting a '*' if the box is not already openned'''
		if not self.openned: 
			self.isflagged = not self.isflagged
		else:
			return None
		if self.isflagged:
			self.id = self.create_text(24,24,fill='black',font=('Helvetica', '15'), text='*')     # Creating '*'
		else:
			self.delete(self.id)
			
					
class Board(Frame):
	'''The grid of minesweeper and all game information'''
	def __init__ (self, master, dix, diy, mines):
		Frame.__init__(self, master)                                                              # Setting up Frame and grid
		self.grid()
		self.colormap = ['','blue','darkgreen','red','purple','maroon','cyan','black','dim gray'] # Creating colormap of colors displayed by the adjacent mines
		'''Creating actual board'''
		self.board = [None] * diy
		self.mines_left = mines
		for i in range(diy):
			self.board[i] = [None] * dix
		self.mines = random.sample(range(dix*diy), mines)
		for x in range(dix):
			for y in range(diy):
				index = y * dix + x
				if index in self.mines:
					self.board[x][y] = Box(self, True, x, y)
				else:
					self.board[x][y] = Box(self, False, x, y)
				self.board[x][y].grid(row=x, column=y)
		self.mineLabel = Label(self, text = mines, font = ('Helvetica', '18'))                    # Creating a label for number of mines left (total mines - numflags)
		self.mineLabel.grid(row=diy, column = int(dix/2), sticky=S)
		self.bind_class('Canvas', '<Button-1>', self.reveal)                                      # Binding all canvases to the reveal and flag functions of board class
		self.bind_class('Canvas', '<Button-3>', self.flag)
		self.dix = dix                                                                            # Adding dimensions to attributes
		self.diy = diy
		
		# Sets local mines for each box.
		for x in range(dix):                                                                      # Telling each box on the board the number of adjacent mines
			for y in range(diy):
				self.set_local_mines(self.board[x][y])
		
	def reveal (self, event):
		''' Reveals the box that is pressed'''
		box = event.widget                                                                        # The box that is going to be revealed
		if not box.isflagged:                                                                     # Conditions for the box
			if not box.can_reveal():
				box['relief'] = SUNKEN                                                            # Reveals box by changing relief and background color   
				box['bg'] = 'yellow'
				if box.local_mines == 0:                                                          # If the box has no adjacent mines we open those boxes
					self.autoexpose(box)
				self.id = box.create_text(24,24,fill=self.colormap[box.local_mines],font=('Helvetica', '15'), text=box.local_mines)
				if self.win():
					messagebox.showinfo('Minesweeper','Congratulations -- you won!',parent=self)  # Winning condition
			else:
				self.reveal_all()
				messagebox.showerror('Minesweeper','KABOOM! You lose.',parent=self)               # Losing condition

	def reveal_specific(self, box):
		''' Reveal a specific box by giving the box'''
		if not box.openned and not box.mine:                                                      # Similar to the reveal, but checks if the box is not a mine
			if not box.isflagged:
				box['relief'] = SUNKEN
				box['bg'] = 'yellow'
				box.openned = True
				self.id = box.create_text(24,24,fill=self.colormap[box.local_mines],font=('Helvetica', '15'), text=box.local_mines)
				if self.win():
					messagebox.showinfo('Minesweeper','Congratulations -- you won!',parent=self)  # Winning condition

	def flag(self, event):
		''' Flagging a box and changing number of mines. '''
		box = event.widget
		if box.isflagged:
			self.mines_left += 1
		else:
			self.mines_left -= 1
		self.mineLabel['text'] = self.mines_left
		box.flagged()                                                                             # Calling the box to flag itself

	def set_local_mines (self, box):
		''' Sets local mines for box given '''
		x = box.x
		y = box.y
		local_mines = 0
		for posx in [x-1, x, x+1]:                                                                # Running through all possible adjacent x's and y's
			for posy in [y-1, y, y+1]:
				if posx >= 0 and posx < self.dix and posy >= 0 and posy < self.diy:               # Making sure the position is in bounds and is not itself
					if not(posx == x and posy == y):
						if self.board[posx][posy].mine:                                           # Increasing adjacent mines if the box is a mine
							local_mines += 1
		box.local_mines = local_mines

	def get_adj (self, cell):
		''' Returns the positions of all boxes that are not mines'''
		x = cell[0]
		y = cell[1]
		adj = []
		for posx in [x-1, x, x+1]:                                                                # Similar process to set_local_mines
			for posy in [y-1, y, y+1]:
				if posx >= 0 and posx < self.dix and posy >= 0 and posy < self.diy:
					if not(posx == x and posy == y):
						if not self.board[posx][posy].mine:                                       # Adding position tuple to list if it is not a mine
							adj += [(posx, posy)]
		return adj                                                                                # Returning list
                                                                                                  
	def autoexpose (self, box):
		'''	Expose all boxes adjacent that are not mines and continue process if they have no local mines'''
		should_open = [(box.x, box.y)]                                                            
		while len(should_open) != 0:                                                              # While there is no more elements in the boxes that should be openned                                                            
			cell, should_open = should_open[0], should_open[1:]                                   # Taking off one cell to be openned and replacing the list with the rest                       
			for adj in self.get_adj(cell):                                                        # For the boxes adjacent to the box
				posx = adj[0]
				posy = adj[1]
				box = self.board[posx][posy]                                                      # Creating box of cell adjacent cell positions
				if not box.openned and box.local_mines == 0:                                      # If box is not openned and has no adjacent mines add coordinates to the list of boxes
					should_open += [adj]                                           
				self.reveal_specific(box)                                                         # Reveal box
				
	def reveal_all (self):
		''' Reveals all mine squares'''
		for x in range(self.dix):                                                                 # For every box
			for y in range(self.diy):
				if self.board[x][y].mine:                                                         # If it is a mine reveal it by making background red and text be an '*'
					self.board[x][y]['bg']='red'
					if not self.board[x][y].isflagged:
						self.board[x][y].openned = False
						self.board[x][y].flagged()
					
	def win (self):
		''' Checks if player won'''
		for x in range(self.dix):                                                                 # For every box
			for y in range(self.diy):
				if (not self.board[x][y].openned) and (not self.board[x][y].mine):                # If it is not openned and not a mine return False (the player has not won)
					return False		
		return True                                                                               # Return True (the player has won)
		
root = Tk()
b = Board(root, 15, 15, 25)
b.mainloop()