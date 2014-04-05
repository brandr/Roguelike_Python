""" A protective item which a Being may be able to equip (if it fits).
"""

from equipment import *

class Armor(Equipment):
	""" Armor( ... ) -> Armor

	An armor corresponds to a specific slot, which we will likely
	keep track of using a dictionary.

	Attributes: TODO

	"""

	def __init__(self, name):
		Equipment.__init__(self, name)