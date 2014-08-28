""" Controls for choosing something (like a spell, an item, etc.) from
a set of possiblities. """

from inventorycontrols import *
from selectlistpane import *

class SelectListControls(Controls):
	""" SelectListControls ( SelectList, Player, Action, bool, bool, bool) -> SelectListControls

	A control scheme associated with a SelectList, used to selecte one or
	more of its contents to perform some action on.

	Attributes:

	select_list is the select_list that the associated player (player attribute) is choosing from.

	action is the Action to be performed on whatever object(s) are selected.

	multiple determines whether multiple objects can be selected.

	expand_to_multiple determines whether opening the full selectlistscreen should change the selection mode to multiple.

	on_main_screen determines whether the controls are open on the main screen or whether a special selectlistscreen is open.
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
		self.active_quantity = None
		self.on_main_screen = on_main_screen
		self.control_map = {}
		self.initialize_control_map(SELECT_LIST_CONTROL_MAP)
		length = self.select_list.length()
		for i in range(length):
			letter = self.select_list.index_letter(i)	 #TODO: figure out how to handle captial letters.
			self.control_map[letter] = SelectListControls.select_object
		for i in xrange(10):
			self.control_map[str(i)] = SelectListControls.input_number
		
	def select_object(self, letter):
		""" slc.select_object( char ) -> None

		Selects an object corresponding to the given letter.
		"""
		if(not self.multiple):
			self.select_object_single(letter)
			return
		self.select_object_multiple(letter)

	def select_object_single(self, letter):
		""" slc.select_object_single( char ) -> None

		Selects an object corresponding to the given letter
		and executes this SelectListControls's associated action upon it.
		"""
		if(letter in self.control_map):
			select_object = self.select_list.select_object_from_letter(letter) 
			#TODO: use quantity if appopriate
			self.exit_to_main_game_controls() #TODO: not the case if selection should not prompt this.
			action = self.action
			action((select_object, None))	# TODO: make sure everything can take this sort of argument.
											# TODO: make lowercase [d]rop the same as uppercase [D]rop.

	def select_object_multiple(self, letter):
		""" slc.select_object_multiple( char ) -> None

		Adds the object corresponding to the given letter to the current selection.
		"""
		if(self.on_main_screen):
			return # TEMP. Currently there is no case for multiple selections on main game screen.
		if(letter in self.control_map):
			if self.active_quantity:
				self.select_list.toggle(letter, int(self.active_quantity))
			else:
				self.select_list.toggle(letter)
			self.active_quantity = None

	def input_number(self, number):
		""" slc.input_number( str ) -> None

		Input a number (as a string) to be used for some action, like picking up/dropping that quantity of some item.
		"""
		if self.select_list.list_class != Item: return
		if self.active_quantity == None: 
			if number == '0': return
			self.active_quantity = number
			return
		if len(self.active_quantity) < 6: #NOTE: this refers to the length of the string, NOT the quantity size.
			self.active_quantity += number

	def exit_to_main_game_controls(self, key = None):
		""" slc.exit_to_main_game_controls( None ) -> None

		Stop using these controls and resume the normal game controls.
		"""
		self.player.taking_input_flag = False
		Controls.exit_to_main_game_screen(self, None)

	def open_expanded_select_list(self, key = None):
		""" slc.open_expanded_select_list( None ) -> None

		Expand the select list, opening a screen to view the objects.
		"""
		select_list_screen = self.select_list_screen(self.select_list)
		self.control_manager.switch_screen(select_list_screen)

	def confirm_selection(self, key = None):
		""" slc.confirm_selection( None ) -> None

		Apply the associated action to the currently selected object(s).
		"""
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
		""" slc.select_list_screen( SelectList ) -> GuiScreen

		Creates a selectlist screen associated with the given SelectList.
		"""
		list_pane = SelectListPane(select_list)
		panes = [list_pane]
		controls = SelectListControls(self.select_list, self.player, self.action, self.expand_to_multiple, False, False) 
		control_manager = self.control_manager.build_control_manager(controls)
		return self.control_manager.build_screen(control_manager, panes)


confirm_selection = SelectListControls.confirm_selection
exit = SelectListControls.exit_to_main_game_controls
open_exanded_select_list = SelectListControls.open_expanded_select_list

SELECT_LIST_CONTROL_MAP = {
	K_ESCAPE:exit,
	K_SPACE: exit,
	'?':open_exanded_select_list,
	K_RETURN:confirm_selection
}
