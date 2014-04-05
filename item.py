""" An object that can be held in an inventory (belonging to a tile or to a Being.)
"""

from math import *

MELEE_WEAPON, ARMOR = "MeleeWeapon", "Armor"
DEFAULT_ITEM_SYMBOLS = {ARMOR:'[', MELEE_WEAPON:')'}

class Item:
	""" Item( ... ) -> Item

	TODO: docstring
	"""
	def __init__(self, name):
		self.name = name #TODO: set name differently once identification is implemented

	def display_name(self):
		return self.name

	def current_symbol(self):
		class_name = self.__class__.__name__
		return DEFAULT_ITEM_SYMBOLS[class_name]

		