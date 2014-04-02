""" Processes the turns for beings on a level.
"""

from tile import *
from player import * 
from monster import *
from action import *

MAX_DELAY = 99

class TurnCounter:

	""" TurnCounter( ) -> TurnCounter

	TODO: docstring
	"""

	def __init__(self):
		self.turn_count = 0
		self.turn_queue = {}
		self.player = None
		self.player_delay = None

	def enqueue_delay(self, actor, delay):
		self.turn_queue[actor] = delay

	def enqueue_player_delay(self, player, delay):
		self.player, self.player_delay = player, delay

	def process_turns(self):
		lowest_actor = self.player
		lowest_delay = self.player_delay
		for a in self.turn_queue:
			delay = self.turn_queue[a]
			if delay < lowest_delay:
				lowest_actor = a
				lowest_delay = delay
		if lowest_actor == self.player: # case for the player's turn is next
			self.increment_counter(lowest_delay)
			self.decrement_turn_delays(lowest_delay)
			return
		else:				   			# case for a monster's turn is next
			del self.turn_queue[lowest_actor]
			self.increment_counter(lowest_delay)
			self.decrement_player_turn_delay(lowest_delay)
			self.decrement_turn_delays(lowest_delay)
			lowest_actor.decide_next_turn()
			self.process_turns()

	def lowest_non_player_delay(self):
		lowest_delay = MAX_DELAY
		for a in self.turn_queue:
			delay = self.turn_queue[a]
			if delay < lowest_delay:
				lowest_delay = delay
		return lowest_delay

	def decrement_turn_delays(self, dec_value):
		for a in self.turn_queue:
			self.turn_queue[a] -= dec_value

	def decrement_player_turn_delay(self, dec_value):
		self.player_delay -= dec_value

	def increment_counter(self, time):
		self.turn_count += time