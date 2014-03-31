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
		self.action_queue.append[queue_action]

	def enqueue_player_action(self, player, action, arg, delay):
		self.player_action = Action(player, action, arg, delay)
		#being.execute_action(action, arg)	#TODO: not right away

	def process_turns(self):
		#if(self.player_action != None): #TODO: might want a case for None player action
		lowest_action = self.player_action
		lowest_index = -1 # represents player index
		for i in range (len(self.action_queue)):
			a = action_queue[i]
			if a.delay < lowest_action.delay:
				lowest_action = a
				lowest_index = i 
		if lowest_index == -1:
			self.process_player_turn(lowest_action)
		else:
			pass
			#TODO


	def process_player_turn(self, player_action):
		self.turn_count += player_action.delay
		player_action.execute()
