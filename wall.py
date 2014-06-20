""" A solid wall which is generally impassable and unbreakable.
"""

from tile import *

class Wall(Tile):
	""" Wall( Level, int, int ) -> Wall

	An impassable Tile object that cannot contain anything or allow anything to pass through it.
	"""

	def __init__(self, level, x, y):
		Tile.__init__(self, level, x, y)
		self.empty_symbol = DEFAULT_WALL_SYMBOL

	def passable(self):
		""" w.passable( ) -> bool

		A general Tile method overridden here, since most Tiles are passable but walls are not.
		"""
		return False