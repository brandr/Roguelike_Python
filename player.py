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
		self.move_delay = 4

	def current_symbol(self):
		return PLAYER_SYMBOL

	def color(self):
		return PLAYER_COLOR

	def temp_move(self, direction):
		#TODO: once movement flowcharts are done, replace this method with better ones.
		coords = self.coordinates()
		dest_coords = (coords[0] + direction[0], coords[1] + direction[1])
		if(self.current_level.valid_tile(dest_coords[0], dest_coords[1])):
			self.begin_player_action(self.move_to, dest_coords ,self.move_delay) #consider an Action class.
		self.end_turn()

	def begin_player_action(self, action, arg, delay):
		#TODO: don't execute right away
		self.current_level.enqueue_player_action(action, arg, delay)