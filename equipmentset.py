""" A set of worn and wielded equipment belonging to some Being.
"""

from inventory import *

class EquipmentSet:
	""" EquipmentSet( str ) -> None

	A set of equipment belonging to a Being.
	Composed of a set of slots, each of which may or may not contain a piece of equipment.
	The types of slots depends on the creature's body parts.

	Attributes:

	slots: A set of equipment slots, each of which is set to None if nothing is in it.
	"""
	def __init__(self, slots_key):
		self.slots = None
		if(slots_key in SLOTS_MAP):
			self.initialize_slots(SLOTS_MAP[slots_key])
			
	def initialize_slots(self, slots):
		""" es.initialize_slots( {str:Item} ) -> None

		Using a set of slots from another equipment set,
		fill in the slots for this equipment set.
		"""
		self.slots = {}
		for key in slots:
			self.slots[key] = slots[key]

	def all_items(self):
		""" es.all_items( ) -> [ Item ]

		Return all items contained in this equipment set.
		"""
		items = []
		for key in self.slots:
			item = self.slots[key]
			if item != None:
				items.append(self.slots[key])
		return items

	def remove_all_equipment(self):
		""" es.remove_all_equipment( ) -> None

		Completely empty this equipment set,
		unequipping everything along the way.
		"""
		for key in self.slots:
			item = self.slots[key]
			if item != None:
				item.unwield()
				item.unequip()
				self.slots[key] = None

	def wield_item(self, item): #TODO: this may be structured very differently after the equipment flowchart is figured out
		""" es.wield_item( Item ) -> None

		Wield the given item.
		Note that any item can be wielded, but
		only equipment can be equipped.
		"""
		item.wield()
		self.slots[RIGHT_HAND_SLOT] = item #TODO: may have to change this for non-humanoids that can still wield items.

	def equip_item(self, item):
		""" es.equip_item( Equipment ) -> None

		Equip the item to the proper slot.
		Checks for whether this slot is in this set
		sholud be done before this method is called.
		"""
		item.equip()
		key = item.equip_slot()
		if key in self.slots:
			self.slots[key] = item

	def unwield_item_in_slot(self, key):
		""" es.unwield_item_in_slot( str ) -> None

		Unwield the item in the selected slot.
		This is only to be used for weapons and other
		wieldables-- this will cause problems for
		equipped items.
		"""
		if key in self.slots:
			item = self.slots[key]
			item.unwield()
			self.slots[key] = None

	def unequip_item_in_slot(self, key):
		""" es.unequip_item_in_slot( str ) -> None
		Unequip the item in the selected slot.
		THis is similar to unwield_item_in_slot.
		"""
		if key in self.slots:
			equipment = self.slots[key]
			equipment.unequip()
			self.slots[key] = None

	def item_is_in_slot(self, key):
		""" es.item_is_in_slot( str ) -> bool
		Check whether there is any item in the selected slot.
		"""
		return key in self.slots and self.slots[key] != None

	def get_item_in_slot(self, key):
		""" es.get_item_in_slot( str ) -> Item

		Returns the item in the selected slot,
		assuming something is there.
		"""
		if key in self.slots:
			return self.slots[key]
		return None