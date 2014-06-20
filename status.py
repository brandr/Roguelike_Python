""" A status which affects a being with some effect over some duration.
"""

class Status:
	""" Status( Method, int, int ) -> Status

	A lasting effect that affects the Being it applies to in some way.

	Attributes:

	effect is the method that affects the target.

	delay is how often the status applies its effect.

	target is the Being the status applies to.

	remaining_duration is how much longer before the status runs out.
	"""
	def __init__(self, effect, delay = 1, starting_duration = 1):
		self.effect, self.delay = effect, delay
		self.target = None
		self.remaining_duration = starting_duration

	def take_effect(self):
		""" s.take_effect( ) -> None

		The status's effect is applied to its target.
		"""
		self.remaining_duration -= self.delay #assumes that the status does not take effect immediately, but needs to wait for delay time.
		if(self.remaining_duration <= 0):
			self.end_status()
			return
		self.effect(self.target)

	def decide_next_turn(self):
		""" s.decide_next_turn( ) -> None

		This is a general method that Beings (and things that inherit from Being) also call when they are active.
		"""
		self.target.take_status_effect(self)

	def end_status(self):
		""" s.end_status( ) -> None

		The status is removed from its target.
		"""
		self.target.remove_status(self)