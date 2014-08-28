""" A weapon meant for melee. However, it may still have a range greater than 1 tile
	(if it is a halberd, for instance.)
"""

from weapon import *

AXE = "axe"
SHORT_BLADE = "short_blade"
LONG_BLADE = "long_blade"

STR = "strength"
DEX = "dexterity"

SLASH = "slashing"
STAB = "stabbing"

WEAPON_DICT = {
	AXE: [STR, [2, 6], 1.2, 1, SLASH],
	SHORT_BLADE: [DEX, [1, 4], 1.6, 1, STAB],
	LONG_BLADE: [STR, [2, 5], 1.4, 1, STAB]
}

class MeleeWeapon(Weapon):
	""" MeleeWeapon( ... ) -> MeleeWeapon

	A weapon specifically meant for melee, inherting
	from more general weapons (which may be ranged or melee).
	Every melee weapon should have the following attributes:
	Attributes:
	(inherited from Weapon), and:
	weapon_type (string): The type of melee weapon this is.
	weapon_stat (string): The stat that makes this weapon strong.
	weapon_damage (int): The base damage for this weapon.
	weapon_speed (float): The base speed for this weapon.
	weapon_range (int): Max hit range for this weapon.
	weapon_damage_type (string): Damage type for this weapon. 
	weapon_enchant_numbers (list): [To hit bonus, damage bonus]
	weapon_enchant_brand (string): Other effects

	"""

	def __init__(self, name, weapon_type, two_handed = False):
		Weapon.__init__(self, name, two_handed)
		self.weapon_type = weapon_type
		weapon_info = WEAPON_DICT[weapon_type]
		self.weapon_stat = weapon_info[0]
		self.weapon_damage = 500
		self.weapon_speed = 5
		self.weapon_range = weapon_info[3]

	def create_copy(self, amount = None):
		""" a.create_copy( int ) -> Ammo

		Returns a new ammo that is a copy of this one with the given amount.
		"""
		if not amount: amount = self.current_quantity()
		return MeleeWeapon(self.name, self.weapon_type, self.two_handed)

		#self.weapon_damage_type = weapon_info[4] Should go in after we figure typed damage out, but oughta be stored here.

