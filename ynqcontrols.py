""" A set of controls for a yes/no (or cancellable) action.
"""

from controls import *

class YNQControls(Controls):
	""" YNQControls( Method, ? ) -> YNQControls

	Used to allow the user to answer or cancel a yes/no question.

	Attbributes:
	yes_action: the action to peform if the user says yes.
	no_action: the action to peform if the user says no.
	arg: the argument to be used either way.
	"""
	def __init__(self, yes_action, no_action, quit_action, arg, player = None):
		Controls.__init__(self)
		self.yes_action, self.no_action, self.quit_action, self.arg = yes_action, no_action, quit_action, arg
		self.control_map = YNQ_CONTROL_MAP
		self.player = player

	def yes_action(self, key):
		self.exit_to_main_game_controls(self.player)
		self.yes_action(self.arg)

	def no_action(self, key):
		self.exit_to_main_game_controls(self.player)
		self.no_action(self.arg)

	def quit_action(self, key):
		self.exit_to_main_game_controls(self.player)
		self.quit_action(self.arg)

exit = Controls.exit_to_main_game_screen
yes = YNQControls.yes_action
no = YNQControls.no_action
quit = YNQControls.quit_action

YNQ_CONTROL_MAP = {
	'y':yes, 'Y':yes, 'n':no, 'N':no, 'q':quit, 'Q':quit
}