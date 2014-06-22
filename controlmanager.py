""" Organizes various control contexts based on the situation.
"""

from maingamecontrols import * 
from ynqcontrols import *

class ControlManager:
	""" ControlManager( Controls ) -> ControlManager

	Can hold one Controls object at a time.

	Attributes:

	Controls: current control scheme for keyboard input.

	"""

	def __init__(self, controls):
		self.current_controls = controls
		self.current_controls.control_manager = self
		self.screen = None

	def process_event(self, event):
		""" cm.process_event( Event ) -> None

		Process a python Event accordingly based on the current control scheme.
		"""
		if self.current_controls:
			self.current_controls.process_event(event)

	def switch_screen(self, screen):
		""" cm.switch_screen( GuiScreen ) -> None

		Switch the currently displayed screen.
		Not sure why this is called by self.screen,
		but we can look into it and expand this docstring
		if there is any confusion.
		"""
		self.screen.switch_screen(screen)

	def switch_controls(self, controls):
		""" cm.switch_controls( Controls )

		Change the control scheme.
		"""
		controls.control_manager = self
		self.current_controls = controls #not sure if this will work

	def deactivate_controls(self):
		""" cm.deactivate_controls( ) -> None

		Turns off controls so no input will do anything.
		"""
		self.current_controls = None

	def build_screen(self, control_manager, panes):
		""" cm.build_screen( ControlManager, [Pane]) -> GuiScreen

		Return a screen assembled from a set of panes to be displayed, along with a new control manager.
		"""
		return self.screen.build_screen(control_manager, panes)

	def build_control_manager(self, controls):
		""" cm.build_control_manager( controls ) -> ControlManager

		Creates a new ControlManager that starts with the given controls,
		but can change them afterwards if necessary.
		"""
		return ControlManager(controls)

	def exit_to_main_game_controls(self, player):
		""" cm.exit_to_main_game_controls( Player ) -> None

		Go back to the controls usually used to play the game.
		"""
		controls = MainGameControls(player)
		self.switch_controls(controls)

	def exit_to_main_game_screen(self, player):
		""" cm.exit_to_main_game_screen( Player ) -> None

		Go back to the main screen used to play the game.
		"""
		self.screen.exit_to_main_game_screen(player)