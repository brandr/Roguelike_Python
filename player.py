""" A representation of the player playing the game. The hero that procedurally generated
dungeons deserve.
"""

from being import *
#from maingamecontrols import *

PLAYER_SYMBOL = '@'
PLAYER_COLOR = Color("#FF0000")


class Player(Being): 
	""" Player ( ... ) -> Player

	TODO: docstring
	"""

	def __init__(self, name): #TODO: figure out how player should actually be created
		Being.__init__(self, name)
		self.screen_manager = None #TODO: consider giving monsters an attribute for the screen, too
		self.equipment_set = EquipmentSet(HUMANOID) #TODO: change this if the player can be a non-humanoid.
		self.hit_points = (10, 10)
		self.magic_points = (8, 8)
		self.move_delay = 4
		self.attack_delay = 3
		self.event_pane = None
		self.melee_range = 1 #TEMP

	def display_name(self): #TODO: change for different cases
		return "You"

	def start_game(self):
		self.send_event("Welcome to the dungeon!") #TEMP

	def send_event(self, message):
		self.event_pane.display(message)

	def current_symbol(self):
		return PLAYER_SYMBOL

	def color(self):
		return PLAYER_COLOR

	def hp_display(self):
		return str(self.hit_points[0]) + "/" + str(self.hit_points[1])

	def mp_display(self):
		return str(self.magic_points[0]) + "/" + str(self.magic_points[1])

	def begin_wait(self, time):
		self.execute_player_action(self.wait, None, time)

	def wait(self, arg): #even though this method does nothing, it still seems to be necessary.
		pass

	def begin_pick_up(self):
		if(not self.current_tile.contains_items()):
			self.send_event("Nothing to pick up.")
			return
		if(self.current_tile.item_count() == 1):
			item = self.current_tile.top_item()
			self.pick_up_tile_item(item)
			return
		self.pick_up_prompt()

	def pick_up_prompt(self):
		self.send_event("Pick up which item?")
		item_list = self.current_tile.tile_item_select_list()
		tile_items = self.current_tile.tile_items
		self.screen_manager.switch_to_select_list_controls(item_list, self, self.pick_up_tile_item)
		
	def pick_up_tile_item(self, item):
		pick_up_delay = 1 #TODO: derive this from something if it should vary based on the situation.
		self.execute_player_action(self.temp_pick_up_item, item, pick_up_delay)

		#might not be temp anymore
	def temp_pick_up_item(self, item):
		self.current_tile.remove_item(item)
		self.obtain_item(item)
		self.send_event("Picked up " + item.name + ".")

	def temp_move(self, direction):
		#TODO: once movement flowcharts are done, replace this method with better ones.
		dest_coords = self.coords_in_direction(direction)
		if(self.enemy_in_tile(dest_coords[0], dest_coords[1])):
			self.temp_attempt_melee_attack(self.current_level.being_in_tile(dest_coords[0], dest_coords[1]))
		elif(self.current_level.open_tile(dest_coords[0], dest_coords[1])):
			self.execute_player_action(self.move_to, dest_coords, self.move_delay)

	def temp_attempt_melee_attack(self, being):
		self.execute_player_action(self.melee_attack, being, self.attack_delay)

	def begin_player_wield_item(self):
		if(self.inventory.empty()):
			self.send_event("Nothing to wield.")
			return
		#TODO: check for current wielded item is cursed and stuff like that
		self.wield_item_prompt()
	
	def wield_item_prompt(self):
		self.send_event("Wield which item?")
		item_list = self.inventory.item_select_list()
		self.screen_manager.switch_to_select_list_controls(item_list, self, self.wield_item)

	def wield_item(self, item):
		if(item.wielded):
			self.send_event("You are already wielding that!")
			return
		if(item.equipped):
			self.send_event("You are wearing that.")
			self.send_event("Use w to wield weapons and W to equip or unequip armor.")
			return
		if(self.wielding_item()):
			self.unwield_item_prompt(self.wielded_item(), item)
			return
		# TODO: check for:
		# attempting to wield a two-handed weapon with a shield
		# attempting to wield known cursed item
		# other unusual cases
		wield_delay = 1 #TODO: if wield delay should be something else,  change this.
		self.execute_player_action(self.confirm_wield_item, item, wield_delay)

	def unwield_item_prompt(self, wielded_item, prompt_item):
		self.send_event("Do you want to unwield " + wielded_item.display_name()
			+ " and wield " + prompt_item.display_name() + "? (y/n/q)")
		self.screen_manager.switch_to_ynq_controls(self.confirm_replace_wield, self.cancel_replace_wield, prompt_item, self)

	def confirm_replace_wield(self, item):
		unwield_delay = 1
		wield_delay = 1
		self.execute_player_action(self.unwield_current_item, None, unwield_delay)
		self.execute_player_action(self.confirm_wield_item, item, wield_delay)

	def cancel_replace_wield(self, item):
		self.send_event("Nevermind.")
	
	def execute_player_action(self, action, arg, delay):
		action(arg)
		self.current_level.enqueue_player_delay(self, delay)
		self.end_turn()

	def lowest_non_player_delay(self):
		return self.current_level.turn_counter.lowest_non_player_delay()