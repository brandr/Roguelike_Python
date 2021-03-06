""" An object that can be held in an inventory (belonging to a tile or to a Being.)
"""

from math import *
from status import *
from pygame import Color

AMMO, ARMOR, POTION, WEAPON = "Ammo", "Armor", "Potion", "Weapon"
DEFAULT_ITEM_SYMBOLS = {AMMO:'(', ARMOR:'[', POTION:'!', WEAPON:')'}
EQUIP_STRING = "[E]"
WIELD_STRING = "[W]"
DEFAULT_STACK_SIZE = 1

WHITE = Color("#FFFFFF")

class Item:
	""" Item( str, [int, int] ) -> Item

	TODO: docstring

	Attributes:

	name: the name of the item. Subject to change once we implement identification.
	wielded: whether the item is currently wielded by someone.
	equipped: whether the item is currently equipped by someone.
	quantity: how many of this item are is this Item object and how many there can be at maximum.
	material: what this item is made of. Determines damage/protection (if weapon or armor), and what it is damaged by/characteristics of damage if anything else.
	is_artifact: Boolean indicating artifactness. Has to do with brands that can be generated, if its destructible by common means, how valuable it is, etc.
	"""
	def __init__(self, name = None, quantity = [DEFAULT_STACK_SIZE, DEFAULT_STACK_SIZE]): # since name might be derivable from other attributes, it is optional sometimes.
		self.name = name #TODO: set name differently once identification is implemented
		self.wielded = False
		self.equipped = False
		self.quantity = quantity
		self.material = None #Unused field for material
		self.is_artifact = False #Unused field for artifactness
		self.two_handed = False

	def display_name(self, equip_check = False):
		""" i.display_name( bool ) -> str

		The name of this item as it should be displayed for some context.
		The context will affect what equip_check should be set to.
		"""
		display_string = self.name
		if(equip_check):
			if(self.equipped):
				display_string += " " + EQUIP_STRING
			elif(self.wielded):
				display_string += " " + WIELD_STRING
		if self.quantity[0] > 1:
			display_string += " " + "(" + str(self.quantity[0]) + ")"
		return display_string

	def create_copy(self, amount = None):
		""" i.create_copy( int ) -> Item

		Returns a new item that is a copy of this one with the given quantity.
		"""
		if not amount: amount = self.current_quantity()
		return Item(self.name, [amount, DEFAULT_STACK_SIZE])

	def item_category(self):
		""" i.item_category( ) -> str

		Returns the name of this item's class as a string.

		"""
		return self.__class__.__name__

	def current_symbol(self):
		""" i.current_symbol( ) -> char

		Returns the symbol that should be used to display this item onscreen.
		"""
		category = self.item_category()
		return DEFAULT_ITEM_SYMBOLS[category]

	def current_color(self):
		""" i.current_color( ) -> color

		Returns the color that should be used to display this item onscreen.
		"""
		return WHITE #TEMP

	def collide_with_tile(self, tile, player):
		""" i.collide_with_tile( Tile, Player ) -> None

		Perform the proper collision with the given tile (and whatever's in it, if applicable).
		"""
		if tile.current_being:
			#TODO: collide with the being in the tile.
			return
		tile.add_item(self)

	def current_quantity(self):
		""" i.current_quantity( ) -> int

		How many of this item there are.
		"""
		return self.quantity[0]

	def decrement_quantity(self, quantity = 1):
		""" i.decrement_quantity( ) -> None

		Reduces the quantity of this item by the given amount.
		"""
		self.quantity[0] -= quantity

	def is_equippable(self):
		""" i.is_equippable( ) -> None

		Tells whether this item can be equipped.
		Overridden for equipment.
		"""
		return False

	def wield_slot(self): #TODO: change if necessary
		""" i.wield_slot( ) -> str

		Returns a string key saying where this item should be wielded.
		"""
		return RIGHT_HAND_SLOT

	def equip_slot(self):
		""" i.equip_slot( ) -> str

		Returns a string key saying where this item should be equipped.
		"""
		return None

	def equip(self): #not valid for anything but equipment
		pass

	def unequip(self): #not valid for anything but equipment
		pass

	def wield(self):
		""" i.wield( ) -> None

		Some Being wields this item as a weapon.
		"""
		self.wielded = True
		self.equipped = False

	def unwield(self):
		""" i.unwield( ) -> None

		Some Being stops wielding this item as a weapon.
		"""
		self.wielded = False

# slot names.
# TODO: find a way to organize which slots are dependent on which others.
	# ex: cannot change gloves if weapon is cursed, cannot remove chest armor if cloak is cursed, etc.
HEAD_SLOT = "head_slot"
CHEST_SLOT = "chest_slot"
CLOAK_SLOT = "cloak_slot"
RING1_SLOT = "ring1_slot"
RING2_SLOT = "ring2_slot"
LEFT_HAND_SLOT = "left_hand"
RIGHT_HAND_SLOT = "right_hand"
GLOVES_SLOT = "gloves_slot"
FEET_SLOT = "feet_slot"


HUMANOID = "humanoid"
HUMANOID_SLOTS = {
	HEAD_SLOT:None, CHEST_SLOT:None, CLOAK_SLOT:None, RING1_SLOT:None, RING2_SLOT:None, LEFT_HAND_SLOT:None, RIGHT_HAND_SLOT:None, GLOVES_SLOT:None, FEET_SLOT:None
}
HUMANOID_DEPENDENCIES = {
	CHEST_SLOT:[CLOAK_SLOT], GLOVES_SLOT:[RIGHT_HAND_SLOT, LEFT_HAND_SLOT, RING1_SLOT, RING2_SLOT]  #TODO: other dependencies go here (not sure how to handle 1-handed to 2-handed dependencies)
}

SLOTS_MAP = {
	HUMANOID:HUMANOID_SLOTS
}
DEPENDENCIES_MAP = {
	HUMANOID:HUMANOID_DEPENDENCIES
}
