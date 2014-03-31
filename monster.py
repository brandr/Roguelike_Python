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
		self.move_delay = 6

	def current_symbol(self):
		return 'M'			#TODO: figure out how monster symbols will be derived

	def decide_next_turn(self):
		player = self.current_level.player
		if player != None:
			self.move_towards(player)

	def move_towards(self, target):
		direction = self.direction_towards(target) #TODO: pathing
		dest_coords = self.coords_in_direction(direction)
		self.temp_monster_move_to(dest_coords)
		
	def temp_monster_move_to(self, coords): # TODO: replace with a more robust process based on flowchart.
		if(self.current_level.open_tile(coords[0], coords[1])):
			self.begin_action(self.move_to, coords, self.move_delay) #consider an Action class.
		else:		
			self.begin_action(self.wait, None, 2)