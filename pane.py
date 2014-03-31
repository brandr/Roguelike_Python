""" An abstract pane class representing a visual, immobile pane of the game screen.
"""

from tile import *
from numpy import *

#WHITE = Color("#FFFFFF")
#BLACK = Color("#000000")

class Pane:
	""" Pane ( int, int ) -> Pane

	TODO: describe a Pane and what it does

	"""

	def __init__(self, x, y, width, height):
		self.x_off, self.y_off = x, y
		self.width, self.height = width, height
		self.contents = Surface((self.width, self.height))
		self.pane_image = Surface((self.width + 4, self. height + 4)) # add 2 * 2 for the borders.
		self.draw_borders(width + 2, height + 2)

	def draw_borders(self, width, height):
		pygame.draw.line(self.pane_image, WHITE, (0, 0), (width, 0), 2)
		pygame.draw.line(self.pane_image, WHITE, (width, 0), (width, height), 2)
		pygame.draw.line(self.pane_image, WHITE, (width, height), (0, height), 2)
		pygame.draw.line(self.pane_image, WHITE, (0, height), (0, 0), 2)

	def update(self, contents = None):
		self.clear()
		if(contents != None):
			self.contents.blit(contents, (0, 0))

	def clear(self):
		self.contents = Surface((self.width, self.height))

	def draw_pane_image(self):
		self.pane_image.blit(self.contents, (2, 2))
		return self.pane_image
		# TODO: add more pane attributes if necessary.