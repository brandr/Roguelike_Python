""" An active projectile respresenting some sort of thrown/shot object, spell, etc.
"""

PROJECTILE_SPEED_CONSTANT = 4

class Projectile:
	""" Projectile( Item/Spell, [Tile] ) -> Projectile

	A projectile technically "has" the object it represents, and only exists as long as that object
	is in motion across the screen. It is essentially an abstract "vehicle" that allows the carried
	object to either hit a wall and (possibly) dissipate or collide with some target.

	Attributes:

	held_object: the object the projectile represents.

	tile_path: the tiles the object should travel across.

	player: the player witnessing (not necessarily involved with) this projectile.

	projectile_index: an index indicating how far the projectile has traveled.



	"""

	def __init__(self, held_object, tile_path, player): #TODO: more args?
		self.held_object = held_object
		self.tile_path = tile_path
		self.player = player
		self.projectile_index = 0


	def update(self):
		""" p.update( ) -> None

		The projectile continues to advance across the level.
		"""
		#TODO: deal with walls here if necessary
		tile_index = self.projectile_index/PROJECTILE_SPEED_CONSTANT
		if self.tile_path[tile_index].solid:	#TODO: make sure this is a robust way to handle wall collisions.
			self.collide_with_tile(self.tile_path[tile_index - 1])
			self.player.current_level.remove_projectile(self)
			return
		# TODO: check for hitting a Being in the current tile here. If the projectile misses and keeps moving (or pierces through a Being), the 
		# 		collision check takes place and sends a message, but does not cause projectile to stop updating.
		if(tile_index >= len(self.tile_path)):
			self.collide_with_tile(self.tile_path[-1])
			self.player.current_level.remove_projectile(self)
			return
		if(tile_index > 0):
			self.tile_path[tile_index - 1].clear_effect()
		tile = self.tile_path[tile_index]
		symbol, color = self.held_object.current_symbol(), self.held_object.current_color()
		tile.set_effect(symbol, color)
		self.projectile_index += 1
		
	def collide_with_tile(self, tile):
		""" p.collide_with_tile( Tile ) -> None

		Perform the proper collision with this tile.
		"""
		tile.clear_effect()
		self.held_object.collide_with_tile(tile)
		self.player.screen_manager.switch_to_main_game_controls(self.player)

	def collide_with_being(self, being):
		""" p.collide_with_being( Being ) -> None

		Perform the proper collision with this being.
		"""
		pass #TODO