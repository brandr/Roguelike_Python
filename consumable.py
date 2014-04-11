""" Something the player may eat/drink.
"""

from item import *

class Consumable(Item):
	""" Consumable( int, int ) -> Consumable

	An abstract class to be inherited by Potion, Food, and possibly others.

	Attributes:
	dose_count: the amount of times this object may be consumed before it runs out.
	consume_time: the time it takes to conusme each dose.
	"""

	def __init__(self, name = None, quantity = [DEFAULT_STACK_SIZE, DEFAULT_STACK_SIZE], dose_count = 1, consume_time = 1):
		Item.__init__(self, name, quantity)
		self.doses = [dose_count, dose_count]
		self.consume_time = consume_time

	def take_effect(self, target):
		pass #TODO: implement effects in inherited classes.

	def consume_dose(self):
		self.doses[0] = max(self.doses[0] - 1, 0)

	def no_doses(self):
		return self.doses[0] <= 0