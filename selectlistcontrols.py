""" Controls for choosing something (like a spell, an item, etc.) from
a set of possiblities. """

from inventorycontrols import *
from selectlistpane import *

class SelectListControls(Controls):
	""" SelectListControls ( ... ) -> SelectListControls

	TODO

	Attributes:

	TODO
	"""
	def __init__(self, select_list, player, action, multiple = False, on_main_screen = True):
		# TODO: make it possible to select multiple objects sometimes, but not always.
		# consider other different selection modes.
		Controls.__init__(self)
		self.select_list = select_list
		self.player = player
		self.action = action
		self.multiple = multiple
		self.on_main_screen = on_main_screen
		self.control_map = SELECT_LIST_CONTROL_MAP
		length = self.select_list.length()
		for i in range(self.select_list.length()):
			letter = self.select_list.index_letter(i)	 #TODO: figure out how to handle captial letters.
			self.control_map[letter] = SelectListControls.select_object

	def select_object(self, letter): #TODO
		select_object = self.select_list.select_object_from_letter(letter)
		self.exit_to_main_game_controls() #TODO: not the case if selection should not prompt this.
		action = self.action
		action(select_object)

	def exit_to_main_game_controls(self, key = None):
		if(not self.on_main_screen):
			self.control_manager.exit_to_main_game_screen(self.player)
			return
		self.control_manager.exit_to_main_game_controls(self.player)

	def open_expanded_select_list(self, key = None):
		select_list_screen = self.select_list_screen(self.select_list)
		self.control_manager.switch_screen(select_list_screen)

	def select_list_screen(self, select_list):
		list_pane = SelectListPane(select_list) #TODO: make this class
		panes = [list_pane]
		controls = SelectListControls(self.select_list, self.player, self.action, True, False) # "True" is temporary. (it represents the ability to select multiple things)
		control_manager = self.control_manager.build_control_manager(controls)
		return self.control_manager.build_screen(control_manager, panes)
		 #TODO: open an expanded list like for forgetting spells/picking up tile items in crawl.

exit = SelectListControls.exit_to_main_game_controls
open_exanded_select_list = SelectListControls.open_expanded_select_list

SELECT_LIST_CONTROL_MAP = {
	K_ESCAPE:exit,
	'?':open_exanded_select_list,
}