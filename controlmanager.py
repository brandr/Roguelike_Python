""" Organizes various control contexts based on the situation.
"""

from maingamecontrols import * 

class ControlManager:
	""" ControlManager( ... ) -> ControlManager

	Can hold one Controls object at a time.

	Attributes:

	Controls: current control scheme for keyboard input.

	"""

	def __init__(self, controls):
		self.current_controls = controls
		self.current_controls.control_manager = self
		self.screen = None

	def process_event(self, event):
		self.current_controls.process_event(event)

	def switch_screen(self, screen):
		self.screen.switch_screen(screen)

	def build_screen(self, control_manager, panes):
		return self.screen.build_screen(control_manager, panes)

	def build_control_manager(self, controls):
		return ControlManager(controls)

	def exit_to_main_game_screen(self, player):
		self.screen.exit_to_main_game_screen(player)