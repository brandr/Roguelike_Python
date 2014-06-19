""" Any item that the player can equip, such as armor, rings, amulets, etc.
	Weapons are not considered equipment, because any item can be wielded.
	Shields are considered equipment, however.
"""

from item import *

class Equipment(Item):
	""" Equipment( str, str ) -> Equipment

	An abstract class used as a template for anything that can be [E]quipped by a being.

	Attributes:
	name: inherited from Item.
	slot: a string (to be compared with constants) which represents the equipment slot
		this item belongs in.
	"""

	def __init__(self, name, slot):
		Item.__init__(self, name)
		self.slot = slot

	def is_equippable(self):
		""" e.is_equippable( ) -> bool

		A method that uses overriding to let an item more generally say whether or not
		it is equiment.
		"""
		return True

	def equip_slot(self):
		""" e.equip_slot( ) -> str

		Tells which slot this equipment should be in.
		"""
		return self.slot

	def equip(self):
		""" e.equip( ) -> None

		Equips this item.
		"""
		self.equipped = True

	def unequip(self):
		""" e.unequip( ) -> None

		Unequips this item.
		"""
		self.equipped = False