""" A weapon meant for melee. However, it may still have a range greater than 1 tile
	(if it is a halberd, for instance.)
"""

from weapon import *

AXE = "axe"
SWORD = "sword"
STR = "strength"
DEX = "dexterity"

WEAPON_DICT = {AXE: [STR,[2,6],1.2, 1]}

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
	weapon_enchant_numbers (list): [To hit bonus, damage bonus]
	weapon_enchant_brand (string): Other effects

	"""

	def __init__(self, name, type):
		Weapon.__init__(self, name)
		weapon_type = type
		weapon_info = WEAPON_DICT[type]
		weapon_stat = weapon_info[0]
		weapon_damage = 500
		weapon_speed = 5
		weapon_range = weapon_info[3]

