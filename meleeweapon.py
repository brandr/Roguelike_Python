""" A weapon meant for melee. However, it may still have a range greater than 1 tile
	(if it is a halberd, for instance.)
"""

from weapon import *

class MeleeWeapon(Weapon):
	""" MeleeWeapon( ... ) -> MeleeWeapon

	A weapon specifically meant for melee, inherting
	from more general weapons (which may be ranged or melee).

	Attributes:
	(all inherited from Weapon)
	"""

	def __init__(self, name):
		Weapon.__init__(self, name)
