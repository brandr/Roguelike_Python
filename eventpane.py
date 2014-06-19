""" A text-only pane showing events that occur in the game.
"""

from pane import *

EVENT_PANE_X = 40
EVENT_PANE_Y = 540

EVENT_PANE_WIDTH = 450
EVENT_PANE_HEIGHT = 64

LINE_COUNT = 4 #number of lines that can be displayed at ance
X_MARGIN = 4

class EventPane(Pane):
	""" EventPane ( Player ) -> EventPane

	An event pane shows text describing game events from the
	Player's point of view.

	Attributes:

	player: The player who is described in this event pane.
	lines: Lines of text to be displayed.
	"""

	def __init__(self, player): # should this really be centered on the player? not sure
		Pane.__init__(self, EVENT_PANE_X, EVENT_PANE_Y, EVENT_PANE_WIDTH, EVENT_PANE_HEIGHT)
		player.event_pane = self
		self.player = player
		self.lines = []

	def display(self, message): #TODO: case for messages that have multiple lines (should be handled here)
		""" ep.display( str ) -> None

		Displays the given string on the lowest line of the event pane.
		"""
		rendered_message = self.rendered_text(message)
		self.display_line(rendered_message)

	def display_line(self, line):
		""" ep.display_line( Surface ) -> None

		Displays the given rendered text image on the lowest
		line of the event pane.
		"""
		self.lines.append(line)
		self.update()

	def update(self):
		""" ep.update( ) -> None

		Updates the event pane so that it shows only the 4 most recent
		message lines.
		"""
		self.clear()
		height = self.contents.get_height()
		bottom_y = height - 16 #temp
		line_height = height/LINE_COUNT
		for i in range(LINE_COUNT):
			if(i + 1 <= len(self.lines)):
				line = self.lines[-(i + 1)]
				self.contents.blit(line,(X_MARGIN, bottom_y - line_height*i))