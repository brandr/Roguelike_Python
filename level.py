""" A level of the dungeon, usually filled with monsters and treasure. 
"""

#TODO: import as necessary.
from turncounter import *

class Level:
	""" Level( int, int, int ) -> Level

	A level exists in the context of a larger dungeon. It contains a two-dimensional
	set of tiles which beings such as the player can traverse.

	Attributes:

	width and height are the dimensions of the Level in tiles.

	depth is how far "underground" the level is, where 0 means it's on the surface.
	A higher depth means a lower (and usually harder) level.
	Multiple levels may be on different branches, but have the same depth.

	"""

	def __init__(self, width, height, depth): #TODO: other args if necessary
		self.width, self.height = width, height
		self.depth = depth
		self.level_map = Surface((width * TILE_WIDTH, height * TILE_HEIGHT))
		self.tiles = []
		self.init_tiles()
		self.beings = []
		self.player = None
		self.turn_counter = TurnCounter()

	def init_tiles(self):
		for y in range(self.height):
			self.tiles.append([])
			for x in range(self.width):
				next_tile = Tile(self, x, y) #TODO: change if tiles get args
				self.tiles[y].append(next_tile)
				next_tile.update()

	def process_turns(self):
		self.turn_counter.process_turns() #TODO

	def enqueue_action(self, being, action, arg, delay):
		self.turn_counter.enqueue_action(being, action, arg, delay)

	def enqueue_player_action(self, action, arg, delay):
		self.turn_counter.enqueue_player_action(self.player, action, arg, delay)

	def clear_map(self):
		self.level_map =  Surface((self.width * TILE_WIDTH, self.height * TILE_HEIGHT))

	def add_player(self, player, x, y):
		self.player = player
		self.add_being(player, x, y)

	def add_being(self, being, x, y):
		self.beings.append(being)
		if(self.valid_tile(x, y)):
			being.current_level = self
			self.tiles[y][x].set_being(being)

	def level_map_section(self, x1, y1, x2, y2):
		map_width, map_height = TILE_WIDTH * (x2 - x1), TILE_HEIGHT * (y2 - y1)
		l_map = Surface((map_width, map_height))
		x_start, y_start = x1 * TILE_WIDTH, y1 * TILE_HEIGHT
		x_end, y_end = x2 * TILE_WIDTH, y2 * TILE_HEIGHT
		section_x1, section_y1 = max(0, x_start), max(0, y_start)
		section_x2, section_y2 = min(self.level_map.get_width() - section_x1, x_end), min(self.level_map.get_height() - section_y1, y_end)
		section = self.level_map.subsurface(section_x1, section_y1, section_x2, section_y2)
		blit_off_x, blit_off_y = TILE_WIDTH + max(0, -1 * x_start), TILE_HEIGHT + max(0, -1 * y_start)
		l_map.blit(section, (blit_off_x, blit_off_y))
		return l_map

	def tile_at(self, x, y):
		#TODO: error checking? (might want it before this method is called in many cases.)
		return self.tiles[y][x]

	def valid_tile(self, x, y):
		return x >= 0 and y >= 0 and x < self.width and y < self.height

	def temp_place_being(self, being, x, y): #used for movement. TEMPORARY.
		if(self.valid_tile(x, y)):
			self.tiles[y][x].set_being(being)

	def turn_count(self):
		return self.turn_counter.turn_count