""" Parses keyboard input and passes it to various components of the game for
	processing.
"""

from level import *

class Controls:
	""" Controls( ) -> Controls

		An abstract class for translating key presses into actions.

		Attributes:

		control_map: a dict of key inputs to methods.

	"""

	def __init__(self):
		self.control_map = None #TODO: add things to this class that aren't specific to the maingamecontrols.
		self.control_manager = None
		self.player = None

	def initialize_control_map(self, model_map):
		""" c.initialize_control_map( {str:Method} ) -> None

		Using a control dict of pygame key constants to methods, set which key
		presses will have which effects for this control scheme.
		"""
		self.control_map = {}
		for key in model_map:
			self.control_map[key] = model_map[key]

	def process_event(self, event): #abstract method, to be inherited from by subclasses
		""" c.process_event( EVent ) -> None

		Process a keyborad event and execute the associated action.
		"""
		if event.type == QUIT: raise(SystemExit)
		if event.type == KEYDOWN:
			if event.unicode in(self.control_map):
				action = self.control_map[event.unicode]
				action(self, event.unicode)
			elif event.key in(self.control_map):
				action = self.control_map[event.key]
				action(self, event.key)

	def exit_to_main_game_screen(self, key = None):
		""" exit_to_main_game_screen( None ) -> None

		Stop using the current control set and exit to the main game screen.
		"""
		self.player.taking_input_flag = False
		self.control_manager.exit_to_main_game_screen(self.player)

	def exit_to_main_game_controls(self, key = None):
		""" exit_to_main_game_controls( None ) -> None

		Change from this control set to the one used for the main game.
		"""
		self.player.taking_input_flag = False
		self.control_manager.exit_to_main_game_controls(self.player)

#might not use this or the map below. Keeping them just in case.
LETTER_TO_KEY_MAP = {
	'a':K_a, 'b':K_b, 'c':K_c, 'd':K_d, 'e':K_e, 'f':K_f, 'g':K_g, 'h':K_h, 'i':K_i, 'j':K_j, 'k':K_k, 'l':K_l, 'm':K_m,
	'n':K_n, 'o':K_o, 'p':K_p, 'q':K_q, 'r':K_r, 's':K_s, 't':K_t, 'u':K_u, 'v':K_v, 'w':K_w, 'x':K_x, 'y':K_y, 'z':K_z #TODO: figure out how to handle captial letters.
}

KEY_TO_LETTER_MAP = {
	K_a:'a', K_b:'b', K_c:'c', K_d:'d', K_e:'e', K_f:'f', K_g:'g', K_h:'h', K_i:'i', K_j:'j', K_k:'k', K_l:'l', K_m:'m',
	K_n:'n', K_o:'o', K_p:'p', K_q:'q', K_r:'r', K_s:'s', K_t:'t', K_u:'u', K_v:'v', K_w:'w', K_x:'x', K_y:'y', K_z:'z',
	K_RETURN: 'enter'
	 #TODO: figure out how to handle captial letters.
}