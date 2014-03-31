""" Processes the turns for beings on a level.
"""

from tile import *
from player import * 
from monster import *
from action import *

class TurnCounter:

	""" TurnCounter( ) -> TurnCounter

	TODO: docstring
	"""

	def __init__(self):
		self.turn_count = 0
		self.action_queue = []
		self.player_action = None

	def enqueue_action(self, being, action, arg, delay):
		queue_action = Action(being, action, arg, delay)
		self.action_queue.append(queue_action)

	def enqueue_player_action(self, player, action, arg, delay):
		self.player_action = Action(player, action, arg, delay)
	
	def process_turns(self):
		lowest_action = self.player_action
		lowest_index = -1 # represents player index
		for i in range (len(self.action_queue)):
			a = self.action_queue[i]
			if a.delay < lowest_action.delay:
				lowest_action = a
				lowest_index = i 
		if lowest_index == -1: # case for the player's turn is next
			self.decrement_turn_delays(lowest_action.delay)
			self.process_player_turn(lowest_action)
		else:				   # case for a monster's turn is next
			self.action_queue.remove(lowest_action)
			self.decrement_player_turn_delay(lowest_action.delay)
			self.decrement_turn_delays(lowest_action.delay)
			self.process_turn(lowest_action)
			self.process_turns()

	def decrement_turn_delays(self, dec_value):
		for a in self.action_queue:
			a.delay -= dec_value

	def decrement_player_turn_delay(self, dec_value):
		self.player_action.delay -= dec_value

	def process_player_turn(self, player_action):
		self.turn_count += player_action.delay
		player_action.execute()

	def process_turn(self, action):
		self.turn_count += action.delay
		action.execute()
		action.being.decide_next_turn() #decide 
