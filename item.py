""" An object that can be held in an inventory (belonging to a tile or to a Being.)
"""

from math import *

MELEE_WEAPON, ARMOR = "MeleeWeapon", "Armor"
DEFAULT_ITEM_SYMBOLS = {ARMOR:'[', MELEE_WEAPON:')'}
EQUIP_STRING = "[E]"
WIELD_STRING = "[W]"

class Item:
	""" Item( ... ) -> Item

	TODO: docstring
	"""
	def __init__(self, name):
		self.name = name #TODO: set name differently once identification is implemented
		self.wielded = False
		self.equipped = False

	def display_name(self, equip_check = False):
		if(equip_check):
			if(self.equipped):
				return self.name + " " + EQUIP_STRING
			if(self.wielded):
				return self.name + " " + WIELD_STRING
		return self.name

	def current_symbol(self):
		class_name = self.__class__.__name__
		return DEFAULT_ITEM_SYMBOLS[class_name]

	def is_equippable(self):
		return False

	def wield_slot(self): #TODO: change if necessary
		return RIGHT_HAND_SLOT

	def equip_slot(self):
		return None

	def equip(self): #not valid for anything but equipment
		pass

	def unequip(self): #not valid for anything but equipment
		pass

	def wield(self):
		self.wielded = True
		self.equipped = False

	def unwield(self):
		self.wielded = False

# slot names.
# TODO: find a way to organize which slots are dependent on which others.
	# ex: cannot change gloves if weapon is cursed, cannot remove chest armor if cloak is cursed, etc.
HEAD_SLOT = "head_slot"
CHEST_SLOT = "chest_slot"
CLOAK_SLOT = "cloak_slot"
LEFT_HAND_SLOT = "left_hand"
RIGHT_HAND_SLOT = "right_hand"
GLOVES_SLOT = "gloves_slot"
FEET_SLOT = "feet_slot"

HUMANOID = "humanoid"
HUMANOID_SLOTS = {
	HEAD_SLOT:None, CHEST_SLOT:None, CLOAK_SLOT:None, LEFT_HAND_SLOT:None, RIGHT_HAND_SLOT:None, GLOVES_SLOT:None, FEET_SLOT:None
}

SLOTS_MAP = {
	HUMANOID:HUMANOID_SLOTS
}

		