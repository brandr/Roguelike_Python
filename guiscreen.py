""" A specific screen shown in the game window at a given time.
"""

from controlmanager import *
from characterpane import *
from eventpane import *
from mappane import *

class GuiScreen:
	""" GuiScreen( ControlManager ) -> GuiScreen

	Sends keyboard input to the control manager and shows events onscreen.

	Attributes:

	screen_manager: the ScreenManager controlling this guiscreen.
	control_manager: parses input depending on the current context.
	panes: Visual panes that appear on the screen.
	"""

	def __init__(self, control_manager, panes):
		self.screen_manager = None
		self.control_manager = control_manager
		control_manager.screen = self
		self.panes = panes

	def draw_panes(self, master_screen):
		""" gs.draw_panes( Surface ) -> None

		Update the screen by drawing panes onto a pygame screen.
		"""
		for p in self.panes:
			master_screen.blit(p.draw_pane_image(), (p.x_off, p.y_off))

	def update(self):
		""" gs.update( ) -> None

		updates each of this screen's panes.
		Updating means something different for different panes.
		"""
		for p in self.panes:
			p.update()

	def switch_screen(self, screen):
		""" gs.switch_screen( GuiScreen) -> None

		Switch from displaying this screen to another one.
		"""
		self.screen_manager.switch_current_screen(screen)

	def switch_controls(self, controls):
		""" gs.switch_controls( Controls ) -> None

		Change the control scheme used by this screen.
		"""
		self.control_manager.switch_controls(controls)

	def deactivate_controls(self):
		""" gs.deactivate_controls( ) -> None

		Turns off controls so no input will do anything.
		"""
		self.control_manager.deactivate_controls()

	def build_screen(self, control_manager, panes):
		""" gs.build_screen( ControlManager, [Pane] ) -> GuiScreen

		Creates a new GuiScreen with the given control manager (and its controls)
		along with the given panes.
		"""
		return GuiScreen(control_manager, panes)

	def exit_to_main_game_screen(self, player):
		""" gs.exit_to_main_game_screen( Player ) -> None

		Leave this screen and switch to the main screen used to play the game.
		""" 
		map_pane = MapPane(player)               
		character_pane = CharacterPane(player)
		event_pane = EventPane(player)
		main_screen_panes = [character_pane, map_pane, event_pane] 
		game_controls = MainGameControls(player)
		control_manager = ControlManager(game_controls)
		main_game_screen = GuiScreen(control_manager, main_screen_panes)
		self.screen_manager.switch_current_screen(main_game_screen)