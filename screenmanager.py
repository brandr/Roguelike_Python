""" A manager for various screens that can be displayed.
"""

from guiscreen import *

class ScreenManager:
	""" ScreenManager (...) -> ScreenManager

	TODO
	Attributes:
	
	current_screen: the current screen to be displayed. Only one may display at a time.
	"""

	def __init__(self, master_screen, current_screen, player = None):
		self.master_screen = master_screen
		self.set_current_screen(current_screen)
		self.player = player
		if(player != None):
			player.screen_manager = self

	def set_current_screen(self, screen):
		self.current_screen = screen
		screen.screen_manager = self

	def switch_controls(self, controls):
		self.current_screen.switch_controls(controls)

	def draw_panes(self):
		self.current_screen.draw_panes(self.master_screen)

	def process_event(self, event):
		self.current_screen.control_manager.process_event(event)

	def update_current_screen(self):
		self.current_screen.update()

	def switch_current_screen(self, screen):
		self.clear_all_panes()
		self.set_current_screen(screen)

	def clear_all_panes(self):
		dark = Surface((self.master_screen.get_width(), self.master_screen.get_height()))
		self.master_screen.blit(dark, (0, 0))

	def switch_to_select_list_screen(self, select_list, player, action): 
		select_screen = SelectListScreen(select_list, player, action)

	def switch_to_select_list_controls(self, select_list, player, action):
		controls = SelectListControls(select_list, player, action)
		self.switch_controls(controls)
		list_message = select_list.list_message()
		level = player.current_level
		level.send_event(list_message)

	def switch_to_ynq_controls(self, yes_action, no_action, arg, player = None): #TODO: consider what may be necessary when there are multiple args. (tuplets maybe?)
		controls = YNQControls(yes_action, no_action, arg, player)
		self.switch_controls(controls)