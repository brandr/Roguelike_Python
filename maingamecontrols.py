""" Handles the controls used when the player is in the main game.
"""
from selectlistcontrols import *
from inventoryitempane import *

class MainGameControls(Controls):
	""" MainGameControls( Player ) -> MainGameControls

	Can handle various contexts, but they should all be associated with
	the main game.

	Attributes:

	Player: the player associated with these controls.
	"""

	def __init__(self, player):
		Controls.__init__(self)
		self.player = player
		self.initialize_control_map(MAIN_GAME_CONTROL_MAP)

	def move_input(self, key):
		""" mgc.move_input( str ) -> None

		Takes some input related to movement and translates it into a move action.
		"""
		if(key in MAIN_GAME_DIRECTION_MAP):
			direction = MAIN_GAME_DIRECTION_MAP[key]
			self.player.temp_move(direction)

	def wait(self, key): #the key arg not necessary for this method, but just for program compilation.
		""" mgc.wait( str ) -> None

		The player does nothing until something happens around him.
		Might want to change this if it causes an unacceptably long wait time.
		"""
		wait_time = self.player.lowest_non_player_delay() + 1
		self.player.begin_wait(wait_time)

	def pick_up_item(self, key):
		""" mgc.pick_up_item( str ) -> None

		Tell the player to pick up one or more things in the current tile.
		"""
		self.player.begin_pick_up_item()

	def drop_item(self, key):
		""" mgc.drop_item( str ) -> None

		Tell the player to drop something in the current tile.
		"""
		self.player.begin_drop_item()

	def drop_item_multiple(self, key):
		""" mgc.drop_item_multiple( str ) -> None

		Tell the player to drop multiple things in the current tile.
		"""
		self.player.begin_drop_item(True)

	def open_player_inventory_screen(self, key):
		""" mgc.open_player_inventory_screen( str ) -> None

		Opens the player's inventory screen, closing the main screen temporarily.
		"""
		inventory_screen = self.inventory_screen(self.player.inventory)
		self.control_manager.switch_screen(inventory_screen)

	def inventory_screen(self, inventory):
		""" mgc.inventory_screen( Inventory ) -> None

		Builds an inventory screen from an inventory (the player's or a tile's, usually).
		"""
		item_pane = InventoryItemPane(inventory)
		inventory_panes = [item_pane] #TODO: other inventory panes
		inventory_controls = InventoryControls(self.player, self.player.inventory)
		inventory_control_manager = self.control_manager.build_control_manager(inventory_controls)
		return self.control_manager.build_screen(inventory_control_manager, inventory_panes)

	def wield_item(self, key):
		""" mgc.wield_itemi( str ) -> None

		Tells the player to try to wield some item.
		"""
		self.player.begin_player_wield_item()

	def equip_item(self, key):
		""" mgc.equip_item( str ) -> None

		Tells the player to try to equip some item.
		"""
		self.player.begin_player_equip_item()

	def fire_item(self, key):
		""" mgc.fire_item( str ) -> None 
		
		Tells the player to try to throw or shoot some item.
		"""
		self.player.begin_player_fire_item()	

	def quaff_item(self, key):
		""" mgc.quaff_item( str ) -> None

		Tells the player to try to quaff some item.
		"""
		self.player.begin_player_quaff_item()

drop_item = MainGameControls.drop_item
drop_item_multiple = MainGameControls.drop_item_multiple
fire_item = MainGameControls.fire_item
equip_item = MainGameControls.equip_item
move = MainGameControls.move_input
open_player_inventory_screen = MainGameControls.open_player_inventory_screen
pick_up_item = MainGameControls.pick_up_item
quaff_item = MainGameControls.quaff_item
wait = MainGameControls.wait
wield_item = MainGameControls.wield_item

MAIN_GAME_CONTROL_MAP = {
	K_UP:move, K_DOWN:move, K_LEFT:move, K_RIGHT:move,			# arrow keys

	K_KP1:move, K_KP2:move, K_KP3:move, K_KP4:move, K_KP5:move,	# numpad keys (might change 5 at some point)
	K_KP6:move, K_KP7:move, K_KP8:move, K_KP9:move,

	# inputs to open other screens

	'i':open_player_inventory_screen,

	# wait input

	'.':wait,

	# general item interaction inputs

	',':pick_up_item,
	'd':drop_item,
	'D':drop_item_multiple,
	'w':wield_item,
	'W':equip_item,
	'f':fire_item,

	# consumables

	'q':quaff_item
}

MAIN_GAME_DIRECTION_MAP = {
	K_UP:(0, -1), K_DOWN:(0, 1), K_LEFT:(-1, 0), K_RIGHT:(1,0),

	K_KP1:(-1, 1), K_KP2:(0, 1), K_KP3:(1, 1), K_KP4:(-1, 0), K_KP5:(0, 0),
	K_KP6:(1, 0), K_KP7:(-1, -1), K_KP8:(0, -1), K_KP9:(1, -1)
}
