""" Handles the controls used when the player is in the main game.
"""
from selectlistcontrols import *
from inventoryitempane import *

class MainGameControls(Controls):
	""" MainGameControls( Player ) -> MainGameControls

	Can handlre various contexts, but they should all be associated with
	the main game.

	Attributes:

	Player: the player associated with these controls. 
	"""

	def __init__(self, player):
		Controls.__init__(self)
		self.player = player
		self.control_map = MAIN_GAME_CONTROL_MAP

	def move_input(self, key):
		if(key in MAIN_GAME_DIRECTION_MAP):
			direction = MAIN_GAME_DIRECTION_MAP[key]
			self.player.temp_move(direction)

	def wait(self, key): #the key arg not necessary for this method, but just for program compilation.
		wait_time = self.player.lowest_non_player_delay() + 1
		self.player.begin_wait(wait_time)

	def pick_up(self, key):
		self.player.begin_pick_up()

	def open_player_inventory_screen(self, key):
		inventory_screen = self.inventory_screen(self.player.inventory)
		self.control_manager.switch_screen(inventory_screen)

	def inventory_screen(self, inventory):
		item_pane = InventoryItemPane(inventory)
		inventory_panes = [item_pane] #TODO: other inventory panes
		inventory_controls = InventoryControls(self.player, self.player.inventory)
		inventory_control_manager = self.control_manager.build_control_manager(inventory_controls)
		return self.control_manager.build_screen(inventory_control_manager, inventory_panes)
	
move = MainGameControls.move_input
wait = MainGameControls.wait
pick_up = MainGameControls.pick_up
open_player_inventory_screen = MainGameControls.open_player_inventory_screen

MAIN_GAME_CONTROL_MAP = { 
	K_UP:move, K_DOWN:move, K_LEFT:move, K_RIGHT:move,			# arrow keys

	K_KP1:move, K_KP2:move, K_KP3:move, K_KP4:move, K_KP5:move,	# numpad keys (might change 5 at some point)
	K_KP6:move, K_KP7:move, K_KP8:move, K_KP9:move,

	K_PERIOD:wait,

	K_COMMA:pick_up,

	K_i:open_player_inventory_screen
}

MAIN_GAME_DIRECTION_MAP = {
	K_UP:(0, -1), K_DOWN:(0, 1), K_LEFT:(-1, 0), K_RIGHT:(1,0),

	K_KP1:(-1, 1), K_KP2:(0, 1), K_KP3:(1, 1), K_KP4:(-1, 0), K_KP5:(0, 0), 
	K_KP6:(1, 0), K_KP7:(-1, -1), K_KP8:(0, -1), K_KP9:(1, -1)
} 