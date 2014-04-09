""" A monster is a creature in the dungeon, usually hostile to the player.
"""

from being import *

class Monster(Being):
	""" Monster( ... ) -> Monster

	TODO: docstring
	"""
	def __init__(self, name): #TODO: args (first figure out how monsters will be built)
		Being.__init__(self, name)
		self.hit_points = (10, 10) #TEMP
		self.move_delay = 5
		self.attack_delay = 3

	def current_symbol(self):
		return 'M'			#TODO: figure out how monster symbols will be derived

	def decide_next_turn(self):	#TODO: monster AI-based decision-making goes here
		#TODO: may check action queue here. not sure.
		player = self.current_level.player
		if player != None:
			self.melee_pursue(player)

	def melee_pursue(self, target):
		direction = self.direction_towards(target)
		dest_coords = self.coords_in_direction(direction)
		if(self.enemy_in_tile(dest_coords[0], dest_coords[1])):
			new_target = self.current_level.being_in_tile(dest_coords[0], dest_coords[1]) #this may actually be the original target.
			self.temp_monster_attempt_melee_attack(new_target)
		elif(self.current_level.open_tile(dest_coords[0], dest_coords[1])):
			self.begin_move_towards(target)
		else:
			self.execute_action(self.wait, None, 1)

	def begin_move_towards(self, target): #I forget why I gave this its own method
		self.temp_monster_move_towards(target)
		
	def temp_monster_move_towards(self, target): # TODO: replace with a more robust process based on flowchart.
		direction = self.direction_towards(target) #TODO: pathing
		dest_coords = self.coords_in_direction(direction)
		if(self.current_level.open_tile(dest_coords[0], dest_coords[1])):
			self.execute_action(self.move_towards, target, self.move_delay)
		else:		
			self.execute_action(self.wait, None, 1)

		#TEMP
	def temp_monster_attempt_melee_attack(self, being):
		self.execute_action(self.melee_attack, being, self.attack_delay)