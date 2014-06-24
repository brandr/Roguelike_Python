""" A monster is a creature in the dungeon, usually hostile to the player.
"""

from being import *

class Monster(Being):
	""" Monster( ... ) -> Monster

	A monster is a Being that is not the Player and is usually hostile to the player.

	Attributes:

	name is the Monster's name. It should probably be displayed the same way in most contexts.

	hit_points are [current hp, max hp]. When HP goes to zero the monster usually dies.

	move_delay is how long the monster must wait after moving before doing something gain.

	attack_delay is how long the monster must wait after attacking before doing something again.
	"""
	def __init__(self, name): #TODO: args (first figure out how monsters will be built)
		Being.__init__(self, name)
		self.hit_points = [10, 10] #TEMP
		self.move_delay = 5
		#self.attack_delay = 3

	def current_symbol(self):
		""" m.current_symbol( ) -> char

		Gives the symbol that should be used to represent the monster onscreen.
		"""
		return 'M'			#TODO: figure out how monster symbols will be derived

	def die(self):
		""" m.die( ) -> None

		The monster dies, instantly dropping all its items.
		"""
		self.send_event(self.display_name() + " died!") #TEMP
		self.remove_all_equipment()
		self.drop_all_items()
		#TODO: implement corpse dropping and other death-prompted things
		self.current_level.remove_monster(self)

	def decide_next_turn(self):	#TODO: monster AI-based decision-making goes here
		""" m.decide_next_turn( ) -> None

		The monster plans its next turn.
		We want to implement AI here.
		"""
		#TODO: may check action queue here. not sure.
		player = self.current_level.player
		if player != None:
			self.melee_pursue(player)

	def melee_pursue(self, target):
		""" m.melee_pursue( Being ) -> None

		Move towards a target with the intent of melee-attacking it,
		or just melee-attack it if it's in range.
		"""
		direction = self.direction_towards(target)
		dest_coords = self.coords_in_direction(direction)
		if(self.enemy_in_tile(dest_coords[0], dest_coords[1])):
			new_target = self.current_level.being_in_tile(dest_coords[0], dest_coords[1]) #this may actually be the original target.
			self.temp_monster_attempt_melee_attack(new_target)
		elif(self.current_level.open_tile(dest_coords[0], dest_coords[1])):
			self.begin_move_towards(target)
		else:
			self.execute_action(self.wait, None, 1)

	def begin_move_towards(self, target): #I forget why I gave this its own method but it will be useful as we work on movement
		""" m.begin_move_towards( Being ) -> None

		The first step of a monster moving towards a target it can see.
		"""
		self.temp_monster_move_towards(target)
		
	def temp_monster_move_towards(self, target): # TODO: replace with a more robust process based on flowchart.
		# no docstring because temporary
		direction = self.direction_towards(target) #TODO: pathing
		dest_coords = self.coords_in_direction(direction)
		if(self.current_level.open_tile(dest_coords[0], dest_coords[1])):
			self.execute_action(self.move_towards, target, self.move_delay)
		else:		
			self.execute_action(self.wait, None, 1)

		#TEMP
	def temp_monster_attempt_melee_attack(self, being):
		# no docstring because temporary
		self.execute_action(self.melee_attack, being, self.melee_attack_delay())