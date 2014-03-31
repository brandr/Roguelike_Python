""" A solid wall which is generally impassable and unbreakable.
"""

from tile import *

class Wall(Tile):
	""" Wall( ... ) -> Wall

	TODO: docstring
	"""

	def __init__(self, level, x, y):
		Tile.__init__(self, level, x, y)
		self.empty_symbol = DEFAULT_WALL_SYMBOL

	def passable(self):
		return False