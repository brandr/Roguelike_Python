from item import *

class Weapon(Item):
	"""
	Weapon is an abstract class meant for inheritance by
	MeleeWeapon, RangedWeapon, ThrowWeapon, etc. A "proper" weapon that can be wielded by a being.
	(any item can technically be wielded, however.)

	Attributes:
	name (string): a temporary value for the weapon's name. (this is subject to change once identification is implemented.)
	"""

	def __init__(self, name, two_handed = False):
		Item.__init__(self, name)
		self.two_handed = two_handed
		
	def item_category(self):
		return WEAPON
