'''
# so_long_map_gen.py

Generates a rectangular map, 
n = 'wide' cells, from L to R
n = 'high' cells, from top to bottom

Map will always be enclosed by a surrounding border wall...
IF starting position's coordinates are entered correctly!

# Map legend:
Walls will be '1's.
Empty spaces will be '0's.
Map will contain only one 'P'.
Map will contain only one 'E'.
'E' will be reachable from 'P'.

NOTE.
Map MAY contain at least one, or more 'C's.
Currently hardcoded, to try to add, up to 42, collectibles.
All 'C's will be reachable from 'P'.

Above conditions, tested to work for:
algo_v1() aka "random_digger"

'''

import numpy as np

wide = 25 # L to R
high = 15 # top to bottom
n_collectibles = 42

### START, function definitons ###

'''
# print_map()

Prints the char in each row, col by col
'''
def print_map(a_map):
	for i in range(len(a_map)):
		for j in range(len(a_map[i])):
			if j == len(a_map[i]) - 1:
				print(a_map[i][j], end='\n')
			else:
				print(a_map[i][j], end='')

'''
# init_map()
Takes in 2 arguments: (# of cells)wide, and (# of cells)high.
Returns a 2D array.

NOTE. Map is init~ed to only contain only '1's / walls.
'''
def init_map(wide, high):
	a_map = []
	i = 0
	while i < high:
		a_map.append([]) # add an empty list, to each row of '2D array'
		j = 0
		while j < wide:
			a_map[i].append(1) # fill each row with 1s
			j += 1
		i += 1
	return (a_map)

'''
algo_v1() aka 'random_digger'

Description:
Player, 'P', will start at the top row, but at a random, non-wall column.
Option to specify an alternative pair of starting coordinates.

Random_digger: 
- will randomly choose 1 of 4 cardinal directions (N/S/E/W) to try.
- will stop when it reaches next-to-bottom, row, 
	and make that cell where it stopped at, the exit, 'E'.

NOTE. collectibles are probabilistically added via another function.
	See add_n_collectibles()
'''

def algo_v1(a_map, x=1, y=np.random.randint(1, wide - 2)):
	a_map[x][y] = 'P' # convert starting mapgrid pos, to 'P', for player
	
	while True:
		
		# generate a pair of coordinates, to move to, from starting pos
		testx, testy = (x, y)
		if np.random.uniform() > 0.5: # move along either x-axis or y-axis
			testx = testx + np.random.choice([-1, 1]) # go L or R
		else:
			testy = testy + np.random.choice([-1, 1]) # go down or up
		
		# check if generated coordinates, is within bounds
		# if within bounds, make the cell at those coordinates, an 'empty'
		# when reach 'bottom' of map, make an 'exit'; stop walking
		if testx > 0 and testx < high - 1 and testy > 0 and testy < wide - 1:
			x, y = (testx, testy)
			#print(x, y)
			if a_map[x][y] == 'P':
				continue
			elif a_map[x][y] != 'P':
				a_map[x][y] = 0
			if x == high - 2: # when walker reaches next-to-last row
				a_map[x][y] = 'E' # make the cell the exit, 'E'
				break

'''
algo_v2()

Iterate thru cells in the map
At each cell, decide whether to make either:
the BOTTOM/'south' or RIGHT/'east' cell, '0'

NOTE. WIP 29 Aug 2024
algo_v2() 
was my implementation of "Mazes For Programmers", Part One, binary tree
'''
def algo_v2(a_map):
	a_map[1][1] = 0 # carve out the first empty
	
	tmp_x, tmp_y = (1, 1)
	for i in range(len(a_map)):
		for j in range(len(a_map[i])):
			if np.random.uniform() > 0.5: # Make 'south' cell, '0'
				tmp_x = i + 1
				tmp_y = j
			else: # Make 'east cell '0'
				tmp_x = i
				tmp_y = j + 1
			
			# only make cell at tmp coordinates, '0', if within bounds
			if tmp_x > 0 and tmp_x < high - 1 and tmp_y > 0 and tmp_y < wide - 1:
				a_map[tmp_x][tmp_y] = 0
			
'''
Iterate thru cells in a map,
probabilitistically try to replace '0's with 'C's.

Repeat until n 'C's have been added to the map.
'''
def add_n_collectibles(a_map, n):
	if n == 0:
		print("\n*** WARNING ***\nZERO collectibles will be added!\n")
		exit()
	c_added = 0
	
	for i in range(len(a_map)):
		for j in range(len(a_map[i])):
			if a_map[i][j] == 0 and c_added < n and np.random.randint(1, 10) == 1:
				a_map[i][j] = 'C'
				c_added += 1
	if c_added == 0:
		print("\n*** WARNING ***\nNo collectibles were added!\n")
	#else:
	#	print(f"{n} collectibles were supposed to be added.")
	#	print(f"{c_added} collectibles were ACTUALLY added.")

### END, function definitions ###

if __name__ == '__main__':	
	a_map = init_map(wide, high)
	algo_v1(a_map)
	add_n_collectibles(a_map, n_collectibles)
	print_map(a_map)		

