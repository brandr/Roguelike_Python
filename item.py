""" An object that can be held in an inventory (belonging to a tile or to a Being.)
"""

WEAPON, ARMOR = "Weapon", "Armor"
DEFAULT_ITEM_SYMBOLS = {ARMOR:'[', WEAPON:')'}

class Item:
	""" Item( ... ) -> Item

	TODO: docstring
	"""
	def __init__(self):
		pass #TODO

	def current_symbol(self):
		class_name = self.__class__.__name__
		return DEFAULT_ITEM_SYMBOLS[class_name]

		