""" A manager for various screens that can be displayed.
"""

from guiscreen import *

class ScreenManager:
	""" ScreenManager (...) -> ScreenManager

	TODO
	Attributes:
	
	current_screen: the current screen to be displayed. Only one may display at a time.
	"""

	def __init__(self, master_screen, current_screen):
		self.master_screen = master_screen
		self.current_screen = current_screen

	def draw_panes(self):
		self.current_screen.draw_panes(self.master_screen)

	def process_event(self, event):
		self.current_screen.control_manager.process_event(event)

	def update_current_screen(self):
		self.current_screen.update()