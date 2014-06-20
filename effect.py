""" A graphical effect occupying a single tile.
"""

#TODO imports

class Effect:
	""" Effect( char, Color ) -> Effect

	A visual effect occupying one tile that does not affect gameplay directly.

	Attributes:

	symbol: the symbol that represents this effect.

	color: the color representing this effect.
	"""
	def __init__(self, symbol, color):
		self.symbol, self.color