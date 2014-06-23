""" A potion that may harm or help the player when swallowed.
"""

from consumable import *

POTION_STACK_SIZE = 99

class Potion(Consumable):
	""" Potion( ... ) -> Potion

	TODO: once potions have been fully implemented, docstring them.
	"""

	def __init__(self, name = None, count = 1):	#might not use name unless there are unique potions. 
		Consumable.__init__(self, name, [count, POTION_STACK_SIZE])

	def display_name(self, arg = None):
		return self.name

	def item_category(self):
		return POTION

	def collide_with_tile(self, tile, player):
		""" p.collide_with_tile( Tile, Player ) -> None

		The potion shatters against a tile, applying some tile effect to it if necessary.
		"""
		player.send_event("The potion shatters against the ground!")
		#TODO: the potion applies some effect to the tile.
		# ex:  water turns a dry floor tile into a shallow water tile,
		#	   polymorph tiles into other tiles with similar passability/solidity, etc.

class InstantPotion(Potion):
	""" TODO """

	def __init__(self, name = None):
		Potion.__init__(self, name)

	def take_effect(self, target):
		self.potion_effect(target)

class DurationPotion(Potion):
	""" TODO """

	def __init__(self, name = None):
		Potion.__init__(self, name)

	def take_effect(self, target):
		effect = self.potion_effect
		poison_status = Status(effect, 7, 25) #7 is temp delay value, 5 is temp duration
		target.add_status(poison_status)

class HealingPotion(InstantPotion):
	""" TODO """

	def __init__(self):
		InstantPotion.__init__(self, "potion of healing")
		self.heal_points = 4 #TEMP

	def potion_effect(self, target):
		target.restore_hp(self.heal_points)

class PoisonPotion(DurationPotion):
	""" TODO""" 

	def __init__(self):
		DurationPotion.__init__(self, "potion of poison")
		self.poison_damage = 1 #TEMP

	def potion_effect(self, target):
		target.take_damage(self.poison_damage)
