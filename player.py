""" A representation of the player playing the game. The hero that procedurally generated
dungeons deserve.
"""

from being import *

PLAYER_SYMBOL = '@'
PLAYER_COLOR = Color("#FF0000")


class Player(Being): 
	""" Player ( ... ) -> Player

	TODO: docstring
	"""

	def __init__(self, name): #TODO: args and inheritance
		Being.__init__(self, name)
		self.hit_points = (10, 10)
		self.magic_points = (8, 8)
		self.move_delay = 4

	def current_symbol(self):
		return PLAYER_SYMBOL

	def color(self):
		return PLAYER_COLOR

	def hp_display(self):
		return str(self.hit_points[0]) + "/" + str(self.hit_points[1])

	def mp_display(self):
		return str(self.magic_points[0]) + "/" + str(self.magic_points[1])

	def temp_move(self, direction):
		#TODO: once movement flowcharts are done, replace this method with better ones.
		dest_coords = self.coords_in_direction(direction)
		if(self.current_level.open_tile(dest_coords[0], dest_coords[1])):
			self.begin_player_action(self.move_to, dest_coords ,self.move_delay) #consider an Action class.
			self.end_turn()

	def begin_player_action(self, action, arg, delay):
		#TODO: don't execute right away
		self.current_level.enqueue_player_action(action, arg, delay)