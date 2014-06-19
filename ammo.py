""" An item specifically meant to be used as a projectile.
"""

from item import *

AMMO_STACK_SIZE = 99

class Ammo(Item):
	""" Ammo( ... ) -> Ammo
	TODO: once ammo actually does stuff, complete this docstring.
	"""

	def __init__(self, name = None, count = 1):
		Item.__init__(self, name, [count, AMMO_STACK_SIZE])