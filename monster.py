""" A monster is a creature in the dungeon, usually hostile to the player.
"""

from being import *

class Monster(Being):
	""" Monster( ... ) -> Monster

	TODO: docstring
	"""
	def __init__(self, name): #TODO: args (first figure out how monsters will be built)
		Being.__init__(self, name)

	def current_symbol(self):
		return 'M'			#TODO: figure out how monster symbols will be derived