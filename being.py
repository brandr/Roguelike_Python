""" A being is a more general version of a player or monster.
"""

from tile import *

class Being:
	""" Being( ... ) -> Being

	Only one being can occupy a tile at a time.

	TODO: docstring
	"""
	def __init__(self, name):
		self.name = name
		self.current_level = None
		self.current_tile = None

	def coordinates(self):
		return self.current_tile.coordinates()

	def begin_action(self, action, arg, delay):
		#TODO: don't execute right away
		self.current_level.enqueue_action(self, action, arg, delay)

	def execute_action(self, action, arg):
		action(arg)

	def move_to(self, dest_coords):
		self.current_tile.remove_being()
		self.current_level.temp_place_being(self, dest_coords[0], dest_coords[1]) #TEMP method		

	def end_turn(self):
		self.current_level.process_turns()