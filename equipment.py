""" Any item that the player can equip, such as armor, rings, amulets, etc.
	Weapons are not considered equipment, because any item can be wielded.
	Shields are considered equipment, however.
"""

from item import *

class Equipment(Item):
	""" Equipment( ... ) -> Equipment

	An abstract class used as a template for anything that can be [E]quipped by a being.

	Attributes:
	TODO
	"""

	def __init__(self):
		Item.__init__(self)
		#TODO