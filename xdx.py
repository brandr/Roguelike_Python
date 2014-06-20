from random import *

"""
Module with functions that simulate rolling dice.
"""

def xdx(die_count, die_max):
	"""
	Rolls a number of N-sided dice.
	Arguments:
		die_count(int): The number of dice to be rolled.
		die_max(int): The maximum number for each die.
	Returns:
		total(int): The sum of the result for all die.
	"""
	minimum = die_count 
	maximum = die_count*die_max
	total = randint(minimum, maximum)
	return total

#Rolls XdX dice and returns list of rolled dice

def xdx_list(die_count, die_max):
	"""
	Rolls a number of N-sided dice.
	Arguments:
		die_count(int): The number of dice to be rolled.
		die_max(int): The maximum number for each die.
	Returns:
		die_list(list of ints): The list of every die result.
	"""
	count = 1
	die_list = []
	while count <= die_count:
		die_list.append(randint(1, die_max))
		count += 1
	return die_list


def random_in_range(minimum, maximum):
	"""
	Returns a random number between minimum and maximum inclusive.
	"""
	return randint(minimum, maximum + 1) # +1 because min and max should be inclusive

#Randomly determines whether or not something succeeds based on a
#float percentage given in the argument. 

def percentSuccess(chance):
	"""
	Given a percentage success chance (a float between zero and one), determines success.
	Returns:
		Boolean with true for success.	
	"""
    roll = random.random()
    if roll <= chance:
        return True
    return False
    
