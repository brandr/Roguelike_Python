""" A being is a more general version of a player or monster.
"""

from tile import *

DEFAULT_COLOR = Color("#FFFFFF")

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

	def coords_in_direction(self, direction):
		coords = self.coordinates()
		return (coords[0] + direction[0], coords[1] + direction[1])

	def direction_towards(self, target):
		current_coords = self.coordinates()
		target_coords = target.coordinates()
		x_diff = int(target_coords[0] - current_coords[0])
		y_diff = int(target_coords[1] - current_coords[1])
		x_dir = Being.direction_from_diff(x_diff)
		y_dir = Being.direction_from_diff(y_diff)
		return (x_dir, y_dir)

	def current_symbol(self):
		return None

	def color(self):
		return DEFAULT_COLOR

	def begin_action(self, action, arg, delay):
		self.current_level.enqueue_action(self, action, arg, delay)

	def execute_action(self, action, arg):
		action(arg)

	def move_to(self, dest_coords):
		if(self.current_level.open_tile(dest_coords[0], dest_coords[1])):
			self.current_tile.remove_being()
			self.current_level.temp_place_being(self, dest_coords[0], dest_coords[1]) #TEMP method		

	def end_turn(self):
		self.current_level.process_turns()

	def wait(self, arg):
		pass

	@staticmethod
	def direction_from_diff(diff):
		if(diff == 0): return 0
		return (int)(diff/abs(diff))