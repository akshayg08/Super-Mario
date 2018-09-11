import numpy as np 
import get,signal,time,random  
import os
import people
from board import Board,init_board
import enemy
"""initializing mario"""
mario = people.Mario()
"""initializing enemies"""
enemy.spawn_enemy()


os.system('clear')
init_board(Board.prev_i,Board.prev_j,Board.prev_k)

start = time.time()
start_ = time.time()

def lost():
	os.system('clear')
	print("SCORE:",people.Mario.score)
	print("BONUS:",people.Mario.bonus)
	print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\t\t\t\t\t\tGAME OVER\n\n\n\n\n\n\n\n\n\n\n\n\n\n")

if __name__=='__main__':
	while True:
		"""game"""
		x,y = people.Mario._get_coordinates(Board.prev_i,Board.prev_j,Board.prev_k)

		if mario.go_down() == "exit":
			lost()
			break

		if people.Boss.health<=0 and people.Boss.attack == 1:
			enemy.won()
			break

		if people.Boss.health>0:
			people.Boss.shoot()

		if people.Boss.attack == 1:
			if time.time()-start_>5:
				boss = people.Boss()
				start_ = time.time()
				boss.attack_mario()
		"""get input from terminal"""
		inp = get.get_input()

		if(inp=='q' or mario.lives<=0):
			lost()
			break
		elif(inp=='d'):
			if mario._move_forward()=="exit":
				lost()
				break
		elif(inp=='a'):
			if mario._move_backward()=="exit":
				lost()
				break

		elif(inp=='w'):
			if Board.board[x+1][y] in people.obstacles:
				mario.go_up()


		elif inp=='s':
			people.Mario.attack_enemy()


		if(time.time()-start>=0.2):
			if enemy._move() == "exit":
				lost()
				break
			start = time.time()

		people.Mario.bullet_move()
