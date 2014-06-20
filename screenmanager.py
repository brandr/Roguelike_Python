""" A manager for various screens that can be displayed.
"""

from guiscreen import *

class ScreenManager:
	""" ScreenManager (...) -> ScreenManager

	The screenmanager conveys information between a GuiScreen object, a control manager,
	and a pygame master screen.

	Attributes:
	
	master_screen: a pygame screen to blit the display onto
	current_screen: the current screen to be displayed. Only one may display at a time.
	player: the player associated with the screen manager
	"""

	def __init__(self, master_screen, current_screen, player = None):
		self.master_screen = master_screen
		self.set_current_screen(current_screen)
		self.player = player
		if(player != None):
			player.screen_manager = self

	def set_current_screen(self, screen):
		""" sm.set_current_screen( GuiScreen ) -> None

		Associate this screen manager with the given screen.
		"""
		self.current_screen = screen
		screen.screen_manager = self

	def switch_controls(self, controls):
		""" sm.switch_controls( Controls ) -> None

		Associate this screen manager with the given controls.
		"""
		self.current_screen.switch_controls(controls)

	def draw_panes(self):
		""" sm.draw_panes( ) -> None

		Redraw the current panes on the screen.
		"""
		self.current_screen.draw_panes(self.master_screen)

	def process_event(self, event):
		""" sm.process_event( Event ) -> None

		Send the given pygame Event to the control manager.
		"""
		self.current_screen.control_manager.process_event(event)

	def update_current_screen(self):
		""" sm.update_current_screen( ) -> None

		Tell the current screen to refresh its contents.
		"""
		self.current_screen.update()

	def switch_current_screen(self, screen):
		""" sm.set_current_screen( GuiScreen ) -> None

		Switch this screen manager to the given screen.
		"""
		self.clear_all_panes()
		self.set_current_screen(screen)

	def clear_all_panes(self):
		""" sm.clear_all_panes( ) -> None

		Fill all panes of the current screen with black.
		"""
		dark = Surface((self.master_screen.get_width(), self.master_screen.get_height()))
		self.master_screen.blit(dark, (0, 0))

	def switch_to_select_list_screen(self, select_list, player, action, multiple = True): 
		""" sm.switch_to_select_list_screen( SelectList, Player, Action, Bool ) -> None

		Switch to a screen showing the given select list, to have the given Action
		performed on one or more things from the SelectList that are selected.
		"""
		controls = SelectListControls(select_list, player, action, False, multiple)
		self.switch_controls(controls)
		controls.open_expanded_select_list()

		#select_screen = SelectListScreen(select_list, player, action)

	def switch_to_select_list_controls(self, select_list, player, action, multiple = False, expand_to_multiple = True):
		""" sm.switch_to_select_list_controls( SelectList, Player, Action, Bool, Bool) -> None

		Similar to switch_to_select_list_screen, but doesn't change the screen.
		"""
		player.taking_input_flag = True
		controls = SelectListControls(select_list, player, action, multiple, expand_to_multiple)
		self.switch_controls(controls)
		list_message = select_list.list_message()
		level = player.current_level
		level.send_event(list_message)

	def switch_to_ynq_controls(self, yes_action, no_action, quit_action, arg, player = None): #TODO: consider what may be necessary when there are multiple args. (tuplets maybe?)
		""" sm.switch_to_ynq_controls( Action, Action, Action, Player ) -> None

		Switch to a controls that allow the player to answer a yes or no question.
		"""
		player.taking_input_flag = True
		controls = YNQControls(yes_action, no_action, quit_action, arg, player)
		self.switch_controls(controls)