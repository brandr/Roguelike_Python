""" Parses keyboard input and passes it to various components of the game for 
	processing.
"""

from level import *
import pygame
class Controls:
	""" Controls( ... ) -> Controls

		TODO: docstring

	"""
	def __init__(self, player):
		self.player = player

	def process_event(self, e):
		if e.type == QUIT:
                        pygame.quit()
		#if e.type != KEYDOWN and e.type != KEYUP:
		#	return
		if e.type == KEYDOWN:
			if e.key in(CONTROL_MAP):
				action = CONTROL_MAP[e.key]
				action(self, e.key)

	def move_input(self, key):
		if(key in DIRECTION_MAP):
			direction = DIRECTION_MAP[key]
			self.player.temp_move(direction) #TEMP METHOD

move = Controls.move_input

CONTROL_MAP = { 
	K_UP:move, K_DOWN:move, K_LEFT:move, K_RIGHT:move,

	K_KP1:move, K_KP2:move, K_KP3:move, K_KP4:move, K_KP5:move,
	K_KP6:move, K_KP7:move, K_KP8:move, K_KP9:move #TODO
}

DIRECTION_MAP = {
	K_UP:(0, -1), K_DOWN:(0, 1), K_LEFT:(-1, 0), K_RIGHT:(1,0),

	K_KP1:(-1, 1), K_KP2:(0, 1), K_KP3:(1, 1), K_KP4:(-1, 0), K_KP5:(0, 0), #TODO
	K_KP6:(1, 0), K_KP7:(-1, -1), K_KP8:(0, -1), K_KP9:(1, -1)
} #TODO
