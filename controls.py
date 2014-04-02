""" Parses keyboard input and passes it to various components of the game for 
	processing.
"""

from level import *

class Controls:
	""" Controls( ... ) -> Controls

		TODO: docstring

	"""

	def __init__(self, player):
		self.player = player

	def process_event(self, e):
		if e.type == QUIT: raise(SystemExit)
		if e.type == KEYDOWN:
			if e.key in(CONTROL_MAP):
				action = CONTROL_MAP[e.key]
				action(self, e.key)

	def move_input(self, key):
		if(key in DIRECTION_MAP):
			direction = DIRECTION_MAP[key]
			self.player.temp_move(direction) #TEMP METHOD

	def wait(self, key): #the key arg not necessary for this method, but just for program compilation.
		wait_time = self.player.lowest_non_player_delay() + 1
		self.player.begin_wait(wait_time)

	def pick_up(self, key):
		self.player.attempt_pick_up()

move = Controls.move_input
wait = Controls.wait
pick_up = Controls.pick_up

CONTROL_MAP = { 
	K_UP:move, K_DOWN:move, K_LEFT:move, K_RIGHT:move,			# arrow keys

	K_KP1:move, K_KP2:move, K_KP3:move, K_KP4:move, K_KP5:move,	# numpad keys (might change 5 at some point)
	K_KP6:move, K_KP7:move, K_KP8:move, K_KP9:move,

	K_PERIOD:wait,

	K_COMMA:pick_up
}

DIRECTION_MAP = {
	K_UP:(0, -1), K_DOWN:(0, 1), K_LEFT:(-1, 0), K_RIGHT:(1,0),

	K_KP1:(-1, 1), K_KP2:(0, 1), K_KP3:(1, 1), K_KP4:(-1, 0), K_KP5:(0, 0), #TODO
	K_KP6:(1, 0), K_KP7:(-1, -1), K_KP8:(0, -1), K_KP9:(1, -1)
} #TODO