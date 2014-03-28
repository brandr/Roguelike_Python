""" An abstract pane class representing a visual, immobile pane of the game screen.
"""

import pygame 
from pygame import *
from numpy import *

WHITE = Color("#FFFFFF")
BLACK = Color("#000000")

class Pane:
	""" Pane ( int, int ) -> Pane

	TODO: describe a Pane and what it does

	"""

	def __init__(self, x, y, width, height):
		self.x_off = x
		self.y_off = y
		self.contents = Surface((width, height))
		self.draw_borders(width - 2, height - 2)

	def draw_borders(self, width, height):
		pygame.draw.line(self.contents, WHITE, (0, 0), (width, 0), 2)
		pygame.draw.line(self.contents, WHITE, (width, 0), (width, height), 2)
		pygame.draw.line(self.contents, WHITE, (width, height), (0, height), 2)
		pygame.draw.line(self.contents, WHITE, (0, height), (0, 0), 2)
		#self.contents.fill(WHITE)
		#self.rect = Rect(x, y, width, height)

		# TODO: add more pane attributes if necessary.