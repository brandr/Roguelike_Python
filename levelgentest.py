from random import *
'''
An independent module that lets us test level generation ideas on a 2x2 array.
'''

level_size = 20
level_array = [["#" for i in range(level_size)] for j in range(level_size)] #2-D array preserving point adjacency.
level_dict = {1: [-1, 1], 2:[0,1], 3:[1,1],4:[-1,0],6:[1,0],7:[-1,-1],8:[-1,0],9:[1,-1]}

def circle(level_array, a, b, r):
	for i in range(level_size):
		 for j in range(level_size):
			if r > 3:
				if (((i-b)**2)+((j-a)**2)) <= r**2-1:
					level_array[i][j] = '.'
			else:
				if (((i-b)**2)+((j-a)**2)) <= r**2:
					level_array[i][j] = '.'

def line(level_array, x1, y1, x2, y2):
	level_array[x1][y1] = '.'

def tunnel(level_array, x, y): #Completely random tunnel generation, no bias in any direction.
	current_tunnel_location = [6, 6]
	count = 0
	next_array = [1,2,3,4,6,7,8,9]
	while count < 40:
		if y > 0 and x > 0 and nextTo(level_array, x, y) == False:		
			try:			
				level_array[y][x] = '.'
				tempx = x
				tempy = y			
				next = choice(next_array)
				x += level_dict[next][0]
				y += level_dict[next][1]
				while level_array[y][x] =='.':
					x = tempx
					y = tempy
					next = choice(next_array)
					x += level_dict[next][0]
					y += level_dict[next][1]								
			except LookupError:
				y = randint(0,15)
				x = randint(0,15)				
		else:
			y = randint(0,15)
			x = randint(0,15)				
		count += 1

def printLevel(level_array):
	for i in level_array:
		print ""
		for j in i:
			print j,
	
def iround(x):
    """iround(number) -> integer
    Round a number to the nearest integer."""
    return int(round(x) - .5) + (x > 0)

circle(level_array, 6, 7, 7)
printLevel(level_array)
