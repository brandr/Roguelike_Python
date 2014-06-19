""" A chronologically ordered set of actions that a Being 'plans' to perform.
"""

from action import *

class ActionQueue:
	""" ActionQueue( ) -> ActionQueue

	An ordered queue of actions.

	Attributes:

	actions: A List of actions, in order.
	"""
	def __init__(self):
		self.actions = []

	def enqueue_action(self, action):
		"""aq.enqueue_action( Action ) -> None

		Puts this action at the bottom (lowest index) of the queue.
		"""
		self.actions.insert(0, action)

	def dequeue_action(self):
		""" aq.dequeue_action( ) -> Action

		Pops the action at the top (highest index) of the queue.
		"""
		return self.actions.pop()

	def clear(self):
		""" aq.clear( ) -> None

		Removes all actions from the queue.
		"""
		self.actions = []

	def empty(self):
		""" aq.empty( ) -> bool

		Checks whether the queue contains any actions.
		"""
		return len(self.actions) == 0
