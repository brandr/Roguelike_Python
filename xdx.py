import random

#Rolls XdX dice and returns total score
def xdx(die_count, die_max):
	min = die_count 
	max = die_count*die_max
	total = random.randint(min, max)
	return total

#Rolls XdX dice and returns list of rolled dice
def xdx_list(die_count, die_max):
	count = 1
	die_list = []
	while count <= die_count:
		die_list.append(random.randint(1, die_max))
		count += 1
	return die_list

#Randomly determines whether or not something succeeds based on a
#float percentage given in the argument. 
def percentSuccess(chance):
    roll = random.random()
    if roll <= chance:
        return True
    return False
    
