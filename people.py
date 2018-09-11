from board import Board,init_board
import get
import os 
import enemy
import time
import random
from subprocess import call

obstacles = ['/','T','X','B','H','I','K','S','E']
pass_through = ['T','S','0','/','X','K','I','M','E']

class Parent:
	"""Parent class from which enemy , boss and mario inherit."""
	attack = 0
	vel = 1
	bullets = []

class Enemy(Parent):
	enemies = []
	def __init__(self,x,y):
		self.x = x
		self.y = y
		self.hit = 0
		Board.board[x][y]='@'

	def _move_forward(enemy):
		"""move forward function fro enemy."""
		Board.board[enemy.x][enemy.y]=' '
		enemy.y += Enemy.vel 
		if((enemy.x,(enemy.y)-Enemy.vel) in Board.triangle):
			Board.board[enemy.x][(enemy.y)-Enemy.vel]='.'

		if(Board.board[enemy.x][enemy.y]=='M'):
			Mario.lives -= 1
			if Mario.lives<=0:
				return "exit"
			os.system('clear')
			print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\t\t\t\t\t\tNumber of Mario left:",Mario.lives)
			Mario.respawn(enemy.x,enemy.y)
			time.sleep(2)

		Board.board[enemy.x][enemy.y]='@'
				

	def _move_backward(enemy):
		"""move backward function for enemy"""
		Board.board[enemy.x][enemy.y]=' '
		enemy.y -= Enemy.vel
		if((enemy.x,(enemy.y)+Enemy.vel) in Board.triangle):
			Board.board[enemy.x][(enemy.y)+Enemy.vel]='.'

		if(Board.board[enemy.x][enemy.y]=='M'):
			Mario.lives -= 1
			if Mario.lives<=0:
				return "exit"
			os.system('clear')
			print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\t\t\t\t\tNumber of Mario left:",Mario.lives)
			Mario.respawn(enemy.x,enemy.y)		
			time.sleep(2)

		Board.board[enemy.x][enemy.y]='@'

class Boss(Parent):
	health = 0
	boss_ = boss_ = ['B','O','S','0']
	def __init__(self):
		self.boss_x = random.randint(11,32)
		self.boss_y = Board.prev_k-15

		Board.board[13,420:451]='/'
		Board.board[21,420:451]='/'
		Board.board[28,420:451]='/'
		Board.board[35,415]='E'
		Board.board[35,495]='E'

		for i in range(6,38):
			for j in range(Board.prev_j,Board.prev_k):
				if Board.board[i][j] in Boss.boss_:
					Board.board[i][j]=' '

		for i in range(self.boss_x-4,self.boss_x):
			Board.board[i][self.boss_y]='B'

		for i in range(self.boss_x-4,self.boss_x):
			Board.board[i][self.boss_y+1]='O'
			
		for i in range(self.boss_x-4,self.boss_x):
			Board.board[i][self.boss_y+2]='S'	

		for i in range(self.boss_x-4,self.boss_x):
			Board.board[i][self.boss_y+3]='S'	

	def attack_mario(self):
		"""attack function for boss"""
		if Boss.attack:
			Board.board[self.boss_x-2][self.boss_y-1]='<'
			Boss.bullets.append([self.boss_x-2,self.boss_y-1])

	def shoot():
		for bullet in Boss.bullets:
			x = bullet[0]
			y = bullet[1]

			if Board.board[x][y-1]=='M':
				Board.board[x][y]=' '
				Mario.lives -= 1
				Board.board[35][410]='M'		
				Board.board[x][y-1]=' '
				os.system('clear')
				print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\t\t\t\t\tNumber of Mario left:",Mario.lives)
				time.sleep(2)

			elif Board.board[x][y-1] in pass_through:
				Board.board[x][y]=' '
				Boss.bullets.remove(bullet)

			else:
				Board.board[x][y]=' '
				Board.board[x][y-1]='<'
				bullet[1]-=1


class Mario(Parent):
	lives = 3
	score = 0
	bonus = 0

	def __init__(self):
		self.x = 35
		self.y = 10
		Board.board[self.x][self.y] = 'M'

	def remove_enemy():
		for en in Enemy.enemies:
			en.x=' '
			en.y=' '
		Enemy.enemies = []

	def _get_coordinates(x,y,z):
		"""function to get coordinates of mario in a given frame"""
		temp = Board.board
		temp1 = temp=='M'
		for i in range(6,x):
			for j in range(y,z):
				if(temp1[i][j]==True):
					current_x = i
					current_y = j

		return current_x,current_y

	def attack_enemy():
		"""attack boss"""
		if Mario.attack:
			x,y = Mario._get_coordinates(Board.prev_i,Board.prev_j,Board.prev_k)
			Board.board[x][y+1]='>'
			Mario.bullets.append([x,y+1])

	def bullet_move():
		for bullet in Mario.bullets:
			x = bullet[0]
			y = bullet[1]
			if Board.board[x][y+1] in pass_through:
				Board.board[x][y]=' '
				Mario.bullets.remove(bullet)

			elif Board.board[x][y+1]=='B':
				Mario.bonus+=150
				Board.board[x][y]=' '
				Mario.bullets.remove(bullet)
				Boss.health -= 20
			else:
				Board.board[x][y]=' '
				Board.board[x][y+1]='>'
				bullet[1]+=1

	def _pass(x,y):
		flag = 0
		if (x,y) in Board.triangle:
			Board.board[x][y]='.'
			flag = 1
		elif (x,y) in Board.underscore:
			Board.board[x][y]='_'
			flag = 1
		elif (x,y) in Board.close_:
			Board.board[x][y]=')'
			flag = 1 
		elif (x,y) in Board.open_:
			Board.board[x][y]='('	
			flag = 1
		else:
			Board.board[x][y]=' '

		return flag

	def respawn(x,y):
		"""respawning enemy after it dies"""
		pos = Board.prev_j+1
		while pos<y:
			if (Board.board[x][pos]==' ' or Board.board[x][pos]=='.') and Board.board[x+1][pos]!='-':
				Board.board[x][pos]='M'
				break
			pos+=1

	def _move_forward(self):
		"""move forward fo mario"""
		self.x,self.y = Mario._get_coordinates(Board.prev_i,Board.prev_j,Board.prev_k)
		if(self.y<=798):
			self.y = self.y+1
			if Board.board[self.x][self.y]=='0':
				Mario.score += 1
				Mario._pass(self.x,self.y-1)
				Board.board[self.x][self.y]='M'

			elif Board.board[self.x][self.y]=='P':
				Mario.lives+=1
				Mario._pass(self.x,self.y-1)
				Board.board[self.x][self.y]='M'
				call(["aplay","-q","smb_1-up.wav"])

			elif Board.board[self.x][self.y]=='A':
				Mario._pass(self.x,self.y-1)
				Board.board[self.x][self.y]='M'
				Mario.attack = 1
				call(["aplay","-q","smb_powerup.wav"])

			elif Board.board[self.x][self.y]=='@':
				Mario._pass(self.x,self.y-1)
				Mario.lives-=1
				call(["aplay","-q","smb_mariodie.wav"])
				if Mario.lives<=0:
					call(["aplay","-q","smb_gameover.wav"])
					return "exit"
				os.system('clear')
				print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\t\t\t\t\t\tNumber of Mario left",Mario.lives)
				Mario.respawn(self.x,self.y)
				time.sleep(2)
				init_board(Board.prev_i,Board.prev_j,Board.prev_k)

			elif(Board.board[self.x][self.y]=='/'):
				Mario._pass(self.x,self.y-1)
				Board.board[self.x-1][self.y]='M'

			elif Board.board[self.x][self.y]=='I':
				Mario._pass(self.x,self.y-1)
				call(["aplay","-q","smb_stage_clear.wav"])
				Board.bonus_round()

			elif Board.board[self.x][self.y]=='K':
				Mario._pass(self.x,self.y-1)
				call(["aplay","-q","smb_stage_clear.wav"])
				enemy.boss_round()

			elif(Board.board[self.x][self.y] in obstacles):
				Mario._pass(self.x,self.y-1)
				Board.board[self.x][self.y-1]='M'

			elif((Board.board[self.x+1][self.y-1]=='/' or Board.board[self.x+1][self.y-1]=='T') and Board.board[self.x+1][self.y]==' '):
				Mario._pass(self.x,self.y-1)
				Board.board[self.x][self.y+1]='M'
				Mario.go_down(self)
			else:
				Mario._pass(self.x,self.y-1)
				Board.board[self.x][self.y]='M'

		if( self.y-1 >= ((Board.prev_j+Board.prev_k)/2) ):
			os.system('clear')
			Board.prev_j += 1 
			Board.prev_k += 1
			init_board(Board.prev_i,Board.prev_j,Board.prev_k)
		else:
			os.system('clear')
			init_board(Board.prev_i,Board.prev_j,Board.prev_k)

	def _move_backward(self):
		self.x,self.y = Mario._get_coordinates(Board.prev_i,Board.prev_j,Board.prev_k)
		if(self.y>Board.prev_j):
			self.y = self.y-1
			if Board.board[self.x][self.y]=='0':
				Mario._pass(self.x,self.y+1)
				Mario.score += 1
				Board.board[self.x][self.y]='M'


			if Board.board[self.x][self.y]=='@':
				Mario._pass(self.x,self.y+1)
				Mario.lives-=1
				call(["aplay","-q","smb_mariodie.wav"])
				if Mario.lives<=0:
					call(["aplay","-q","smb_gameover.wav"])
					return
				os.system('clear')
				print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\t\t\t\t\t\tNumber of Mario left",Mario.lives)
				Mario.respawn(self.x,self.y)
				time.sleep(2)
				init_board(Board.prev_i,Board.prev_j,Board.prev_k)

			elif Board.board[self.x][self.y]=='P':
				Mario.lives+=1
				Mario._pass(self.x,self.y+1)
				Board.board[self.x][self.y]='M'
				call(["aplay","-q","smb_1-up.wav"])

			elif Board.board[self.x][self.y]=='A':
				Mario._pass(self.x,self.y+1)
				Board.board[self.x][self.y]='M'	
				Mario.attack = 1
				call(["aplay","-q","smb_powerup.wav"])

			elif(Board.board[self.x][self.y]=='/'):
				Mario._pass(self.x,self.y+1)
				Board.board[self.x-1][self.y]='M'

			elif(Board.board[self.x][self.y] in obstacles):
				Mario._pass(self.x,self.y+1)
				Board.board[self.x][self.y+1]='M'

			elif((Board.board[self.x+1][self.y+1]=='/' or Board.board[self.x+1][self.y+1]=='T')and Board.board[self.x+1][self.y]==' '):	
				Mario._pass(self.x,self.y+1)
				Board.board[self.x][self.y-1]='M'
				Mario.go_down(self)
			else:
				Mario._pass(self.x,self.y+1)
				Board.board[self.x][self.y]='M'

		os.system('clear')
		init_board(Board.prev_i,Board.prev_j,Board.prev_k)

	def go_up(self):
		"""jump up for mario"""
		self.x,self.y = Mario._get_coordinates(Board.prev_i,Board.prev_j,Board.prev_k)
		Mario._pass(self.x,self.y)
		temp = self.x
		flag = 0
		while(temp>=self.x-8):
			if(Board.board[temp][self.y] in obstacles):
				flag = 1
				temp_x = temp+1
				break
			temp = temp-1

		if(not flag):
			temp_x = self.x-8

		if Board.board[temp_x-1][self.y]=='B':
			new = self.y
			for i in range(new-4,new+5):
				if Board.board[temp_x-1][i]=='B':
					Board.board[temp_x-1][i]='T'
			Mario.bonus+=50
			if self.y==229 or self.y ==230 or self.y==231:
				Board.board[23][230]='P'


		Board.board[temp_x][self.y] = 'M'		
		os.system('clear')
		init_board(Board.prev_i,Board.prev_j,Board.prev_k)

	def go_down(self):
		"""coming down for mario"""
		self.x,self.y = Mario._get_coordinates(Board.prev_i,Board.prev_j,Board.prev_k)
		if(Board.board[self.x+1][self.y]=='@'):
			Mario.bonus += 100
			Board.board[self.x+1][self.y]='M'
			call(["aplay","-q","smb_stomp.wav"])

			for en in Enemy.enemies:
				if en.x==self.x+1 and en.y == self.y:
					Enemy.enemies.remove(en)
			Mario._pass(self.x,self.y)

		elif Board.board[self.x+1][self.y]=='S' or Board.board[self.x+1][self.y]=='E':
			Mario._pass(self.x,self.y)
			Board.board[self.x-25][self.y]='M'

		elif Board.board[self.x+1][self.y]=='P':
			Mario.lives+=1
			Mario._pass(self.x,self.y)
			Board.board[self.x+1][self.y]='M'
			call(["aplay","-q","smb_1-up.wav"])

		elif Board.board[self.x+1][self.y]=='A':
			Mario.attack=1
			Board.board[self.x][self.y]=' '
			Board.board[self.x+1][self.y]='M'
			call(["aplay","-q","smb_powerup.wav"])						

		elif Board.board[self.x+1][self.y]=='-':
			Mario._pass(self.x,self.y)
			Mario.lives -= 1
			call(["aplay","-q","smb_mariodie.wav"])
			if Mario.lives<=0:
				call(["aplay","-q","smb_gameover.wav"])
				return "exit"
			minimum = 500
			os.system('clear')
			Board.board[self.x][self.y]=' '
			print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\t\t\t\t\t\tNumber of Mario left:",Mario.lives)
			for gaps in Board.gap:
				if self.y-gaps>=0:
					if self.y-gaps < minimum:
						minimum = self.y - gaps
						temp_space = gaps

			Board.board[35][temp_space-3]='M'
			time.sleep(2)


		elif Board.board[self.x+1][self.y]=='0':
			Mario._pass(self.x,self.y)
			Mario.score+=1
			Board.board[self.x+1][self.y]='M'

		elif Board.board[self.x+1][self.y]=='/' or Board.board[self.x+1][self.y]=='<':
			Board.board[self.x][self.y]='M'

		elif Board.board[self.x+1][self.y] not in obstacles:
			Mario._pass(self.x,self.y)
			Board.board[self.x+1][self.y]='M'

		os.system('clear')
		init_board(Board.prev_i,Board.prev_j,Board.prev_k)