""" A protective item which a Being may be able to equip (if it fits).
"""

from equipment import *

class Armor(Equipment):
	""" Armor( str, str ) -> Armor

	An armor corresponds to a specific slot, which we will likely
	keep track of using a dictionary.

	Attributes:
	name, slot: Both inherited from Equipment.

	"""

	def __init__(self, name, slot):
		Equipment.__init__(self, name, slot)

	def item_category(self):
		""" a.item_category( ) -> str

		Through method overriding, some broader item type can be identified as armor this way.
		"""
		return ARMOR
		