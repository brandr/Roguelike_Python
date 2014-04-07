""" A set of worn and wielded equipment belonging to some Being.
"""

from inventory import *

class EquipmentSet:
	""" EquipmentSet( ... ) -> None

	TODO

	"""
	def __init__(self, slots_key):
		self.slots = None
		if(slots_key in SLOTS_MAP):
			self.slots = SLOTS_MAP[slots_key]

	def wield_item(self, item): #TODO: this may be structured very differently after the equipment flowchart is figured out
		item.wield()
		self.slots[RIGHT_HAND_SLOT] = item #TODO: may have to change this for non-humanoids that can still wield items.

	def unwield_item_in_slot(self, key):
		if key in self.slots:
			item = self.slots[key]
			item.unwield()
			self.slots[key] = None

	def unequip_item_in_slot(self, key):
		if key in self.slots:
			equipment = self.slots[key]
			equipment.unequip()
			self.slots[key] = None

	def item_is_in_slot(self, key):
		return key in self.slots and self.slots[key] != None

	def get_item_in_slot(self, key):
		if key in self.slots:
			return self.slots[key]
		return None