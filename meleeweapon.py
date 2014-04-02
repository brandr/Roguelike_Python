""" A weapon meant for melee. However, it may still have a range greater than 1 tile
	(if it is a halberd, for instance.)
"""

from weapon import *

class MeleeWeapon(Weapon):
	""" MeleeWeapon( ... ) -> MeleeWeapon

	TODO

	Attributes:
	TODO
	"""

	def __init__(self, name):
		Weapon.__init__(self, name)
