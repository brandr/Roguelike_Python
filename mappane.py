""" The pane in wihcih the main map for the game is generated.
"""

from pane import *
from level import *
# NOTE: this isn't high priority, but later on we might want to store the map
# pane dimensions someplace where it's easier to see the values that they are relative to.
# (i.e., total screen size and whatnot.)

MAP_PANE_X = 40
MAP_PANE_Y = 80

MAP_PANE_WIDTH = 450
MAP_PANE_HEIGHT = 450

class MapPane(Pane):
	""" MapPane ( ... ) -> MapPane

	TODO: describe a MapPane and what it does

	Attributes:

	TODO

	"""

	def __init__(self, player):
		Pane.__init__(self, MAP_PANE_X, MAP_PANE_Y, MAP_PANE_WIDTH, MAP_PANE_HEIGHT)
		self.player = player
		
	def update(self): 
		coords = self.player.coordinates()
		center_x, center_y = coords[0], coords[1]
		half_width, half_height = MAP_PANE_WIDTH/(2 * TILE_WIDTH), MAP_PANE_HEIGHT/(2 * TILE_HEIGHT)
		x1, y1 = center_x - half_width, center_y - half_height
		x2, y2 = center_x + half_width, center_y + half_height
		level_map = self.player.current_level.level_map_section(x1, y1, x2, y2)
		Pane.update(self, level_map)