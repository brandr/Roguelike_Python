""" A representation of the player playing the game. The hero that procedurally generated
dungeons deserve.
"""

from being import *
from projectile import *
from equipmentset import EquipmentSet
#from targetcontrols import SMITE, LINE

PLAYER_SYMBOL = '@'
PLAYER_COLOR = Color("#FF0000")

SMITE = "smite"
LINE = "line"

class Player(Being):
	""" Player ( ... ) -> Player

	The player is a special type of Being that can only act if it receives user input
	or if it has some special queued actions.

	Attributes:

	screen_manager is a commanding object which controls the screen the player is on.

	equipment_set contains all of the player's currently equipped items.

	hit_points is [current_hp, max_hp] and the player dies when current_hp is 0 or lower.

	current_action is a string explaining what the player is doing (in terms of queued actions).

	move_delay is how long the player must wait after moving before acting again.

	attack_delay is how long the player must wait after attacking before acting again.

	event_pane is a visual text pane explaining what is happening to and around the player.

	melee_range is how far away the player can reach with a melee attack.
	It should really be dervied from the player's current weapon, though.

	taking_input_flag checks whether the game is waiting for some input besides the main game controls.
	"""

	def __init__(self, name): #TODO: figure out how player should actually be created
		Being.__init__(self, name)
		self.screen_manager = None #TODO: consider giving monsters an attribute for the screen, too
		self.equipment_set = EquipmentSet(HUMANOID) #TODO: change this if the player can be a non-humanoid.
		self.hit_points = [20, 20] #TEMP. (so are other attributes, until player creation is implented)
		self.magic_points = [8, 8]
		self.current_action = "SURROUNDINGS"
		self.move_delay = 4
		#self.attack_delay = 3
		self.event_pane = None
		self.taking_input_flag = False
		self.name = "Link"

	def display_name(self): #TODO: change for different cases
		""" p.display_name( ) -> str

		What the player's name should display as in the event pane.
		"""
		return "You"

	def set_current_action(self, name):
		""" p.set_current_action( str ) -> None

		Mutator for current_action.
		"""
		self.current_action = name

	def get_current_action(self):
		""" p.get( str ) -> None

		Accessor for current_action.
		"""
		return self.current_action

	def start_game(self):
		""" p.start_game( ) -> None

		Handles things that should happen when the player arrives in the dungeon.
		(Not all of them are handled here, though.)
		"""
		self.send_event("Welcome to the dungeon!") #TEMP

	def send_event(self, message):
		""" p.send_event( str ) -> None

		Display some message on the event pane.
		"""
		self.event_pane.display(message)

	def current_symbol(self):
		""" p.current_symbol( ) -> char

		Gives the symbol that should be used to represent the player on the map.
		"""
		return PLAYER_SYMBOL

	def color(self):
		""" p.color( ) -> Color

		Gives the color that should be used to represent the player on the map.
		"""
		return PLAYER_COLOR

	def hp_display(self):
		""" p.hp_display( ) -> str

		Gives the string that should be used to represent the player's hp.
		"""
		return str(self.hit_points[0]) + "/" + str(self.hit_points[1])

	def mp_display(self):
		""" p.mp_display( ) -> str

		Gives the string that should be used to represent the player's mp.
		"""
		return str(self.magic_points[0]) + "/" + str(self.magic_points[1])

	def decide_next_turn(self, arg = None):
		""" p.decide_next_turn( None ) -> None

		The player either executes its next queued action or waits for user input.
		"""
		if(self.action_queue.empty() or self.taking_input_flag):
			return
		else:
			action = self.action_queue.dequeue_action()
			action.method(action.arg)
			self.current_level.enqueue_player_delay(self, action.delay)

	def enqueue_player_action(self, method, arg, delay):
		""" p.enqueue_player_action( Method, ?, int ) -> None

		The player puts an action in the action queue to be executed later.
		"""
		action = Action(self, method, arg, delay)
		self.action_queue.enqueue_action(action)

	def execute_player_action(self, method, arg, delay):
		""" p.execute_player_action( Method, ?, int ) -> None

		The player performs an action and then must wait before actincg again.
		"""
		method(arg)
		self.current_level.enqueue_player_delay(self, delay)
		self.end_turn()

	def execute_first_queued_action(self):
		""" p.execute_first_queued_action( ) -> None

		Executes the next action in the player's action queue.
		"""
		action = self.action_queue.dequeue_action()
		action.method(action.arg)
		self.current_level.enqueue_player_delay(self, action.delay)
		self.end_turn()

	def lowest_non_player_delay(self):
		""" p.lowest_non_player_delay( ) -> None

		Gives the delay of the actor that will act soonest (besides the player).
		"""
		return self.current_level.turn_counter.lowest_non_player_delay()

	def cancel_action_message(self):
		""" p.cancel_action_message( ) -> None

		Tell the player that an action was cancelled.
		"""
		self.send_event("Nevermind")

		#TODO: consider trying to move a lot of stuff to Being if it helps.

	def begin_wait(self, time):
		""" p.begin_wait( int ) -> None

		The player does nothing for the given amount of time.
		"""
		self.execute_player_action(self.wait, None, time)

	def wait(self, arg): #even though this method does nothing, it is still used to make the waiting process to work.
		""" p.wait( None ) -> None

		The player does nothing. (regen/hunger might occur here later, though.)
		"""
		pass

	def take_damage(self, damage):
		""" p.take_damage( int ) -> None

		The player takes the given amount of damage.
		"""
		Being.take_damage(self, damage)
		if(not self.action_queue.empty()):
			self.send_event("Continue " + self.get_current_action() + " while under attack (y/n/q)?")
			self.screen_manager.switch_to_ynq_controls(self.decide_next_turn, self.clear_action_queue,  self.clear_action_queue, None, self)

		# throw or shoot items

	def begin_player_fire_item(self):
		""" p.begin_player_fire_item( ) -> None

		The player attemps to throw or shoot something.
		"""
		if(self.inventory.empty()):
			self.send_event("You have no items to throw.")
			return
		self.fire_item_prompt()

	def fire_item_prompt(self):
		""" p.throw_item_prompt( ) -> None

		The player is prompted to throw or shoot something.
		"""
		self.send_event("Shoot or throw which item?")
		item_list = self.inventory.item_select_list()
		self.screen_manager.switch_to_select_list_controls(item_list, self, self.attempt_fire_item)

	def attempt_fire_item(self, item):
		""" p.attempt_fire_item( ( Item, int ) ) -> None

		The player attemps to throw or shoot the given item.
		"""
		throw_item = item[0]
		if(throw_item.equipped):
			self.send_event("You must unequip that before throwing it.")
			return
		if(throw_item.wielded):
			unwield_delay = 1 #TEMP
			self.execute_player_action(self.unwield_current_item, None, unwield_delay)
			self.enqueue_player_action(self.attempt_fire_item, throw_item, 0)
			return
		self.fire_item_target_prompt(throw_item)

	def fire_item_target_prompt(self, item):
		""" p.fire_item_target_prompt( Item ) -> None

		Prompt the player to choose a target for a fired item.
		"""
		self.send_event("Choose a target.")
		action_range = 10 		#TEMP. should be line of sight
		target_style = LINE 	#TEMP. figure out how to derive the constant
		self.screen_manager.switch_to_target_controls(self.final_fire_item_checks, action_range, target_style, self, item)
		#TODO: make sure the above method works.

	def final_fire_item_checks(self, item, target_x, target_y): 
		""" p.final_fire_item_checks( Item, int, int ) -> None

		Perform the final checks before firisng an item.
		"""
		projectile_path = self.current_level.tile_line(self.current_tile, self.current_level.tile_at(target_x, target_y))
		if projectile_path[-1] == self.current_tile:
			self.fire_target_self_prompt(item, projectile_path)
			return
		#TODO: final checks go here (trying fire at self and that sort of thing)
		self.confirm_fire_item((item, projectile_path))

	def fire_target_self_prompt(self, item, projectile_path):
		""" p.fire_target_self_prompt( Item, [Tile] ) -> None

		The player is prompted to target himself with some target firing.
		"""
		self.send_event("Really target yourself? (y/n/q)")
		self.screen_manager.switch_to_ynq_controls(self.confirm_fire_item, self.cancel_action_message, self.cancel_action_message, (item, projectile_path), self)
		
	def confirm_fire_item(self, (item, projectile_path)):
		""" p.confirm_fire_item( (Item, [Tile] ) ) -> None

		Confirm firing the item and calculate the proper delay.
		"""
		self.screen_manager.deactivate_controls()
		fire_delay = 1 #TEMP. Figure out how long a throw should take somehow.
		self.execute_player_action(self.fire_item, (item, projectile_path), fire_delay)

	def fire_item(self, (item, projectile_path)):
		""" p.fire_item( ( Item, [Tile] ) ) -> None

		Throw or shoot some item at the target coordinates.
		""" 
		self.inventory.decrement_item(item, 1)
		fired_item = item.create_copy(1)
		projectile = Projectile(fired_item, projectile_path, self)
		self.current_level.add_projectile(projectile)
		
		# pick up items

	def begin_pick_up_item(self):
		""" p.begin_pick_up_item( ) -> None

		The player attemps to pick up the items in its tile.
		"""
		if(not self.current_tile.contains_items()):
			self.send_event("Nothing to pick up.")
			return
		if(self.current_tile.item_count() == 1):
			item = self.current_tile.top_item()
			self.pick_up_tile_item((item, None))
			return
		self.pick_up_prompt()

	def pick_up_prompt(self):
		""" p.pick_up_prompt( ) -> None

		The player is prompted about which item to pick up.
		"""
		self.send_event("Pick up which item?")
		item_list = self.current_tile.tile_item_select_list()
		tile_items = self.current_tile.tile_items
		self.screen_manager.switch_to_select_list_controls(item_list, self, self.pick_up_tile_item)

	def pick_up_tile_item(self, item):
		""" p.pick_up_tile_item( Item ) -> None

		The player picks up the given item from the current tile.
		"""
		pick_up_delay = 1 #TODO: derive this from something if it should vary based on the situation.
		self.execute_player_action(self.pick_up_item, item, pick_up_delay)

		#might not be temp anymore. Also, might want to move to Being class.
	def pick_up_item(self, (item, quantity)):
		""" p.pick_up_item( ( Item, int ) ) -> None

		Picks up the given amount of the given item from the given tile.
		"""
		pickup_quantity = min(item.current_quantity(), quantity)
		pickup_item = item.create_copy(pickup_quantity)
		self.inventory.add_item(pickup_item)
		self.current_tile.tile_items.decrement_item(item, pickup_quantity)
		self.send_event(self.display_name() + " picked up " + pickup_item.display_name() + ".")

		# drop items

	def begin_drop_item(self, multiple = False):
		""" p.begin_drop_item( bool ) -> None

		The player attemps to drop one or more items into the current tile.
		"""
		self.set_current_action("dropping things")
		if(self.inventory.empty()):
			self.send_event("You have no items to drop.")
			return
		if(multiple):
			item_list = self.inventory.item_select_list()
			self.screen_manager.switch_to_select_list_screen(item_list, self, self.attempt_drop_item)
			return
		else:
			self.drop_item_prompt()

	def drop_item_prompt(self):
		""" p.drop_item_prompt( ) -> None

		The player is propted about which item to drop.
		"""
		self.send_event("Drop which item?")
		item_list = self.inventory.item_select_list()
		self.screen_manager.switch_to_select_list_controls(item_list, self, self.attempt_drop_item)

	def attempt_drop_item(self, item_stack):
		""" p.attempt_drop_item( ( Item, int ) ) -> None

		The player attemps to drop the given item.
		"""
		item = item_stack[0]
		quantity = item_stack[1]
		if(item.equipped):
			self.send_event("You must unequip that before dropping it.")
			return
		if(item.wielded):
			unwield_delay = 1 #TEMP
			self.execute_player_action(self.unwield_current_item, None, unwield_delay)
			drop_item_delay = 1 #TEMP
			self.enqueue_player_action(self.drop_item, (item, quantity), drop_item_delay)
			return
		drop_item_delay = 1 #TEMP
		self.execute_player_action(self.drop_item, (item, quantity), drop_item_delay)

		# movement

	def temp_move(self, direction):
		# no docstring because temp
		#TODO: once movement flowcharts are done, replace this method with better ones.
		dest_coords = self.coords_in_direction(direction)
		if(self.enemy_in_tile(dest_coords[0], dest_coords[1])):
			self.temp_attempt_melee_attack(self.current_level.being_in_tile(dest_coords[0], dest_coords[1]))
		elif(self.current_level.open_tile(dest_coords[0], dest_coords[1])):
			self.execute_player_action(self.move_to, dest_coords, self.move_delay)

	def temp_attempt_melee_attack(self, being):
		self.execute_player_action(self.melee_attack, being, self.melee_attack_delay())

		# item/weapon wielding: (not equipping)

	def begin_player_wield_item(self):
		""" p.begin_player_wield_item( ) -> None

		The player begins trying to wield something.
		"""
		if(self.inventory.empty()):
			self.send_event("Nothing to wield.")
			return
		#TODO: check for current wielded item is cursed and stuff like that
		self.wield_item_prompt()

	def wield_item_prompt(self):
		""" p.wield_item_prompt( ) -> None

		The player is prompted about what item to wield.
		"""
		self.send_event("Wield which item?")
		item_list = self.inventory.item_select_list()
		self.screen_manager.switch_to_select_list_controls(item_list, self, self.wield_item, False, False)

		# some of this might be moveable to Being, but not sure.
	def wield_item(self, item):
		""" p.wield_item( Item ) -> None

		The player wields the given item if possible.
		"""
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
		if item.two_handed and self.equipment_set.item_is_in_slot(LEFT_HAND_SLOT): # case for attempting to wield a two-handed weapon with a shield. NOTE: this won't work for non-humanoids.
			wield_delay = 1
			self.enqueue_player_action(self.confirm_wield_item, item, wield_delay)
			unequip_delay = 1
			self.execute_player_action(self.unequip_item_in_slot, LEFT_HAND_SLOT, unequip_delay)
			return
		wield_delay = 1 #TODO: if wield delay should be something else,  change this.
		self.execute_player_action(self.confirm_wield_item, item, wield_delay)

	def unwield_item_prompt(self, wielded_item, prompt_item):
		""" p.unwield_item_prompt( Item, Item ) -> None

		The player is prompted to unwield its current item in favor of another one.
		"""
		self.send_event("Do you want to unwield " + wielded_item.display_name() + " and wield " + prompt_item.display_name() + "? (y/n/q)")
		self.screen_manager.switch_to_ynq_controls(self.confirm_replace_wield, self.cancel_action_message, self.cancel_action_message, prompt_item, self)

	def confirm_replace_wield(self, item):
		""" p.confirm_replace_wield( Item ) -> None

		The player unequips one it
		"""
		unwield_delay = 1
		wield_delay = 1
		if item.two_handed and self.equipment_set.item_is_in_slot(LEFT_HAND_SLOT):
			unequip_delay = 1
			self.enqueue_player_action(self.unequip_item_in_slot, LEFT_HAND_SLOT, unequip_delay)
		self.enqueue_player_action(self.confirm_wield_item, item, wield_delay)
		self.execute_player_action(self.unwield_current_item, None, unwield_delay)


	def cancel_replace_wield(self, item):
		""" p.cancel_replace_wield( Item ) -> None

		The player decides not to wierd the given item.
		"""
		self.send_event("Nevermind.")

		# item/armor equipping: (not wielding)

	def begin_player_equip_item(self):
		""" p.begin_player_equip_item( ) -> None

		The player begins trying to equip something.
		"""
		if(not self.inventory.contains_equippables()):
			self.send_event("Nothing to equip.")
			return
		self.equip_item_prompt()

	def equip_item_prompt(self):
		""" p.equip_item_prompt( ) -> None

		The player is prompted to choose an item to equip.
		"""
		self.send_event("Equip which item?")
		equip_list = self.inventory.equippable_item_select_list()
		self.screen_manager.switch_to_select_list_controls(equip_list, self, self.equip_item, False, False)

	def equip_item(self, item):
		""" p.equip_item( Item ) -> None

		The player attemps to equip the given item.
		"""
		self.current_action = "changing equipment"
		if(item.equipped):
			#TODO: check for item is cursed here.
			equipment = item
			slot = equipment.equip_slot()
			blocking_equipment = self.equipment_set.blocking_equipment(slot)
			if not blocking_equipment:
				unequip_delay = 1 #TEMP
				self.execute_player_action(self.unequip_item_in_slot, slot, unequip_delay)
				return
			self.change_equip_blocked_item(equipment, slot, blocking_equipment, True)
			return
		if(item.wielded):
			self.send_event("You are wielding that.")
			self.send_event("I'm not sure why you're wielding something that is supposed to be armor.")
			self.send_event("Sorry, we haven't implemented that possibility yet.") #TODO: do so
			return
		slot = item.equip_slot()
		if(self.has_equipment_in_slot(slot)): #TODO: figure out how this will work with new system
			self.unequip_item_prompt(self.equipment_in_slot(slot), item)
			return

		# TODO: make sure the system is robust enough to deal with:
		# attempting to remove chest armor while wearing a cloak
		# attemping to remove gloves while wielding a cursed item
		# attemping to wield a shield with a two-handed weapon
		# other unusal cases

		equipment = item
		slot = equipment.equip_slot()
		blocking_equipment = self.equipment_set.blocking_equipment(slot)
		if not blocking_equipment:
			equip_delay = 1 #TODO: if equip delay should be something else (it probably should), change this.
			self.execute_player_action(self.confirm_equip_item, equipment, equip_delay)
			return
		self.change_equip_blocked_item(equipment, slot, blocking_equipment, False)
		

	def change_equip_blocked_item(self, target_equipment, slot, blocking_equipment, unequip, replace_item = None):
		#TODO: make this more general so that it can also apply to equipping a blocked item
		unequip_queue = []
		equipment = None
		for b in blocking_equipment:
			if b:
				equipment = b	
				unequip_delay = 1 #TEMP
				unequip_queue.append(equipment)
				slot = equipment.equip_slot()	
				next_blocking_equipment = self.equipment_set.blocking_equipment(slot)
				if next_blocking_equipment:
					for next_item in next_blocking_equipment:
						blocking_equipment.append(next_item)
		# go through the blocking equipment and queue unequipping it all.
		wielded_items = []
		for u in reversed(unequip_queue):
			slot = u.equip_slot()
			if u.wielded:
				wielded_items.append(u)
				unwield_delay = 1 #TEMP
				self.enqueue_player_action(self.unwield_current_item, None, unwield_delay)
			else:
				unequip_delay = 1 #TEMP
				self.enqueue_player_action(self.unequip_item_in_slot, slot, unequip_delay)
		#queue performing the chosen equip action on the target equipment.
		if unequip:
			target_unequip_delay = 1 #TEMP
			self.enqueue_player_action(self.unequip_item_in_slot, target_equipment.equip_slot(), target_unequip_delay)
			if replace_item:
				replace_delay = 1 #TEMP
				self.enqueue_player_action(self.equip_item, replace_item, replace_delay)
		else:
			target_equip_delay = 1 #TEMP
			self.enqueue_player_action(self.confirm_equip_item, target_equipment, target_equip_delay)
		# queue reequipping the blocking equipment.
		# the first element of unequip queue is the original item we wanted to unequip, so we make no plans to reequip it.
		for u in unequip_queue:
			slot = u.equip_slot()
			if u in wielded_items:
				rewield_delay = 1 #TEMP
				self.enqueue_player_action(self.confirm_wield_item, u, rewield_delay)
			else:
				reequip_delay = 1 #TEMP
				self.enqueue_player_action(self.confirm_equip_item, u, reequip_delay)
		unequip_delay = 1 #TEMP
		self.execute_first_queued_action()

	def unequip_item_prompt(self, equipped_item, prompt_item):
		""" p.unequip_item_prompt( Item, Item ) -> None

		The player is prompted to unequip one item in favor of another.
		"""
		self.send_event("Do you want to unequip " + equipped_item.display_name()
			+ " and equip " + prompt_item.display_name() + "? (y/n/q)")
		self.screen_manager.switch_to_ynq_controls(self.confirm_replace_equip, self.cancel_action_message, self.cancel_action_message, prompt_item, self)

		#this and confirm_unequip might belong in the Being class.
	def confirm_replace_equip(self, item):
		""" p.confirm_replace_equip( Item ) -> None

		The player unequips one item and plans to equip another.
		"""
		slot = item.equip_slot()
		blocking_equipment = self.equipment_set.blocking_equipment(slot)
		if not blocking_equipment:
			unequip_delay = 1 	#TODO: change these to be based on the equipment itself
			equip_delay = 1
			self.enqueue_player_action(self.confirm_equip_item, item, equip_delay)
			self.execute_player_action(self.unequip_item_in_slot, slot, unequip_delay)
			return
		self.change_equip_blocked_item(self.equipment_set.get_item_in_slot(slot), slot, blocking_equipment, True, item) #untested

	def unequip_item(self, item):
		""" p.unequip( Item ) -> None

		The player unequips the given item.
		"""
		unequip_delay = 1 #TODO: set properly
		slot = item.equip_slot()
		self.execute_player_action(self.unequip_item_in_slot, slot, unequip_delay)

	def cancel_replace_equip(self, item):
		""" p.cancel_replace_equip( Item ) -> None

		The player decides not to replace his current equipment.
		"""
		self.send_event("Nevermind.")

	def begin_player_quaff_item(self):
		""" p.begin_player_quaff_item( ) -> None

		The player starts trying to quaff something.
		"""
		if(not self.inventory.contains_item_class(Potion)):
			self.send_event("Nothing to quaff.")
			return
		self.quaff_item_prompt()

	def quaff_item_prompt(self):
		""" p.quaff_item_prompt( ) -> None

		The player is prompted on which item to quaff.
		"""
		self.send_event("Quaff what?")
		item_list = self.inventory.class_item_select_list(Potion)
		self.screen_manager.switch_to_select_list_controls(item_list, self, self.temp_player_quaff_item, False, False)

	def temp_player_quaff_item(self, item):
		# no docstring because temp
		#TODO: potion actually affects the player
		#TODO: potion disappears
		quaff_delay = item.consume_time
		self.execute_player_action(self.confirm_quaff_item, item, quaff_delay)
