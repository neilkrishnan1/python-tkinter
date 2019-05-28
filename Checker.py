from tkinter import *
from tkinter import messagebox
import logging
logging.basicConfig(level='WARNING')

class Square(Canvas):
	''' Acts as a square in the checker board,'''
	def __init__(self, x, y, master, colorback, colorcir=None):   
		Canvas.__init__(self,master,width=80,height=80,bg=colorback,\
						bd=5,relief=FLAT)                                                                                                                          # Initializing square with flat relief and dimensions 80 X 80
		self.id = None
		if colorcir != None:
			self.id = self.create_oval(10, 10, 80, 80, outline='black',fill=colorcir, width=1)                                                                     # If there is a given colored checker make it (create_oval)
		# Initializing Square information
		self.astrix = None
		self.colorcircle=colorcir
		self.colorback = colorback
		self.status = 'regular'
		self.x = x
		self.y = y
		
	def remove (self):
		'''Removes the checker from the square.'''
		if self.id != None:                                                                                                                                        # Deleting anything that might be on the box like a checker or and * for kings
			self.delete(self.id)
		if self.astrix != None:
			self.delete(self.astrix)
		self.colorcircle = None                                                                                                                                    # Changing game information to adapt box
		self.id = None
		self.astrix = None
		logging.info("({}, {}) changed to {}. Its supposed to be None".format(self.x, self.y, self.colorcircle))
	
	def red (self):
		'''Adds a red checker to the square.'''
		self.remove()                                                                                                                                              # Taking off anything that might be on the square
		self.id = self.create_oval(10, 10, 80, 80, outline='black',fill="red", width=1)                                                                            # Putting Red checker on square and changing square information
		self.colorcircle = 'red'
		logging.info("({}, {}) changed to {}. Its supposed to be red".format(self.x, self.y, self.colorcircle))
		
	def white (self):
		'''Adds a white checker to the square.'''
		self.remove()                                                                                                                                              # Taking off anything that might be on the square
		self.id = self.create_oval(10, 10, 80, 80, outline='black',fill="white", width=1)                                                                          # Putting Red checker on square and changing square information
		self.colorcircle = 'white'                                                                                                                                 
		logging.info("({}, {}) changed to {}. Its supposed to be white".format(self.x, self.y, self.colorcircle))
		
	def king (self):
		'''Makes checker status a king and puts astrix'''
		if self.astrix == None:
			self.astrix = self.create_text(45,65,fill='black',font=('Helvetica', '60'), text='*')                                                                  # Puts an * on the square if there is none already and changes game information
		self.status = 'king'
		logging.info("({}, {}) Changed to {}".format(self.x, self.y, self.status))
	def __str__(self):
		'''Returns information of Square'''
		return "Square ({}, {}) checker={}, status={}".format(self.x, self.y, self.colorcircle, self.status)
		
class Show_Turn (Canvas):
	''' Is the turn square at the bottom which changes color based on who's turn it is.'''
	def __init__ (self, master):
		Canvas.__init__(self,master,width=80,height=80,bg='gray',\
						bd=5,relief=FLAT)                                                                                                                         # Makes the turn square with gray background and initializes a red circle on the square
		self.id = self.create_oval(10, 10, 80, 80, outline='black',fill='red', width=1)
	def change_color (self, color):
		''' Changes color to specified color by deleting and replacing the circle'''
		self.delete(self.id)
		self.id = self.create_oval(10, 10, 80, 80, outline='black',fill=color, width=1)                                                                            
		
class Board(Frame):
	''' Acts as the Checker board and has all the logistics of the game.'''
	def __init__ (self, master):
		Frame.__init__(self, master)                                                                                                                               # Initializing frame and grid
		self.grid()
		self.board = [[None] * 8 for j in range(8)]                                                                                                                # Creating Board matrix
		colorback = [['blanched almond', 'dark green'] * 4] + [['dark green', 'blanched almond'] * 4]                                                              # Making matrices for the color of the squares on the board, if there are going to be checkers and what color they will be etc...
		colorback = colorback * 4                                                                                                                     
		colorcircle = [[None,'red'] * 4] + [['red',None] * 4] + [[None,'red'] * 4] + [[None]*8]*2 + [['white',None] * 4] + [[None,'white'] * 4] + [['white',None] * 4] 
		for i in range(8):
			for j in range(8):
				# Note that i ranges over y-coordinate, and j ranges over x-coordinate.
				self.board[i][j] = Square(j, i, self, colorback[i][j], colorcircle[i][j])                                                                          # Creating all of the squares with the initialized information in the matrices                                                                           
				self.board[i][j].grid(row=i, column=j)
		self.bind_class('Canvas', '<Button-1>', self.press)                                                                                                        # Binding all square presses to function self.press()
		self.turn = 'red'                                                                                                                                         
		Label(self, text = "Turn: ", font = ('Helvetica', '24')).grid(row=8, column=2)                                                                             # Creating a label that says turn and adding a Show_Turn class to give it
		self.cont_jump=None
		self.turncir = Show_Turn(self)
		self.turncir.grid(row=8, column=3)
		# Setting up other game information
		self.selectbox = None
		self.cont = False
		for row in self.board:
			for square in row:
				logging.debug(str(square))
		
	def press (self, event):
		'''Handles the button press event that either selects a square or moves the checker to the square.'''
		if self.selectbox == None:
			'''Select the square.'''
			if event.widget.colorcircle == None or event.widget.colorcircle != self.turn:                                                                         # If there is no checker on the square or it is not the checkers turn exit
				return
			self.selectbox = event.widget                                                                                                                         # Setting the selected box and making it look selected
			self.selectbox['bg'] = 'yellow'
			logging.info("Selected {}".format(self.selectbox))
		else:
			'''Move the checker to this square.'''
			box = event.widget                                                                                                                                    # Square that the selected box's checker is going to move to
			l = None
			if box.colorcircle != None:
				if not(self.cont):
					self.selectbox['bg'] = self.selectbox.colorback
					self.selectbox = None
				return
			else: l = self.legal(box)
			if box.colorcircle != None or not(l[0]):                                                                                                              # If there is a Checker or not l[0] (boolean for if it is legal) we are doing the same process of unselecting
				if not(self.cont):
					self.selectbox['bg'] = self.selectbox.colorback
					self.selectbox = None
				return
			diddouble = l[1]                                                                                                                                      # If the person took another piece
			logging.info("diddouble is {}".format(diddouble))
			ifturn = self.turn
			# Changing the new box to have a () checker and changing the turn. Also we are changing the piece to a king
			if self.selectbox.colorcircle == 'red':
				box.red()
				self.turn = 'white'
			elif self.selectbox.colorcircle == 'white':
				box.white()
				self.turn = 'red'
			if self.selectbox.astrix != None:
				box.king()
			if (box.y == 7 and box.colorcircle == 'red') or (box.y == 0 and box.colorcircle == 'white'):
				box.king()
			else:
				box.status, self.selectbox.status = self.selectbox.status, None
			# Unselecting the selectbox and changing it to have no checker
			self.selectbox.remove()
			self.selectbox['bg'] = self.selectbox.colorback
			self.selectbox = box
			if self.continue_jump() and diddouble:                                                                                                               # If the person can continue his jump by taking another piece and has already taken a piece we are making them have another turn to jump
				self.turn = ifturn
				self.selectbox['bg'] = 'yellow'
				if self.cont_jump == None:
					self.cont_jump = Label(self, text="Must continue jumping", font = ('Helvetica', '18'))                                                       # Creating a label on the side that tells the person to continue their jump
					self.cont_jump.grid(row=4,column=8,columnspan=2)
				self.cont = True
			else:
				# Reseting everything and taking of the label to continue the jump
				self.selectbox = None
				self.turncir.change_color(self.turn)
				if self.cont_jump != None:
					self.cont_jump.pack_forget()
					self.cont_jump.destroy()
					self.cont_jump = None
				self.cont = False
			oppositecolor = 'white' if self.turn == 'red' else 'red'
			if self.win(self.turn):                                                                                                                             # If win condition then say the person one
				messagebox.showinfo('Checker', '{} Won !!!!!!!'.format(oppositecolor),parent=self)
				exit()
	def legal (self, box):
		'''Returns true if a move is legal, false otherwise.
		
		The method iterates through all possible legal offsets from the current
		position to see if the user clicked on one of these squares. It returns true
		or false based on this checks. 
		
		Arguments:	
		box 			 The box to move the checker to.
		self.selectbox	 The box from where to move the checker.	
		'''
		
		assert(self.selectbox != None)
		assert(self.selectbox.status == 'regular' or self.selectbox.status == 'king')
		assert(box.colorcircle == None)   # Box should not have a checker
		logging.info('Checking legal move for ({}, {}) to ({}, {})'.format(self.selectbox.x, self.selectbox.y, box.x, box.y))
		
		# Build the legal offsets for the selectbox. A regular checker can
		# move towards the opponent on two diagonal squares. A king can move
		# can move in four diagonal squares. Origin is at the top-left corner
		# and red regular checker moves to larger values of y and white regular checker 
		# moves to smaller values of y.
		xoff = []
		yoff = []
		# Setting legal offsets for all cases
		if self.selectbox.status == 'king':
			xoff = [1,1,-1,-1]
			yoff = [1,-1,1,-1]
		else:
			if self.selectbox.colorcircle == 'red':
				xoff = [1,-1]
				yoff = [1,1]
			else:
				xoff = [1,-1]
				yoff = [-1,-1]
		# Runs through all the legal offsets and if one of the positions is equal 
		# to the position of the box posted then return true and that this was a single move
		for i in range(len(xoff)):                                                                                                                             
			legalx = self.selectbox.x + xoff[i]
			legaly = self.selectbox.y + yoff[i]
			if legalx == box.x and legaly == box.y:
				return [True, False]

		# Now we handle the case where the checker jumps over an opponent checker.
		# The legal moves are same as before but with offsets of size two and 
		# they require that there is an opponent checker in the middle of the jump.
		# Setting legal offsets for the legal move and the middle square in that move
		xmid, ymid = xoff, yoff
		if self.selectbox.status == 'king':
			xoff = [2,2,-2,-2]
			yoff = [2,-2,2,-2]
		else:
			if self.selectbox.colorcircle == 'red':
				xoff = [2,-2]
				yoff = [2,2]
			else:
				xoff = [2,-2]
				yoff = [-2,-2]
		# Runs through all the legal offsets and middle ofsets and if one of the positions 
		# is equal and the box in the middle of the jump has a checker of opposite color then 
		# remove the middle checker and return that the move is legal and that this was a double move
		for i in range(len(xoff)):
			legalx = self.selectbox.x + xoff[i]
			legaly = self.selectbox.y + yoff[i]
			middlex = self.selectbox.x + xmid[i]
			middley = self.selectbox.y + ymid[i]
			oppositecolor = 'white' if self.selectbox.colorcircle == 'red' else 'red'			
			if legalx == box.x and legaly == box.y:
				middle = self.board[middley][middlex]
				if middle.colorcircle == oppositecolor:
					logging.info('Jumped over ({}, {})'.format(middlex, middley))
					middle.remove()
					return [True, True]
		return [False, False]
		
	def continue_jump (self):
		''' Checks if another double jump is possible'''
		# Setting up the offsets for the legal move and the middle square in that move as 
		# this is only for double jumps
		xmid = []
		ymid = []
		if self.selectbox.status == 'king':
			xmid = [1,1,-1,-1]
			ymid = [1,-1,1,-1]
		else:
			if self.selectbox.colorcircle == 'red':
				xmid = [1,-1]
				ymid = [1,1]
			else:
				xmid = [1,-1]
				ymid = [-1,-1]
		xoff = []
		yoff = []
		if self.selectbox.status == 'king':
			xoff = [2,2,-2,-2]
			yoff = [2,-2,2,-2]
		else:
			if self.selectbox.colorcircle == 'red':
				xoff = [2,-2]
				yoff = [2,2]
			else:
				xoff = [2,-2]
				yoff = [-2,-2]
		#Runs through all the offsets for middle and legal moves. 
		#If the final outcome is within the bounds of the checker board 
		#and there is a checker of opposite color in the middle square then 
		#we are returning True as yes the player can make another jump.
		for i in range(len(xoff)):
			legalx = self.selectbox.x + xoff[i]
			legaly = self.selectbox.y + yoff[i]
			middlex = self.selectbox.x + xmid[i]
			middley = self.selectbox.y + ymid[i]
			c = False
			if legalx >= 0 and legalx < 8 and legaly >= 0 and legaly < 8:
				c = True
				oppositecolor = 'white' if self.selectbox.colorcircle == 'red' else 'red'			
				if self.board[legaly][legalx].colorcircle == None:
					middle = self.board[middley][middlex]
					if middle.colorcircle == oppositecolor:
						logging.info("Returned True")
						return True
		return False
		
	def win (self, color):
		''' Returns if one of the players won'''
		for i in range(8):                                                                                                                                      # Running through all of the squares
			for j in range(8):
				# Note that i ranges over the y-coordinate and j ranges over the x-coordinate
				box = self.board[i][j]                                                                                                                          # Initializing square
				if box.colorcircle == color:
					# Setting legal offsets
					xoff = []
					yoff = []
					if box.status == 'king':
						xoff = [1,1,-1,-1]
						yoff = [1,-1,1,-1]
					elif box.status == 'regular':
						if color == 'red':
							xoff = [1,-1]
							yoff = [1,1]
						else:
							xoff = [1,-1]
							yoff = [-1,-1]
					# Running through all the legal offsets and checking that if the legal offset square is within bounds and doesn't already have a square. 
					#If it doesn't than return False.
					for k in range(len(xoff)):
						legalx = box.x + xoff[k]
						legaly = box.y + yoff[k]
						if legalx >= 0 and legalx < 8 and legaly >= 0 and legaly < 8:
							if self.board[legaly][legalx].colorcircle == None:
								logging.info("Didn't win legalx = {} legaly = {} color of circle = {}".format(legalx, legaly, self.board[legaly][legalx].colorcircle))
								return False
					# Setting the offsets for the jump
					xmid = xoff
					ymid = yoff
					xoff = []
					yoff = []
					if box.status == 'king':
						xoff = [2,2,-2,-2]
						yoff = [2,-2,2,-2]
					elif box.status == 'regular':
						if color == 'red':
							xoff = [2,-2]
							yoff = [2,2]
						else:
							xoff = [2,-2]
							yoff = [-2,-2]
					#Runs through all the offsets for middle and legal moves. 
					#If the final outcome is within the bounds of the checker board 
					#and there is a checker of opposite color in the middle square then 
					#we are returning True as yes the player can make another jump.
					for k in range(len(xoff)):
						legalx = box.x + xoff[k]
						legaly = box.y + yoff[k]
						middlex = box.x + xmid[k]
						middley = box.y + ymid[k]
						if legalx >= 0 and legalx < 8 and legaly >= 0 and legaly < 8:
							oppositecolor = 'white' if color == 'red' else 'red'			
							if self.board[legaly][legalx].colorcircle == None:
								middle = self.board[middley][middlex]
								if middle.colorcircle == oppositecolor:
									return False
		logging.info("won")
		return True
		
root = Tk()
t = Board(root)
t.mainloop()