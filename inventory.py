""" A set of items held by a Being or a Tile.
"""

from equipment import *
from meleeweapon import *

class Inventory:
	""" Inventory( ... ) -> Inventory

	TODO: docstring

	Attributes:
	"""

	def __init__(self):
		self.items = [] #TODO: find a better way to store than a list if it proves useful.

	def add_item(self, item):
		self.items.append(item)

	def empty(self):
		return(not self.items)

	def top_item(self):
		if(not self.empty()):
			return self.items[-1]
		return None