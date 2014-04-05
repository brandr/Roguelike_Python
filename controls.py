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
		self.control_manager = None

	def process_event(self, event): #abstract method, to be inherited from by subclasses
		if event.type == QUIT: raise(SystemExit)
		if event.type == KEYDOWN:
			if event.key in(self.control_map):
				action = self.control_map[event.key]
				action(self, event.key)

	def exit_to_main_game_screen(self, key):
		self.control_manager.exit_to_main_game_screen(self.player)

LETTER_TO_KEY_MAP = {
	'a':K_a, 'b':K_b, 'c':K_c, 'd':K_d, 'e':K_e, 'f':K_f, 'g':K_g, 'h':K_h, 'i':K_i, 'j':K_j, 'k':K_k, 'l':K_l, 'm':K_m,
	'n':K_n, 'o':K_o, 'p':K_p, 'q':K_q, 'r':K_r, 's':K_s, 't':K_t, 'u':K_u, 'v':K_v, 'w':K_w, 'x':K_x, 'y':K_y, 'z':K_z #TODO: figure out how to handle captial letters.
	#'A':K_A, 'B':K_B, 'C':K_C, 'D':K_D, 'E':K_E, 'F':K_F, 'G':K_G, 'H':K_H, 'I':K_I, 'J':K_J, 'K':K_K, 'L':K_L, 'M':K_M,
	#'N':K_N, 'O':K_O, 'P':K_P, 'Q':K_Q, 'R':K_R, 'S':K_S, 'T':K_T, 'U':K_U, 'V':K_V, 'W':K_W, 'X':K_X, 'Y':K_Y, 'Z':K_Z
} 

KEY_TO_LETTER_MAP = {
	K_a:'a', K_b:'b', K_c:'c', K_d:'d', K_e:'e', K_f:'f', K_g:'g', K_h:'h', K_i:'i', K_j:'j', K_k:'k', K_l:'l', K_m:'m',
	K_n:'n', K_o:'o', K_p:'p', K_q:'q', K_r:'r', K_s:'s', K_t:'t', K_u:'u', K_v:'v', K_w:'w', K_x:'x', K_y:'y', K_z:'z' #TODO: figure out how to handle captial letters.
}