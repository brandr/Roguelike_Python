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
		#self.action_queue = []
		self.turn_queue = {}
		#self.player_action = None
		#self.player_delay_counter = None
		self.player = None
		self.player_delay = None

	#def enqueue_action(self, actor, action, arg, delay):
	#	queue_action = Action(actor, action, arg, delay)
	#	self.action_queue.append(queue_action)
	def enqueue_delay(self, actor, delay):
		self.turn_queue[actor] = delay

	#def enqueue_player_action(self, player, action, arg, delay):
	#	self.player_action = Action(player, action, arg, delay)
	def enqueue_player_delay(self, player, delay):
		#self.player_delay_counter = (player, delay)
		self.player, self.player_delay = player, delay

	def process_turns(self):
		#lowest_action = self.player_action
		lowest_actor = self.player
		lowest_delay = self.player_delay
		#lowest_index = -1 	   # represents player index
		for a in self.turn_queue:
			delay = self.turn_queue[a]
			if delay < lowest_delay:
				lowest_actor = a
				lowest_delay = delay
		#for i in range (len(self.turn_queue)):
		#	a = self.action_queue[i]
		#	if a.delay < lowest_action.delay:
		#		lowest_action = a
		#		lowest_index = i 
		if lowest_actor == self.player: # case for the player's turn is next
			self.decrement_turn_delays(lowest_delay)
			#self.process_player_turn(lowest_action)
		else:				   # case for a monster's turn is next
			#self.turn_queue.remove(lowest_action)
			del self.turn_queue[lowest_actor]
			self.decrement_player_turn_delay(lowest_delay)
			self.decrement_turn_delays(lowest_delay)
			lowest_actor.decide_next_turn()
			#self.process_turn(lowest_action)
			self.process_turns()

	def decrement_turn_delays(self, dec_value):
		for a in self.turn_queue:
			self.turn_queue[a] -= dec_value

	def decrement_player_turn_delay(self, dec_value):
		self.player_delay -= dec_value

	def process_player_turn(self, player_action):
		self.turn_count += player_action.delay
		player_action.execute()

	#def process_turn(self, action):
	#	self.turn_count += action.delay
	#	action.execute()
	#	action.actor.decide_next_turn() #decide 
