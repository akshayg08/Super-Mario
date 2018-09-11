import numpy as np
import people
import os
import time
import random

class Board:
	"""class to initialize the board"""
	prev_i = 38
	prev_j = 0
	prev_k = 100
	triangle = []
	underscore = []
	open_ = []
	close_ = []
	gap = []
	board = np.full((38,800),' ')
	x = board.shape[0] 
	y = board.shape[1]	
	board[10:12,:400]='X'
	board[x-2:x,:]='X'
	board[10:,0:2]='X'
	board[6:,398:400]='X'

	board[6:,y-2:y]='X'
	board[33:36,382:398]='I'


	def _cloud(start):
		"""initialize clouds"""
		Board.board[17][start+8]='('
		Board.board[17][start+9:start+16]='_'
		Board.board[17-1][start+9]='('
		Board.board[17-2][start+10]='('
		Board.board[17-3][start+11:start+14]='_'
		Board.board[17-2][start+14]=')'
		Board.board[17-1][start+15]=')'
		Board.board[17][start+16]=')'

		for i in range(Board.board.shape[0]):
			for j in range(Board.board.shape[1]):
				if Board.board[i][j]=='_':
					Board.underscore.append((i,j))
				elif Board.board[i][j]==')':
					Board.close_.append((i,j))
				elif Board.board[i][j]=='(':
					Board.open_.append((i,j))


	def pipe(start):
		"""obstacles"""
		for i in range(30,36):
			for j in range(start,start+5):
				Board.board[i][j]='T'

	def gaps(start):
		Board.board[36:38,start:start+7]='-'
		Board.gap.append(start)

	def brick(start):
		Board.board[24][start:start+3]='B'	

	def support(x,y,z):
		Board.board[x-1][range(y,y+z,3)]='0'
		Board.board[x][y:y+z]='/'

	def stairs(start):
		Board.board[31:36,start:start+5]='T'
		for i in range(31,36):
			for j in range(start,start+35-i):
				Board.board[i][j]=' '

	def tri(start):	
		for i in range(28,36):
			for j in range(start,start+8-i+28):
				Board.board[i][j]=' '

			for k in range(j+1,j+1+2*(i-28)-1):
				Board.triangle.append((i,k))
				Board.board[i][k]='.'

	def bonus_round():
		os.system('clear')
		print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\t\t\t\t\t\tBONUS ROUND")
		Board.prev_j = 300
		Board.prev_k = 400		
		for i in range(6,36):
			for j in range(Board.prev_j,450):
				if (i,j) in Board.triangle:
					Board.triangle.remove((i,j))

				elif (i,j) in Board.underscore:
					Board.underscore.remove((i,j))

				elif (i,j) in Board.close_:
					Board.close_.remove((i,j))
					
				elif (i,j) in Board.open_:
					Board.open_.remove((i,j))		

				Board.board[i][j]=' '


		people.Mario.remove_enemy()		
		Board.board[36:38,:]='X'
		Board.board[14][445]='A'
		Board.board[15][440:449]='/'
		Board.board[:,448:450]='X'		
		Board.board[35][Board.prev_j+10]='M'
		Board.support(30,Board.prev_j+20,30)
		Board.support(15,Board.prev_j+20,30)
		Board.support(23,Board.prev_j+35,30)
		Board.support(23,Board.prev_j+80,30)
		Board.support(15,Board.prev_j+90,30)
		Board.support(30,Board.prev_j+90,30)
		Board.board[33:36,434:450]='K'
		Board.board[32][438]='S'
		time.sleep(2)
		init_board(38,Board.prev_j,Board.prev_k)
		
"""initializing obstacles"""
for i in range(17,399,50):
	Board._cloud(i)

for i in range(45,340,100):
	Board.pipe(i)

for i in range(103,380,120):
	Board.gaps(i)

for i in range(29,380,200):
	Board.brick(i)

for i in range(50,380,200):
	Board.support(23,i,10)

for i in range(25,380,200):
	Board.support(30,i,10)

for i in range(70,350,40):
	Board.tri(i)

Board.stairs(170)


def init_board(x,y,z):
	"""function to print frame"""
	print("\nSCORE:",people.Mario.score,"\nLIVES:",people.Mario.lives,"\nBONUS:",people.Mario.bonus)
	for i in range(6,x):
		if z>=500:
			z=500
		for j in range(y,z):
			print(Board.board[i][j],end = "")
		print()
