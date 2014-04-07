""" A set of items held by a Being or a Tile.
"""

from armor import *
from meleeweapon import *
from selectlist import *

class Inventory:
	""" Inventory( ... ) -> Inventory

	TODO: docstring

	Attributes:
	"""

	def __init__(self):
		self.items = [] #TODO: find a better way to store than a list if it proves useful.

	def item_select_list(self):
		return SelectList(Item, self.items)

	def equippable_item_select_list(self):
		items = []
		for i in self.items:
			if i.is_equippable():
				items.append(i)
		return SelectList(Item, items)

	def item_at_index(self, index):
		return self.items[index]

	def add_item(self, item):
		self.items.append(item)

	def remove_item(self, item):
		self.items.remove(item)

	def contains_equippables(self):
		for i in self.items:
			if(i.is_equippable()):
				return True
		return False

	def empty(self):
		return(not self.items)

	def top_item(self):
		if(not self.empty()):
			return self.items[-1]
		return None

	def item_count(self):
		return len(self.items) #TODO: change this if blank item slots must be stored.