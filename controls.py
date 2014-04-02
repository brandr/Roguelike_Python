""" Parses keyboard input and passes it to various components of the game for 
	processing.
"""

from level import *

class Controls:
	""" Controls( ... ) -> Controls

		An abstract class for translating key presses into actions.

		Attributes:

		control_map: a dict of key inputs to methods.

	"""

	def __init__(self): #, player):
		self.control_map = None #TODO: add things to this class that aren't specific to the maingamecontrols.

	def process_event(self, event): #abstract method, to be inherited from by subclasses
		if event.type == QUIT: raise(SystemExit)
		if event.type == KEYDOWN:
			if event.key in(self.control_map):
				action = self.control_map[event.key]
				action(self, event.key)