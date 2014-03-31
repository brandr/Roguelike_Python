""" A representation of the player playing the game. The hero that procedurally generated
dungeons deserve.
"""

from tile import *

PLAYER_SYMBOL = '@'
PLAYER_COLOR = Color("#FF0000")


class Player: #TODO: inheritance
	""" Player ( ... ) -> Player

	TODO: docstring
	"""

	def __init__(self): #TODO: args and inheritance
		self.name = "Link"
		self.hit_points = (10, 10)
		self.current_level = None
		self.current_tile = None

	def current_symbol(self):
		return PLAYER_SYMBOL

	def color(self):
		return PLAYER_COLOR

	def coordinates(self):
		return self.current_tile.coordinates()

	def temp_move(self, direction):
		#TODO: once movement flowcharts are done, replace this method with better ones.
		coords = self.coordinates()
		dest_coords = (coords[0] + direction[0], coords[1] + direction[1])
		if(self.current_level.valid_tile(dest_coords[0], dest_coords[1])):
			self.current_tile.remove_being()
			self.current_level.temp_place_being(self, dest_coords[0], dest_coords[1]) #TEMP method

	#TODO: first thing to do is make sure the player can move around on the map and have the camera follow him.