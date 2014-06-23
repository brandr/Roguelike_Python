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

	solid: whether things should be unable to pass through the tile. False for deep water, lava, and other hazards, as well as tiles that have Beings in them.
	"""

	def __init__(self, level, x, y): #TODO: args
		self.empty_symbol = EMPTY_TILE_FLOOR_SYMBOL
		self.empty_color = WHITE
		self.current_being = None
		self.x, self.y = x, y
		self.level = level
		self.tile_items = Inventory() #TODO: implement tile items
		self.effect = None
		self.solid = False
		# TODO: figure out how to handle a tile's contents, their order, and which symbol should appear on top,
		# along with how to udpade the current symbol properly.

	def update(self):
		""" t.update( ) -> None

		Updates the tile with whatever should appear on top of it.
		"""

		symbol = self.symbol_image()
		self.level.level_map.blit(symbol, (self.x * TILE_WIDTH, self.y * TILE_HEIGHT))

	def set_effect(self, symbol, color):
		""" t.set_effect( char, Color ) -> None

		Adds a visual effect to this tile.
		"""
		self.effect = Effect(symbol, color)
		self.update()

	def clear_effect(self):
		""" t.clear_effect( ) -> None

		Removes the visual effect from this tile.
		"""
		self.effect = None
		self.update()

	def passable(self):
		""" t.passable( ) -> None

		Tells whether something can move through this tile.
		Later, we'll need to handle walls being impassable, water being passable only for hovering/flying stuff, etc. 
		"""

		return not self.solid and self.current_being == None #TODO: make this also return false for closed doors, solid walls, etc.

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

	def in_range(self, target, check_range):
		""" t.in_range(Being/Tile, int ) -> bool

		Check whether this Tile is in the given range of the given other being/tile.
		"""
		offset = self.offset_from(target)
		#distance = (int)(sqrt(pow(offset[0], 2) + pow(offset[1], 2)))	# we may want this-- it calculates a circle rather than a square, which is not accurate for roguelike geometry but looks nicer.
		distance = max(abs(offset[0]), abs(offset[1]))
		return check_range >= distance

	def direction_towards(self, target):
		""" t.direction_towards( Being/Tile ) -> (int, int)

		Returns the direction that the given target is in with respect to this Tile.
		Uses the same directional notation as coords_in_direction.
		"""
		offset = self.offset_from(target)
		x_dir = Tile.direction_from_diff(offset[0])
		y_dir = Tile.direction_from_diff(offset[1])
		return (x_dir, y_dir)

	def offset_from(self, target): #signed offset from target being
		""" t.offset_from( Being/Tile ) -> (int, int)

		Like direction_towards(), but includes distance instead of just direction.
		"""
		current_coords = self.coordinates()
		target_coords = target.coordinates()
		x_diff = int(target_coords[0] - current_coords[0])
		y_diff = int(target_coords[1] - current_coords[1])
		return (x_diff, y_diff)

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

	@staticmethod
	def direction_from_diff(diff):
		""" direction_from_diff( int ) -> int

		Take a number and return its sign multiplied by 1.
		i.e., f(32) = 1, f(0) = 0, f(-32) = -1, f(1) = 1, etc.
		"""
		if(diff == 0): return 0
		return (int)(diff/abs(diff))