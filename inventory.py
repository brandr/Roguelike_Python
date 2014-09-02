""" A set of items held by a Being or a Tile.
"""

from ammo import *
from armor import *
from meleeweapon import *
from potion import *
from selectlist import *

class Inventory:
	""" Inventory( ) -> Inventory

	An Inventory stores items in a list.
	It usually belongs to a Being or Tile.

	Attributes:

	items: a list of items contained in an Inventory.
	"""

	def __init__(self):
		self.items = [] #TODO: find a better way to store than a list if it proves useful.

	def item_select_list(self):
		""" i.item_select_list( ) -> SelectList

		Create a new SelectList so that the player can 
		choose to perform some action on one or more of 
		this inventory's items.
		"""
		return SelectList(Item, self.items)

	def class_item_select_list(self, item_class):
		""" i.class_item_select_list( Class ) -> SelectList

		Create a SelectList, but only containing items of a specific class.
		"""
		items = []
		for i in self.items:
			if isinstance(i, item_class):
				items.append(i)
		return SelectList(Item, items) 

	def equippable_item_select_list(self):
		""" i.equippable_item_select_list( Class ) -> SelectList

		Create a SelectList, but only containing items 
		that can be equipped.
		"""
		items = []
		for i in self.items:
			if i.is_equippable():
				items.append(i)
		return SelectList(Item, items)

	def take_all_items(self):
		""" i.take_all_items( ) -> [Item]

		Remove and return all items contained in this inventory.
		"""
		items = []
		count = self.item_count()
		for i in range(count):
			items.append(self.items.pop())
		return items

	def decrement_item(self, item, quantity = None):
		""" i.decrement_item( Item, int ) -> None

		Decrease the quantity of the given item in this inventory by the given amount, or all if it is none.
		"""
		if not quantity: quantity = item.current_quantity()
		item.decrement_quantity(quantity)
		if(item.current_quantity() <= 0):
			self.remove_item(item)

	def item_at_index(self, index):
		""" i.item_at_index( int ) -> Item

		Returns the item at the given numerical index in this inventory.
		"""
		return self.items[index]

	def add_item_list(self, items):
		""" i.add_item_list( [Item] ) -> None

		Add all items in a list to this inventory.
		"""
		for i in items:
			self.add_item(i)

	def add_item(self, item):
		""" i.add_item( Item ) -> None

		Add an item to this inventory at the end of its list.
		"""
		#TODO: handle stacking here if the item is already in the inventory.
		self.items.append(item)

	def remove_item(self, item):
		""" i.remove_item( Item ) -> None

		Remove an item from this inventory at the end of its list.
		"""
		self.items.remove(item)

	def contains_item_class(self, item_class):
		""" i.contains_item_class( Class ) -> bool

		Check whether this inventory contains an item of the given class.
		"""
		for i in self.items:
			if(isinstance(i, item_class)):
				return True
		return False

	def contains_equippables(self):
		""" i.contains_equippables( ) -> bool

		Check whether this inventory contains equippable items.
		"""
		for i in self.items:
			if(i.is_equippable()):
				return True
		return False

	def empty(self):
		""" i.empty( ) -> bool

		Check whether there are any items in this inventory.
		"""
		return(not self.items)

	def top_item(self):
		""" i.top_item( ) -> Item

		Returns the item at the end of this inventory's list.
		"""
		if(not self.empty()):
			return self.items[-1]
		return None

	def item_count(self):
		""" i.item_count( ) -> None

		Returns the number of items in this inventory.
		"""
		return len(self.items) #TODO: change this if blank item slots must be stored.