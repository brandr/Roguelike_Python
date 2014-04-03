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

	control_manager: parses input depending on the current context.
	"""

	def __init__(self, control_manager, panes):
		self.screen_manager = None
		self.control_manager = control_manager
		control_manager.screen = self
		self.panes = panes

	def draw_panes(self, master_screen):
		for p in self.panes:
			master_screen.blit(p.draw_pane_image(), (p.x_off, p.y_off))

	def update(self):
		for p in self.panes:
			p.update()

	def switch_screen(self, screen):
		self.screen_manager.switch_current_screen(screen)

	def build_screen(self, control_manager ,panes):
		return GuiScreen(control_manager, panes)

	def exit_to_main_game_screen(self, player):
		map_pane = MapPane(player)               
		character_pane = CharacterPane(player)
		event_pane = EventPane(player)
		main_screen_panes = [character_pane, map_pane, event_pane] 
		game_controls = MainGameControls(player)
		control_manager = ControlManager(game_controls)
		main_game_screen = GuiScreen(control_manager, main_screen_panes)
		self.screen_manager.switch_current_screen(main_game_screen)