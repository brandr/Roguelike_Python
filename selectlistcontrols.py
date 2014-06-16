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
	def __init__(self, select_list, player, action, multiple = False, expand_to_multiple = True, on_main_screen = True):
		# TODO: make it possible to select multiple objects sometimes, but not always.
		# consider other different selection modes.
		Controls.__init__(self)
		self.select_list = select_list
		self.player = player
		self.action = action
		self.multiple = multiple
		self.expand_to_multiple = expand_to_multiple
		self.on_main_screen = on_main_screen
		self.control_map = {}
		self.initialize_control_map(SELECT_LIST_CONTROL_MAP)
		length = self.select_list.length()
		for i in range(length):
			letter = self.select_list.index_letter(i)	 #TODO: figure out how to handle captial letters.
			self.control_map[letter] = SelectListControls.select_object
		
	def select_object(self, letter):
		if(not self.multiple):
			self.select_object_single(letter)
			return
		self.select_object_multiple(letter)

	def select_object_single(self, letter):
		if(letter in self.control_map):
			select_object = self.select_list.select_object_from_letter(letter)
			self.exit_to_main_game_controls() #TODO: not the case if selection should not prompt this.
			action = self.action
			action(select_object)

	def select_object_multiple(self, letter):
		if(self.on_main_screen):
			return #TEMP. Currently there is no case for multiple selections on main game screen.
		if(letter in self.control_map):
			self.select_list.toggle(letter)

	def exit_to_main_game_controls(self, key = None):
		self.player.taking_input_flag = False
		if(not self.on_main_screen):
			Controls.exit_to_main_game_screen(self, None)
			return
		Controls.exit_to_main_game_controls(self, None)

	def open_expanded_select_list(self, key = None):
		select_list_screen = self.select_list_screen(self.select_list)
		self.control_manager.switch_screen(select_list_screen)

	def confirm_selection(self, key = None):
		self.exit_to_main_game_controls()

		toggles = self.select_list.toggles
		toggle_length = len(toggles)
		toggle_index = 0
		toggled_objects = self.select_list.toggled_objects()
		length = len(toggled_objects)
		action = self.action

		if(toggled_objects):
			first_object = toggled_objects[0]	
			action(first_object)
			for i in range(1, length):
				o = toggled_objects[i]
				self.player.enqueue_player_action(action, o, 1) #TEMP	
			self.player.decide_next_turn()			

	def select_list_screen(self, select_list):
		list_pane = SelectListPane(select_list)
		panes = [list_pane]
		controls = SelectListControls(self.select_list, self.player, self.action, self.expand_to_multiple, False, False) 
		control_manager = self.control_manager.build_control_manager(controls)
		return self.control_manager.build_screen(control_manager, panes)
		 #TODO: open an expanded list like for forgetting spells/picking up tile items in crawl.

confirm_selection = SelectListControls.confirm_selection
exit = SelectListControls.exit_to_main_game_controls
open_exanded_select_list = SelectListControls.open_expanded_select_list

SELECT_LIST_CONTROL_MAP = {
	K_ESCAPE:exit,
	'?':open_exanded_select_list,
	K_RETURN:confirm_selection
}