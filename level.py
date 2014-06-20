""" A level of the dungeon, usually filled with monsters and treasure. 
"""

#TODO: import as necessary.
from turncounter import *
from wall import *

WHITE = Color("#FFFFFF")

class Level:
	""" Level( int, int, int ) -> Level

	A level exists in the context of a larger dungeon. It contains a two-dimensional
	set of tiles which beings such as the player can traverse.

	Attributes:

	width and height are the dimensions of the Level in tiles.

	depth is how far "underground" the level is, where 0 means it's on the surface.
	A higher depth means a lower (and usually harder) level.
	Multiple levels may be on different branches, but have the same depth.

	level_map is a visual representation of the level, onto which is contents are displayed.

	tiles are the individual, same-sized tiles that make up the level.

	beings and monsters are the creatures that are currently on the level.

	player is the being that the person playing the game is controlling.

	turn_counter is an object that processes the passage of time on the level.
	Different actions take different amounts of time and the turn_counter
	manages this system.

	"""

	def __init__(self, width, height, depth): #TODO: other args if necessary
		self.width, self.height = width, height
		self.depth = depth
		self.level_map = Surface((width * TILE_WIDTH, height * TILE_HEIGHT))
		self.tiles = []
		self.init_tiles()
		self.beings = []
		self.monsters = []
		self.player = None
		self.turn_counter = TurnCounter()
		self.effects = []

	def init_tiles(self):
		""" l.init_tiles( ) -> None

		Create a bunch of empty tiles.
		This is subject to change once we implement level generation.
		"""
		for y in range(self.height):
			self.tiles.append([])
			for x in range(self.width):
				next_tile = Tile(self, x, y) #TODO: change if tiles get args
				self.tiles[y].append(next_tile)
				next_tile.update()

	def level_map_section(self, x1, y1, x2, y2):
		""" l.level_map_section( int, int, int, int ) -> Surface

		Returns an image that is a section of the level with
		(x1, y1) as its upper-left corner and
		(x2, y2) as its lower-right corner.
		"""
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

	def send_event(self, message): #TEMP. might not always send message right away.
		""" l.send_event( str ) -> None

		Display a message on the event pane.
		"""
		if(self.player != None):
			self.player.send_event(message)

	def add_effect(self, symbol, x, y, color = WHITE):
		effect = Effect(symbol, x, y, color)
		self.effects.append(effect)

	def plan_monster_turns(self): #NOTE: might need to do more than this
		""" l.plan_monster_turns( ) -> None

		Every monster on the level decides what it will do next.
		"""
		for m in self.monsters:
			m.decide_next_turn()

	def process_turns(self):
		""" l.process_turns( ) -> None

		Tell the turn counter to process the current turns of all Beings and Statuses on the level.
		"""
		self.turn_counter.process_turns()

	def enqueue_delay(self, actor, delay):
		""" l.enqueue_delay( Being/Status, int ) -> None

		Give the turn counter some delay for an actor on the level.
		The actor must wait this many units of time before doing something again.
		"""
		self.turn_counter.enqueue_delay(actor, delay)

	def enqueue_player_delay(self, player, delay):
		""" l.enqueue_player_delay( Player, int ) -> None

		Tell the turn counter to make the player wait for the given number of units of time
		before acting again.
		"""
		self.turn_counter.enqueue_player_delay(player, delay)

	def clear_map(self):
		""" l.clear_map( ) -> None

		Overwrite the current level map, usually in preparation for redrawing it.
		"""
		self.level_map =  Surface((self.width * TILE_WIDTH, self.height * TILE_HEIGHT))

	def add_tile(self, tile, x, y): # not to be used aside from building the level (at least for now)
		""" l.add_tile( Tile, int, int ) -> None

		Place the given tile on the level at the given coordinates.
		"""
		self.tiles[y][x] = tile

	def add_wall(self, x, y):
		""" l.add_wall( int, int ) -> None

		Place a wall on the level at the given coordinates.
		"""
		wall = Wall(self, x, y)
		self.add_tile(wall, x, y)
		wall.update()

	def add_item(self, item, x, y):
		""" l.add_item( Item, int, int ) -> None

		Add an item to the level on the tile at the given coordinates.
		"""
		if(self.valid_tile(x, y)):
			self.tile_at(x, y).add_item(item)

	def add_player(self, player, x, y):
		""" l.add_player( Player, int, int ) -> None

		Set the level's player to the given Player and place him at the given coordinates.
		"""
		self.player = player
		self.add_being(player, x, y)

	def add_monster(self, monster, x, y):
		""" l.add_monster( Monster, int, int ) -> None

		Add the given monster to the level at the given coordinates.
		"""
		self.monsters.append(monster)
		self.add_being(monster, x, y)

	def remove_monster(self, monster):
		""" l.remove_monster( Monster ) -> None

		Remove the given monster from the level.
		"""
		if(monster in self. monsters):
			self.monsters.remove(monster)
		self.remove_being(monster)

	def add_being(self, being, x, y):
		""" l.add_being( Being, int, int ) -> None

		Add the given being to the level at the given coordinates.
		"""
		self.beings.append(being)
		if(self.valid_tile(x, y)):
			being.current_level = self
			self.tiles[y][x].set_being(being)

	def remove_being(self, being):
		""" l.remove_being( Being ) -> None

		Remove the given Being from the level.
		"""
		if(being in self.beings):
			self.beings.remove(being)
			self.remove_actor(being)
			being.current_tile.remove_being()

	def remove_actor(self, actor):
		""" l.remove_actor( Being/Status ) -> None

		Stop the given actor from doing any more things on this level.
		"""
		self.turn_counter.remove_actor(actor)

	def being_in_tile(self, x, y):
		""" l.being_in_tile( int, int ) -> Being

		If there is a being in the tile at the given coordinates, return it.
		"""
		if(self.valid_tile(x, y)):
			return self.tile_at(x, y).current_being
		return None

	def tile_at(self, x, y):
		""" l.tile_at( int, int ) -> Tile

		Return the tile at the given coordinates.
		"""
		#TODO: error checking? (might want it before this method is called in many cases.)
		return self.tiles[y][x]

	def open_tile(self, x, y):
		""" l.open_tile( int, int ) -> bool

		Check whether the tile at the given coordinates is passable (i.e., a being can move through it.)
		"""
		return self.valid_tile(x, y) and self.tile_at(x, y).passable()

	def valid_tile(self, x, y):
		""" l.valid_tile( int, int ) -> bool

		Check whether the given coordinates correspond to a tile in this level.
		"""
		return x >= 0 and y >= 0 and x < self.width and y < self.height

	def temp_place_being(self, being, x, y): #used for movement. TEMPORARY. (no docstring for temporary methods)
		if(self.valid_tile(x, y)):
			self.tiles[y][x].set_being(being)

	def turn_count(self):
		""" l.turn_count( ) -> int

		Gives the amount of time that has passed since the start of the game.
		"""
		return self.turn_counter.turn_count