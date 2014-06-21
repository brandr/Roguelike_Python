# -*- coding: utf-8 -*-
""" A single space on a level in the dungeon.
"""

from equipmentset import *
from effect import *

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
	""" Tile( Level, int, int) -> Tile

	Tiles are the components that make up a level. A tile can contain at most
	one Being and zero or more items.

	Attributes:

	empty_symbol: the symbol the tile appears as when nothing is in it.

	empty_color: the color the tile appears as when nothing is in it.

	current_being: the Being occupying the Tile.

	level: the level on which the tile is found.

	tile_items: the items contained in the tile
	
	x, y: the coordinates of the tile on that level.
	"""

	def __init__(self, level, x, y): #TODO: args
		self.empty_symbol = EMPTY_TILE_FLOOR_SYMBOL
		self.empty_color = WHITE
		self.current_being = None
		self.x, self.y = x, y
		self.level = level
		self.tile_items = Inventory() #TODO: implement tile items
		self.effect = None
		# TODO: figure out how to handle a tile's contents, their order, and which symbol should appear on top,
		# along with how to udpade the current symbol properly.

	def update(self):
		""" t.update( ) -> None

		Updates the tile with whatever should appear on top of it.
		"""

		symbol = self.symbol_image()
		self.level.level_map.blit(symbol, (self.x * TILE_WIDTH, self.y * TILE_HEIGHT))

	def set_effect(self, symbol, color):
		self.effect = Effect(symbol, color)
		self.update()

	def passable(self):
		""" t.passable( ) -> None

		Tells whether something can move through this tile.
		Later, we'll need to handle walls being impassable, water being passable only for hovering/flying stuff, etc. 
		"""
		return self.current_being == None #TODO: make this also return false for closed doors, solid walls, etc.

	def current_symbol(self):
		""" t.current_symbol( ) -> char

		Returns the symbol that should represent the top of the tile.
		"""
		if(self.current_being != None):
			return self.current_being.current_symbol()
		if(self.contains_items()):
			return self.tile_items.top_item().current_symbol()
		return self.empty_symbol

	def current_color(self):
		""" t.current_color( ) -> Color

		Returns the color that should represent the top of the tile.
		"""
		if(self.current_being != None):
			return self.current_being.color()
		return WHITE

	def symbol_image(self):
		""" t.symbol_image( ) -> Surface

		Returns an image representing this tile.
		"""
		if self.effect:
			symbol_char = self.effect.symbol
			symbol_color = self.effect.color
		else:
			symbol_char = self.current_symbol()
			symbol_color = self.current_color()
		font = pygame.font.Font("./fonts/FreeSansBold.ttf", 8) 	#TODO: consider making this a constant somewhere, or an arg.
		symbol_text = font.render(symbol_char, 0, symbol_color)
		symbol_image = Surface((TILE_WIDTH, TILE_HEIGHT))
		symbol_image.blit(symbol_text, (0, 0))
		return symbol_image

	def tile_item_select_list(self):
		""" t.tile_item_select_list( ) -> SelectList 

		Returns a SelectList containing the items found in this tile.
		Pretty sure this is only called when picking up items.
		"""
		return self.tile_items.item_select_list()

	def add_item_list(self, items):
		""" t.add_item_list( [Item] ) -> None

		Adds a set of items to the tile.
		"""
		self.tile_items.add_item_list(items)
		self.update()

	def add_item(self, item):
		""" t.add_item( Item ) -> None

		Adds one item to the tile.
		"""
		self.tile_items.add_item(item) #TODO: consider how this will affect the tile's appearance
		self.update()

	def remove_item(self, item):
		""" t.remove_item( Item ) -> None

		Removes an item from the tile.
		"""
		self.tile_items.remove_item(item)
		self.update()

	def contains_items(self):
		""" t.contains_items( Item ) -> bool

		Checks whether there are any items in the tile.
		"""
		return not self.tile_items.empty()

	def top_item(self):
		""" t.top_item( ) -> Item

		Return the item at the top of the tile.
		"""
		return self.tile_items.top_item()

	def item_count(self):
		""" t.item_count( Item ) -> int

		Returns the number of items in this tile.	
		"""
		return self.tile_items.item_count()

	def set_being(self, being):
		""" t.set_being( Being ) -> None

		Set the current being that occupies this tile.
		"""
		self.current_being = being
		being.current_tile = self
		self.update()

	def remove_being(self):
		""" t.remove_being( ) -> None

		Remove the current being from this tile.
		"""
		if self.current_being:
			self.current_being.current_tile = None
			self.current_being = None
			self.update()

	def coordinates(self):
		""" t.coordinates( ) -> (int, int)

		Returns the coordinates of this tile on the level.
		"""
		return (self.x, self.y)