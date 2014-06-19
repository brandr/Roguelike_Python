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
		""" c.take_effect( target ) -> None

		The consumable's effect is applied to the target.
		"""
		pass #TODO: implement effects in inherited classes.

	def consume_dose(self):
		""" c.consume_dose( ) -> None

		Reduce the number of "doses" in this consumable.
		NOTE: this is not to be confused with the amount of this consumable in a stack.
		Each individual consumable may be made up of one or more doses.
		When they run out, the stack is decremented by 1.
		We may not want to keep the "dose" system if it dosen't really add to the game.
		"""
		self.doses[0] = max(self.doses[0] - 1, 0)

	def no_doses(self):
		""" c.no_doses( ) -> bool

		check whether this consumable is out of doses.
		"""
		return self.doses[0] <= 0