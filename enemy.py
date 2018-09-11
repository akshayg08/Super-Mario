import numpy as np 
import os
from board import Board,init_board
import people
import time
import random
from subprocess import call


def boss_round():
	os.system('clear')
	print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\t\t\t\t\t\tBOSS ROUND")
	Board.prev_j = 400
	Board.prev_k = 500

	for i in range(6,36):
		for j in range(Board.prev_j,650):
			Board.board[i][j]=' '

	people.Mario.bullets = []

	Board.board[6:,498:500]='X'
	Board.board[35][Board.prev_j+10]='M'
	people.Boss.attack = 1
	people.Boss.health = 100

	boss = people.Boss()

	time.sleep(3)
	init_board(38,Board.prev_j,Board.prev_k)

def spawn_enemy():
	pos = np.arange(55,399,50)
	for i in pos:
		enemy = people.Enemy(35,i)
		people.Enemy.enemies.append(enemy)

def _move():
	flag = 0
	for enemy in people.Enemy.enemies:
		x = enemy.x
		y = enemy.y

		if Board.board[enemy.x+1][enemy.y]=='-':
			Board.board[enemy.x][enemy.y]=' '
			for en in people.Enemy.enemies:
				if en.x==enemy.x and en.y == enemy.y:
					people.Enemy.enemies.remove(en)

		elif(Board.board[x][y-1] in people.obstacles or Board.board[x+1][y-1]=='-'):
			enemy.hit += 1 
			
		elif(Board.board[x][y+1] in people.obstacles or Board.board[x+1][y+1]=='-'):
			enemy.hit += 1

		elif(Board.board[x][y-1]=='T' and Board.board[x][y+1]=='T'):
			flag = 1

	for enemy in people.Enemy.enemies:
		if(enemy.hit%2==1 and flag == 0):
			if people.Enemy._move_forward(enemy) == "exit":
				return "exit"
		elif(enemy.hit%2==0 and flag == 0):
			if people.Enemy._move_backward(enemy) == "exit":
				return "exit"

	os.system('clear')
	init_board(Board.prev_i,Board.prev_j,Board.prev_k)

def won():
	os.system('clear')
	print("SCORE:",people.Mario.score)
	print("BONUS:",people.Mario.bonus)
	
	print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\t\t\t\t\t\tYour Princess is in another castle.\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
	call(["aplay","-q","smb_world_clear.wav"])
	return "exit"