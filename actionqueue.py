""" A chronologically ordered set of actions that a Being 'plans' to perform.
"""

from action import *

class ActionQueue:
	""" ActionQueue( ... ) -> ActionQueue

	TODO
	"""
	def __init__(self):
		self.actions = []

	def enqueue_action(self, action):
		self.actions.insert(0, action)

	def dequeue_action(self):
		return self.actions.pop()

	def empty(self):
		return len(self.actions) == 0
