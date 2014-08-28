""" An item specifically meant to be used as a projectile.
"""

from item import *

MAX_AMMO_STACK_SIZE = 99

class Ammo(Item):
	""" Ammo( ... ) -> Ammo
	TODO: once ammo actually does stuff, complete this docstring.
	"""

	def __init__(self, name = None, count = 1):
		Item.__init__(self, name, [count, MAX_AMMO_STACK_SIZE])

	def create_copy(self, amount = None):
		""" a.create_copy( int ) -> Ammo

		Returns a new ammo that is a copy of this one with the given amount.
		"""
		if not amount: amount = self.current_quantity()
		return Ammo(self.name, amount)