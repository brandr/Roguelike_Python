""" A "proper" weapon that can be wielded by a being.
	(any item can technically be wielded, however.)
"""

from item import *

class Weapon(Item):
	""" Weapon( ... ) -> Weapon

	Weapon is an abstract class meant for inheritance by
	MeleeWeapon, RangedWeapon, ThrowWeapon, etc.

	Attributes:
	TODO
	"""

	def __init__(self):
		Item.__init__(self)