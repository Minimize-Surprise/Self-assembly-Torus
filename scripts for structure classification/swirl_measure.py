import matplotlib.pyplot as plt
import matplotlib 
plt.rcParams.update({'figure.max_open_warning': 0})
import os 
from collections import OrderedDict
import numpy as np
import sys 
import math 


def adaptYPos(y):
	if y >= grid[1]:
		return y - grid[1]
	elif y < 0:
		return y + grid[1]
	else:
		return y 


def adaptXPos(x):
	if x >= grid[0]:
		return x - grid[0]
	elif x < 0:
		return x + grid[0]
	else:
		return x  


def measure_swirls(file, timesteps="500"):
	global grid
	global agents 
	global none 

	pos = []
	p_all = []
	pos_all = []

	f = open(file, 'r')

	# read in file with agent positions 
	for line in f: 	
		# store generation number 
		if line[:4] == "Gen:":
			gen = int(line[5:].rstrip())

		elif line[:5] == "Grid:":
			row = line[6:].split(', ')
			grid = [int(row[0]), int(row[1].rstrip())]

		elif line[:7] == "Agents:":
			agents = int(line[8:].rstrip())

		elif line[:len(timesteps)] != timesteps: # do nothing as long as time step not last time step 
			continue 

		elif line.split(): 
			row = line.split(': ') # first split
			p = row[1].split(', ')
			# array to be modified with all agents 
			pos.append([[int(p[0]), int(p[1])], [int(p[2]), int(p[3])]])
			# array with all agents w/o headings 
			p_all.append([int(p[0]), int(p[1])])
			# array with all agents (not to be modified)
			pos_all.append([[int(p[0]), int(p[1])], [int(p[2]), int(p[3])]])

	swirl = []
	none = [] 
	index = None 
	index2 = None 
	index3 = None 


	while pos: 
		# options to have a swirl --> one agent in front of current agent 
		# this agent points in different direction 

		# agent in heading direction of tested agent
		if [adaptXPos(pos[0][0][0]+pos[0][1][0]), adaptYPos(pos[0][0][1]+pos[0][1][1])] in p_all:
			# find agent in pos list 
			try:
				index = pos.index([[adaptXPos(pos[0][0][0]+pos[0][1][0]), adaptYPos(pos[0][0][1]+pos[0][1][1])], [-1*pos[0][1][1], -1*pos[0][1][0]]])
			except ValueError:
				#print("Your error message")
				try: 
					index = pos.index([[adaptXPos(pos[0][0][0]+pos[0][1][0]), adaptYPos(pos[0][0][1]+pos[0][1][1])], [pos[0][1][1], pos[0][1][0]]])
				except ValueError:
					pass

			if index is not None: 

				try: 
					index2 = pos.index([[adaptXPos(pos[index][0][0]+pos[index][1][0]), adaptYPos(pos[index][0][1]+pos[index][1][1])], [-1*pos[0][1][0], -1*pos[0][1][1]] ])
				except ValueError:
					pass

				try: 
					index3 = pos.index([[adaptXPos(pos[0][0][0]+pos[index][1][0]), adaptYPos(pos[0][0][1]+pos[index][1][1])], [-1*pos[index][1][0], -1*pos[index][1][1]] ])
				except ValueError:
					pass

		
		if index is None or index2 is None or index3 is None: 
			none.append(pos[0])	
		else:

			# check for neighborhod around structure. allow only one "out of range" neighbor
			check = 0 

			min_x = min(pos[0][0][0], pos[index][0][0], pos[index2][0][0], pos[index3][0][0])
			if(min_x == 0 and max(pos[0][0][0], pos[index][0][0], pos[index2][0][0], pos[index3][0][0]) != 1):
				min_x = max(pos[0][0][0], pos[index][0][0], pos[index2][0][0], pos[index3][0][0])
			min_y = min(pos[0][0][1], pos[index][0][1], pos[index2][0][1], pos[index3][0][1])
			if(min_y == 0 and max(pos[0][0][1], pos[index][0][1], pos[index2][0][1], pos[index3][0][1]) != 1):
				min_y = max(pos[0][0][1], pos[index][0][1], pos[index2][0][1], pos[index3][0][1])


			# below 
			if [adaptXPos(min_x), adaptYPos(min_y-1)] in p_all:
				check += 1
			if [adaptXPos(min_x+1), adaptYPos(min_y-1)] in p_all:
				check += 1
			if [adaptXPos(min_x-1), adaptYPos(min_y-1)] in p_all:
				check += 1
			if [adaptXPos(min_x+2), adaptYPos(min_y-1)] in p_all:
				check += 1

			# right
			if [adaptXPos(min_x-1), adaptYPos(min_y)] in p_all:
				check += 1
			if [adaptXPos(min_x-1), adaptYPos(min_y+1)] in p_all:
				check += 1
			if [adaptXPos(min_x-1), adaptYPos(min_y+2)] in p_all:
				check += 1

			# left 
			if [adaptXPos(min_x+2), adaptYPos(min_y)] in p_all:
				check += 1
			if [adaptXPos(min_x+2), adaptYPos(min_y+1)] in p_all:
				check += 1
			if [adaptXPos(min_x+2), adaptYPos(min_y+2)] in p_all:
				check += 1

			# top 
			if [adaptXPos(min_x), adaptYPos(min_y+2)] in p_all:
				check += 1
			if [adaptXPos(min_x+1), adaptYPos(min_y+2)] in p_all:
				check += 1 

			if check > 1: 
				none.append(pos[0])
				none.append(pos[index])
				none.append(pos[index2])
				none.append(pos[index3])

			m = max(index, index2, index3)
			del pos[m]

			if m == index: 
				m = max(index2, index3)
				del pos[m]
				if m == index2: 
					del pos[index3]
				else: 
					del pos[index2]

			elif m == index2: 
				m = max(index, index3)
				del pos[m]
				if m == index: 
					del pos[index3]
				else: 
					del pos[index]

			elif m == index3:
				m = max(index, index2)
				del pos[m]
				if m == index2: 
					del pos[index]
				else: 
					del pos[index2] 

		index = None 
		index2 = None 
		index3 = None 
		del pos[0]


	return none, (float(agents-len(none))/float(agents))

if __name__ == "__main__":

	if len(sys.argv) >= 2:
		file = sys.argv[1]
	else:
		file = 'agent_trajectory'

	print(measure_swirls(file))


