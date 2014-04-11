""" A being is a more general version of a player or monster.
"""

from xdx import *
from tile import *
from actionqueue import *
from identifylist import *

DEFAULT_COLOR = Color("#FFFFFF")

class Being:
	""" Being( ... ) -> Being

	Only one being can occupy a tile at a time.

	TODO: docstring
	"""
	def __init__(self, name):
		self.action_queue = ActionQueue()
		self.identify_list = IdentifyList()
		self.status_list = []

		self.name = name
		self.current_level = None
		self.current_tile = None
		self.melee_range = 1 #TEMP
		self.inventory = Inventory()
		self.equipment_set = None
		self.hit_points = [0, 0]
		self.magic_points = [0, 0]

	def display_name(self, arg = None): #not sure what arg should be for being. currently it only means something for items.
		return self.name

	def send_event(self, message): # IDEA: make an "Event" class whose contents are parsed and sent to the player (if he can see/hear the event).
		self.current_level.send_event(message)

	def set_start_equipment(self, equipment_set):
		self.equipment_set = equipment_set
		equipment = equipment_set.all_items()
		self.inventory.add_item_list(equipment)

	def restore_hp(self, amount):
		self.hit_points[0] = min(self.hit_points[0] + amount, self.hit_points[1])

	def take_damage(self, damage):
		current_hp = self.hit_points[0]
		self.hit_points[0] = max(0, current_hp - damage)
		#should death_check be called here? need flowchart

	def add_status(self, status):
		status.target = self
		self.current_level.enqueue_delay(status, status.delay)
		self.status_list.append(status)

	def remove_status(self, status):
		self.status_list.remove(status)
		self.current_level.remove_actor(status)
		#TODO: figure out how status should send messages in the player's case

	def take_status_effect(self, status):
		if status in self.status_list:
			status.take_effect()
			self.current_level.enqueue_delay(status, status.delay)	#TODO: consider rolling a value for status delay based on some base delay.

	def obtain_item(self, item):
		self.inventory.add_item(item) #TODO: checks for stuff like full inventory? (might take place before here)

	def move_towards(self, target):
		direction = self.direction_towards(target) #TODO: pathing
		dest_coords = self.coords_in_direction(direction)
		if(self.enemy_in_tile(dest_coords[0], dest_coords[1])):
			self.melee_attack(self.current_level.being_in_tile(dest_coords[0], dest_coords[1]))
		elif(self.current_level.open_tile(dest_coords[0], dest_coords[1])):
			self.move_to(dest_coords)
		#TODO: case for destination blocked

	def move_to(self, dest_coords):
		if(self.current_level.open_tile(dest_coords[0], dest_coords[1])):
			self.current_tile.remove_being()
			self.current_level.temp_place_being(self, dest_coords[0], dest_coords[1]) #TEMP method	

	def death_check(self):
		if(self.hit_points[0] <= 0):
			self.die()
			return True
		return False

	def die(self):	#TEMP
		self.send_event(self.display_name() + " died!")
		#TODO: other death stuff

	def melee_attack(self, target):
		if(self.in_range(target, self.melee_range)):
			if(self.melee_hit_roll(target)):
				damage = self.melee_damage_roll(target)
				if(damage <= 0):
					self.send_event(target.display_name() + " shurgged off the attack.")
					return
				target.take_damage(damage) #NOTE: should modifiers apply before here, or not? (probably should)
				if(target.death_check()):
					return
				self.send_event(self.display_name() + " hit " + target.name + " for " + str(damage) + " damage!") #TEMPORARY. TODO: actually implement combat
		#TODO: case for missing because the target moved out of the way.

	def melee_hit_roll(self, target):
		return True #TODO: calculate chance to miss a melee attack here.

	def melee_damage_roll(self, target):
		base_attack = 5 #TODO: get this properly once we figure out combat mechanics
		min_attack = int(0.8 * base_attack)
		max_attack = int(1.2 * base_attack)
		return random_in_range(min_attack, max_attack) #NOTE: this method is subject to a lot of change depending on all the factors that affect melee combat.

	def decrement_item(self, item):
		self.inventory.decrement_item(item)

	def drop_all_items(self, display = False, instant = True): #display tells whether the drop actions should be displayed in the event pane.
		#TODO: consider either removing the args if this is never used for any case besides a monster dying, or actually using them if it is.
		items = self.inventory.take_all_items()
		self.current_tile.add_item_list(items)

	def drop_item(self, item):
		self.inventory.remove_item(item)
		self.current_tile.add_item(item)
		self.send_event(self.display_name() + " dropped " + item.display_name() + ".")

	def remove_all_equipment(self): #not used as an ingame action, only for special cases like a monster dying.
		self.equipment_set.remove_all_equipment()

	def confirm_wield_item(self, item):
		if(self.equipment_set != None):
			self.equipment_set.wield_item(item)
			self.send_event(self.display_name() + " wielded " + item.display_name() + ".")

	def unwield_current_item(self, arg = None):
		if(self.wielding_item()):
			item_name = self.wielded_item().display_name()
			self.equipment_set.unwield_item_in_slot(RIGHT_HAND_SLOT)
			self.send_event(self.display_name() + " unwielded " + item_name + ".")

	def confirm_equip_item(self, item):
		if(self.equipment_set != None):
			self.equipment_set.equip_item(item)
			self.send_event(self.display_name() + " equipped " + item.display_name() + ".")

	def unequip_item_in_slot(self, slot):
		if(self.has_equipment_in_slot(slot)):
			item_name = self.equipment_in_slot(slot).display_name()
			self.equipment_set.unequip_item_in_slot(slot)
			self.send_event(self.display_name() + " unequipped " + item_name + ".")

	def wielding_item(self):
		return self.equipment_set.item_is_in_slot(RIGHT_HAND_SLOT) #TODO: may need to change this for non-humanoids

	def wielded_item(self):
		return self.equipment_set.get_item_in_slot(RIGHT_HAND_SLOT)

	def has_equipment_in_slot(self, slot):
		return self.equipment_set.item_is_in_slot(slot)

	def equipment_in_slot(self, slot):
		return self.equipment_set.get_item_in_slot(slot)

	def confirm_quaff_item(self, item):
		self.send_event(self.display_name() + " quaffed a " + item.display_name() + ".")
		item.take_effect(self)
		item.consume_dose()
		if(item.no_doses):
			self.decrement_item(item)
		#TODO

	def in_range(self, being, check_range):
		offset = self.offset_from(being)
		distance = (int)(sqrt(pow(offset[0], 2) + pow(offset[1], 2)))
		return check_range >= distance

	def enemy_in_tile(self, x, y):
		target_being = self.current_level.being_in_tile(x, y)
		return target_being != None and self.is_enemy(target_being)

	def is_enemy(self, being):
		return True #TODO: figure out whether the being is actually an enemy

	def coordinates(self):
		return self.current_tile.coordinates()

	def coords_in_direction(self, direction):
		coords = self.coordinates()
		return (coords[0] + direction[0], coords[1] + direction[1])

	def direction_towards(self, target):
		offset = self.offset_from(target)
		x_dir = Being.direction_from_diff(offset[0])
		y_dir = Being.direction_from_diff(offset[1])
		return (x_dir, y_dir)

	def offset_from(self, target): #signed offset from target being
		current_coords = self.coordinates()
		target_coords = target.coordinates()
		x_diff = int(target_coords[0] - current_coords[0])
		y_diff = int(target_coords[1] - current_coords[1])
		return (x_diff, y_diff)

	def current_symbol(self):
		return None

	def color(self):
		return DEFAULT_COLOR

	#def begin_action(self, action, arg, delay):
	#	self.current_level.enqueue_action(self, action, arg, delay)

	def execute_action(self, action, arg, delay):
		action(arg)	
		self.current_level.enqueue_delay(self, delay)		

	def end_turn(self):
		self.current_level.process_turns()

	def wait(self, arg):
		pass

	@staticmethod
	def direction_from_diff(diff):
		if(diff == 0): return 0
		return (int)(diff/abs(diff))