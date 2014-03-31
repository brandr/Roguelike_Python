# -*- coding: utf-8 -*-
""" A single space on a level in the dungeon.
"""

import pygame
from pygame import *

BLANK_SYMBOL = ' '
EMPTY_TILE_FLOOR_SYMBOL = u'·'
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

	def __init__(self, level, x, y): #TODO: args
		self.empty_symbol = EMPTY_TILE_FLOOR_SYMBOL
		self.empty_color = WHITE
		self.current_being = None
		self.x, self.y = x, y
		self.level = level
		# TODO: figure out how to handle a tile's contents, their order, and which symbol should appear on top,
		# along with how to udpade the current symbol properly.

	def update(self):
		symbol = self.symbol_image()
		self.level.level_map.blit(symbol, (self.x * TILE_WIDTH, self.y * TILE_HEIGHT))

	def current_symbol(self):
		if(self.current_being != None):
			return self.current_being.current_symbol()
		return self.empty_symbol

	def current_color(self):
		if(self.current_being != None):
			return self.current_being.color()
		return WHITE

	def symbol_image(self):
		symbol_char = self.current_symbol()
		symbol_color = self.current_color()
		font = pygame.font.Font(None, 12) 	#TODO: consider making this a constant somewhere, or an arg.
		symbol_text = font.render(symbol_char, 0, symbol_color)
		symbol_image = Surface((TILE_WIDTH, TILE_HEIGHT))
		symbol_image.blit(symbol_text, (0, 0))
		return symbol_image

	def set_being(self, being):
		self.current_being = being
		being.current_tile = self
		self.update()

	def remove_being(self):
		self.current_being.current_tile = None
		self.current_being = None
		self.update()

	def coordinates(self):
		return (self.x, self.y)