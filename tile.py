# -*- coding: utf-8 -*-
""" A single space on a level in the dungeon.
"""

import pygame
from pygame import *
from equipmentset import *

BLANK_SYMBOL = ' '
EMPTY_TILE_FLOOR_SYMBOL = u'·'
DEFAULT_WALL_SYMBOL = 'X'

TILE_WIDTH = 14		#TEMP, might use font getters instead
TILE_HEIGHT = 16
WHITE = Color("#FFFFFF")
BLACK = Color("#000000")
RED = Color("#FF0000")
GREEN = Color("#00FF00")
BLUE = Color("#0000FF")

class Tile:
	""" Tile( ... ) -> Tile

	TODO: docstring

	Attributes:

	level: the level on which the tile is found
	
	x, y: the coordinates of the tile on that level
	"""

	def __init__(self, level, x, y): #TODO: args
		self.empty_symbol = EMPTY_TILE_FLOOR_SYMBOL
		self.empty_color = WHITE
		self.current_being = None
		self.x, self.y = x, y
		self.level = level
		self.tile_items = Inventory() #TODO: implement tile items

		# TODO: figure out how to handle a tile's contents, their order, and which symbol should appear on top,
		# along with how to udpade the current symbol properly.

	def update(self):
		symbol = self.symbol_image()
		self.level.level_map.blit(symbol, (self.x * TILE_WIDTH, self.y * TILE_HEIGHT))

	def remove_being(self):
		if(self.current_being):
			self.current_being.current_tile = None
			self.current_being = None
			self.update()

	def passable(self):
		return self.current_being == None #TODO: make this also return false for closed doors, solid walls, etc.

	def current_symbol(self):
		if(self.current_being != None):
			return self.current_being.current_symbol()
		if(self.contains_items()):
			return self.tile_items.top_item().current_symbol()
		return self.empty_symbol

	def current_color(self):
		if(self.current_being != None):
			return self.current_being.color()
		return WHITE

	def symbol_image(self):
		symbol_char = self.current_symbol()
		symbol_color = self.current_color()
		font = pygame.font.Font("./fonts/FreeSansBold.ttf", 8) 	#TODO: consider making this a constant somewhere, or an arg.
		symbol_text = font.render(symbol_char, 0, symbol_color)
		symbol_image = Surface((TILE_WIDTH, TILE_HEIGHT))
		symbol_image.blit(symbol_text, (0, 0))
		return symbol_image

	def tile_item_select_list(self):
		return self.tile_items.item_select_list()

	def add_item_list(self, items):
		self.tile_items.add_item_list(items)
		self.update()

	def add_item(self, item):
		self.tile_items.add_item(item) #TODO: consider how this will affect the tile's appearance
		self.update()

	def remove_item(self, item):
		self.tile_items.remove_item(item)
		self.update()

	def contains_items(self):
		return not self.tile_items.empty()

	def top_item(self):
		return self.tile_items.top_item()

	def item_count(self):
		return self.tile_items.item_count()

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