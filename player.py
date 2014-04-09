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

	def decide_next_turn(self):
		empty = self.action_queue.empty()
		if(empty):
			return
		else:
			action = self.action_queue.dequeue_action()
			action.method(action.arg)

	def enqueue_player_action(self, method, arg, delay):
		action = Action(self, method, arg, delay)
		self.action_queue.enqueue_action(action)

	def execute_player_action(self, method, arg, delay):
		method(arg)
		self.current_level.enqueue_player_delay(self, delay)
		self.end_turn()

	def lowest_non_player_delay(self):
		return self.current_level.turn_counter.lowest_non_player_delay()

	def begin_wait(self, time):
		self.execute_player_action(self.wait, None, time)

	def wait(self, arg): #even though this method does nothing, it is still used to make the waiting process to work.
		pass

		# pick up items

	def begin_pick_up_item(self):
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

		#might not be temp anymore. Also, might want to move to Being class.
	def temp_pick_up_item(self, item):
		self.current_tile.remove_item(item)
		self.obtain_item(item)
		self.send_event("Picked up " + item.name + ".")

		# drop items

	def begin_drop_item(self, multiple = False):
		if(self.inventory.empty()):
			self.send_event("You have no items to drop.")
			return
		if(multiple):
			item_list = self.inventory.item_select_list()
			self.screen_manager.switch_to_select_list_screen(item_list, self, self.attempt_drop_item)
			#self.screen_manager.switch_to_select_list_controls(item_list, self, self.attempt_drop_item)
			return #TODO: case for dropping many items. (should probably open a selectlist screen with the "multiple" flag on, and the action set to some drop method.)
		else:
			self.drop_item_prompt()

	def drop_item_prompt(self):
		self.send_event("Drop which item?")
		item_list = self.inventory.item_select_list()
		self.screen_manager.switch_to_select_list_controls(item_list, self, self.attempt_drop_item)

	def attempt_drop_item(self, item):
		if(item.equipped):
			self.send_event("You must unequip that before dropping it.")
			return
		if(item.wielded):
			unwield_delay = 1 #TEMP
			self.execute_player_action(self.unwield_current_item, None, unwield_delay)
		drop_item_delay = 1 #TEMP
		self.execute_player_action(self.drop_item, item, drop_item_delay)

		# movement 

	def temp_move(self, direction):
		#TODO: once movement flowcharts are done, replace this method with better ones.
		dest_coords = self.coords_in_direction(direction)
		if(self.enemy_in_tile(dest_coords[0], dest_coords[1])):
			self.temp_attempt_melee_attack(self.current_level.being_in_tile(dest_coords[0], dest_coords[1]))
		elif(self.current_level.open_tile(dest_coords[0], dest_coords[1])):
			self.execute_player_action(self.move_to, dest_coords, self.move_delay)

	def temp_attempt_melee_attack(self, being):
		self.execute_player_action(self.melee_attack, being, self.attack_delay)

		# item/weapon wielding: (not equipping)

	def begin_player_wield_item(self):
		if(self.inventory.empty()):
			self.send_event("Nothing to wield.")
			return
		#TODO: check for current wielded item is cursed and stuff like that
		self.wield_item_prompt()
	
	def wield_item_prompt(self):
		self.send_event("Wield which item?")
		item_list = self.inventory.item_select_list()
		self.screen_manager.switch_to_select_list_controls(item_list, self, self.wield_item, False, False)

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
		self.screen_manager.switch_to_ynq_controls(self.confirm_replace_wield, self.cancel_replace_wield, self.cancel_replace_wield, prompt_item, self)

	def confirm_replace_wield(self, item):
		unwield_delay = 1
		wield_delay = 1
		self.execute_player_action(self.unwield_current_item, None, unwield_delay)
		self.execute_player_action(self.confirm_wield_item, item, wield_delay)

	def cancel_replace_wield(self, item):
		self.send_event("Nevermind.")

		# item/armor equipping: (not wielding)

	def begin_player_equip_item(self):
		if(not self.inventory.contains_equippables()):
			self.send_event("Nothing to equip.")
			return
		self.equip_item_prompt()
	
	def equip_item_prompt(self):
		self.send_event("Equip which item?")
		equip_list = self.inventory.equippable_item_select_list() 
		self.screen_manager.switch_to_select_list_controls(equip_list, self, self.equip_item, False, False)

	def equip_item(self, item):
		if(item.equipped):
			#TODO: check for item is cursed here.
			self.confirm_unequip(item)
			return
		if(item.wielded):
			self.send_event("You are wielding that.")
			self.send_event("I'm not sure why you're wielding something that is supposed to be armor.")
			self.send_event("Sorry, we haven't implemented that possibility yet.") #TODO: do so
			return
		slot = item.equip_slot()
		if(self.has_equipment_in_slot(slot)):
			self.unequip_item_prompt(self.equipment_in_slot(slot), item)
			return

		# TODO: check for:
		# attempting to remove chest armor while wearing a robe
		# attemping to remove gloves while wielding a cursed item
		# attemping to wield a shield with a two-handed weapon
		# other unusal cases

		equip_delay = 1 #TODO: if equip delay should be something else (it probably should), change this.
		self.execute_player_action(self.confirm_equip_item, item, equip_delay)

	def unequip_item_prompt(self, equipped_item, prompt_item):
		self.send_event("Do you want to unequip " + equipped_item.display_name()
			+ " and equip " + prompt_item.display_name() + "? (y/n/q)")
		self.screen_manager.switch_to_ynq_controls(self.confirm_replace_equip, self.cancel_replace_equip, self.cancel_replace_equip, prompt_item, self)

		#this and confirm_unequip might belong in the Being class.
	def confirm_replace_equip(self, item):
		unequip_delay = 1 	#TODO: change these to be based on the equipment itself
		equip_delay = 1
		slot = item.equip_slot()
		self.execute_player_action(self.unequip_item_in_slot, slot, unequip_delay)
		self.execute_player_action(self.confirm_equip_item, item, equip_delay)

	def confirm_unequip(self, item):
		unequip_delay = 1 #TODO: set properly
		slot = item.equip_slot()
		self.execute_player_action(self.unequip_item_in_slot, slot, unequip_delay)

	def cancel_replace_equip(self, item):
		self.send_event("Nevermind.")

