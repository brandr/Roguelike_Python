""" Controls for use in an inventory screen.
"""

from controls import *

class InventoryControls(Controls):
	""" A set of controls that apply to a player examining its or another inventory.

	attributes:

	player: the player accessing the inventory.

	inventory: the inventory the player is accessing.
	"""

	def __init__(self, player, inventory):
		Controls.__init__(self)
		self.player = player
		self.inventory = inventory
		self.control_map = INVENTORY_SCREEN_CONTROL_MAP #TODO: differentiate between player inventory screen controls and tile inventory screen controls.

exit = Controls.exit_to_main_game_screen

INVENTORY_SCREEN_CONTROL_MAP = {
	K_ESCAPE:exit
}