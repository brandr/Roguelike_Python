""" A specific screen shown in the game window at a given time.
"""

from controlmanager import *

class GuiScreen:
	""" GuiScreen( ControlManager ) -> GuiScreen

	Sends keyboard input to the control manager and shows events onscreen.

	Attributes:

	control_manager: parses input depending on the current context.
	"""

	def __init__(self, control_manager, panes):
		self.control_manager = control_manager
		self.panes = panes

	def draw_panes(self, master_screen):
		for p in self.panes:
			master_screen.blit(p.draw_pane_image(), (p.x_off, p.y_off))

	def update(self):
		for p in self.panes:
			p.update()