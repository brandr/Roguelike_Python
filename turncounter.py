""" Processes the turns for beings on a level.
"""

from tile import *
from player import * 
from monster import *
from action import *

MAX_DELAY = 99
DEFAULT_DELAY = 1

class TurnCounter:

	""" TurnCounter( ) -> TurnCounter

	The turncounter is held by a level and keeps track of all actors on it,
	including the player, monsters, and status effects. These act in order based on the delays 
	between their actions.

	Attributes:

	turn_count is how much time has passed since this TurnCounter started counting.

	turn_queue is a dict mapping actors to their delays before performing their next actions.

	player is a special, tracked separately from actors in the turn queue.

	player_delay is the time left before the player can act again.
	"""

	def __init__(self):
		self.turn_count = 0
		self.turn_queue = {}
		self.player = None
		self.player_delay = None

	def remove_actor(self, actor):
		""" tc.remove_actor( Being/Status ) -> None

		Removes the actor from the turn queue, preventing it from taking any more actions.
		"""
		if actor in self.turn_queue:
			del(self.turn_queue[actor])

	def enqueue_delay(self, actor, delay):
		""" tc.enqueue_delay( Being/Status, int ) -> None

		Store the delay until the actor's next action can take place.
		"""
		if(actor in self.turn_queue):
			self.turn_queue[actor] += delay
		self.turn_queue[actor] = delay

	def enqueue_player_delay(self, player, delay):
		""" tc.enqueue_player_delay( player, int ) -> None

		Store the delay until the player can act.		
		"""
		if(player == self.player):
			self.player_delay += delay
			return
		self.player = player
		self.player_delay = delay

	def process_turns(self):
		""" tc.process_turns( ) -> None

		Figure out who should act soonest and how long it will take before they act.
		"Fast forward" time that far, have that actor take action, and subtract the time that has just passed
		from all other actors' delays. 
		"""
		lowest_actor = self.player
		lowest_delay = self.player_delay
		for a in self.turn_queue:
			delay = self.turn_queue[a]
			if delay < lowest_delay:
				lowest_actor = a
				lowest_delay = delay
		if lowest_actor == self.player: # case for the player's turn is next
			self.increment_counter(lowest_delay)
			self.decrement_player_turn_delay(lowest_delay) #TEMP (not sure this is right)
			self.decrement_turn_delays(lowest_delay)
			self.player.decide_next_turn()
			return
		else:				   			# case for a monster's turn is next
			del self.turn_queue[lowest_actor]
			self.increment_counter(lowest_delay)
			self.decrement_player_turn_delay(lowest_delay)
			self.decrement_turn_delays(lowest_delay)
			lowest_actor.decide_next_turn()
			self.process_turns()

	def lowest_non_player_delay(self):
		""" tc.lowest_non_player_delay( ) -> int

		Returns the amount of time before something besides the player can act.
		"""
		lowest_delay = MAX_DELAY
		for a in self.turn_queue:
			delay = self.turn_queue[a]
			if delay < lowest_delay:
				lowest_delay = delay
		if lowest_delay == MAX_DELAY:
			return 0
		return lowest_delay

	def decrement_turn_delays(self, dec_value):
		""" tc.decrement_turn_delays( int ) -> None

		Decrease all turn delays (except the player's) by the given value.
		"""
		for a in self.turn_queue:
			self.turn_queue[a] -= dec_value

	def decrement_player_turn_delay(self, dec_value):
		""" tc.decrement_player_turn_delay( int ) -> None

		Decrease the player's turn delay by the given value.
		"""
		self.player_delay -= dec_value

	def increment_counter(self, time):
		""" tc.increment_counter( int ) -> None

		Increment the counter by the given amount of time.
		"""
		self.turn_count += time