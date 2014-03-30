""" A single space on a level in the dungeon.
"""

import pygame
from pygame import *

BLANK_SYMBOL = ' '
EMPTY_TILE_FLOOR_SYMBOL = '·'
TILE_WIDTH = 14		#TEMP, might use font getters instead
TILE_HEIGHT = 16
WHITE = Color("#FFFFFF")
BLACK = Color("#000000")

class Tile:
	""" Tile( ... ) -> Tile

	TODO: docstring

	Attributes:

	TODO
	"""

	def __init__(self, x, y): #TODO: args
		self.empty_symbol = EMPTY_TILE_FLOOR_SYMBOL
		self.empty_color = WHITE
		self.current_being = None
		self.x, self.y = x, y
		# TODO: figure out how to handle a tile's contents, their order, and which symbol should appear on top,
		# along with how to udpade the current symbol properly.

	def current_symbol(self):
		if(self.current_being != None):
			return self.current_being.current_symbol()
		return self.empty_symbol

	def symbol_image(self):
		symbol_char = self.current_symbol()
		font = pygame.font.Font(None, 12) 	#TODO: consider making this a constant somewhere, or an arg.
		symbol_image = font.render(symbol_char, 0, WHITE)
		return symbol_image

	def set_being(self, being):
		self.current_being = being
		being.current_tile = self

	def remove_being(self):
		self.current_being.current_tile = None
		self.current_being = None

	def coordinates(self):
		return (self.x, self.y)