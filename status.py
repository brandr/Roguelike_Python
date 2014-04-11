""" A status which affects a being with some effect over some duration.
"""

class Status:
	""" Status( ... ) -> Status

	TODO
	"""
	def __init__(self, effect, delay = 1, starting_duration = 1):
		self.effect, self.delay = effect, delay
		self.target = None
		self.remaining_duration = starting_duration

	def take_effect(self):
		self.remaining_duration -= self.delay #assumes that the status does not take effect immediately, but needs to wait for delay time.
		if(self.remaining_duration <= 0):
			self.end_status()
			return
		self.effect(self.target)

	def decide_next_turn(self):
		self.target.take_status_effect(self)

	def end_status(self):
		self.target.remove_status(self)