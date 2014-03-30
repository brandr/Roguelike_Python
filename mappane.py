""" The pane in wihcih the main map for the game is generated.
"""

from pane import *
from level import *
# NOTE: this isn't high priority, but later on we might want to store the map
# pane dimensions someplace where it's easier to see the values that they are relative to.
# (i.e., total screen size and whatnot.)

MAP_PANE_X = 40
MAP_PANE_Y = 40

MAP_PANE_WIDTH = 450
MAP_PANE_HEIGHT = 450

class MapPane(Pane):
	""" MapPane ( ) -> MapPane

	TODO: describe a MapPane and what it does

	Attributes:

	TODO

	"""

	def __init__(self, level):
		Pane.__init__(self, MAP_PANE_X, MAP_PANE_Y, MAP_PANE_WIDTH, MAP_PANE_HEIGHT)
		self.current_level = level
		
	def level_update(self): #TODO: args
		x1, x2, y1, y2 = 0, 0, 35, 35 #temporary values for testing. TODO: might want to take these as args, or derive them from current_level.
		level_map = self.current_level.level_map_section(x1, x2, y1, y2)
		self.update(level_map)