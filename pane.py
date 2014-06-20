""" An abstract pane class representing a visual, immobile pane of the game screen.
"""

from tile import *
#from numpy import *

class Pane:
	""" Pane ( int, int ) -> Pane

	A pane is an abstract type of rectangular space that can contain visual elements.

	Attributes:
	x_off and y_off are the pane's offset (coords of its upper-left corner) on the master screen.

	width and height are the pane's dimensions in pixels.

	contents are a pygame Surface which will show the visual elements inside the pane.

	font is the font used to write any text on the pane.
	"""

	def __init__(self, x, y, width, height):
		self.x_off, self.y_off = x, y
		self.width, self.height = width, height
		self.contents = Surface((self.width, self.height))
		self.pane_image = Surface((self.width + 4, self. height + 4)) # add 2 * 2 for the borders.
		self.draw_borders(width + 2, height + 2)
		self.font = pygame.font.Font(None, 14) 

	def draw_borders(self, width, height):
		""" p.draw_borders( int, int ) -> None

		Draw white borders around the pane.
		"""
		pygame.draw.line(self.pane_image, WHITE, (0, 0), (width, 0), 2)
		pygame.draw.line(self.pane_image, WHITE, (width, 0), (width, height), 2)
		pygame.draw.line(self.pane_image, WHITE, (width, height), (0, height), 2)
		pygame.draw.line(self.pane_image, WHITE, (0, height), (0, 0), 2)

	def update(self, contents = None):
		""" p.update( Surface ) -> None

		Refresh the pane with its contents' current image.
		"""
		self.clear()
		if(contents != None):
			self.contents.blit(contents, (0, 0))

	def clear(self):
		""" p.clear( ) -> None

		Turn the pane's contents into a black rectangle.
		"""
		self.contents = Surface((self.width, self.height))

	def draw_pane_image(self):
		""" p.draw_pane_image( ) -> Surface

		Returns the pane's image as it will appear onscreen.
		"""
		self.pane_image.blit(self.contents, (2, 2))
		return self.pane_image

	def rendered_text(self, text):
		""" p.rendered_text( str ) -> Surface

		Turn inputted string into a text image.
		"""
		return self.font.render(text, 0, WHITE)
		# TODO: add more pane attributes if necessary.