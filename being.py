""" A being is a more general version of a player or monster.
"""

from xdx import *
from tile import *
from actionqueue import *
from identifylist import *

DEFAULT_COLOR = Color("#FFFFFF")

class Being:
	""" Being( str ) -> Being

	Only one being can occupy a tile at a time.

	Attributes:
	
	name: a string representing the Being's name. 
		For most beings, this can probably be used to refer to them in any situation,
		though the player is generally referred to as "you".
	action_queue: An ordered queue of actions that this Being is "planning" to perform.
	identify_list: A list of items known to this player or monster.	
	status_list: A list of statuses affecting this Being, whose effects remain active 
		until they are removed from this list.
	current_level: the vertical floor of the dungeon this Being currently occupies.
	current_tile: The tile this Being currently occupies.
	melee_range: The distance this Being can reach with a melee weapon. 
		In the future, this should probably be a method, not a variable. Not sure, though.
	inventory: the set of items this Being has on its person.
	equipment_set: the set of armor/weapons/magic bling this Being has on.
	hit_points: [current hit points, maximum hit points] - current points cannot go above maximum
		and the Being dies when current hit points reach zero.
	magic_points: [current magic points, maximum magic points] - current points cannot go above maximum
		and magic consumes current points.
	weapon_skill_aggregate: Affects weapon hit rolls 
	dodge_value: A higher value increases dodge chance.
	block_value: A higher value increases block chance.
	attack_speed: delay from attacking should be a getter based on: 
		f(type of being, weapon, relevant weapon skill, relevant weapon stat)^1
	attack_buffer: The leftover decimal number of "swings" after the last attack.
	resistances: Dictionary mapping resistances to resistance levels. Gonna be pretty useful later, esp because vulnerability can just be minus.
	"""
	def __init__(self, name):
		self.action_queue = ActionQueue()
		self.identify_list = IdentifyList()
		self.status_list = []
		self.name = name
		self.current_level = None
		self.current_tile = None
		self.inventory = Inventory()
		self.equipment_set = EquipmentSet(HUMANOID)
		self.hit_points = [0, 0]	
		self.magic_points = [0, 0]
		self.dodge_value = 0 #TEMP
		self.block_value = 10 #TEMP dodge and block values for combat
		self.attack_buffer = 0.0
		self.attacked_last_turn = True #Fixed attack buffer issue.
		self.resistances = {"fire":0, "ice":0,"acid":0,"lightning":0,"slashing":0,"piercing":0,"bludgeoning":0,"acid":0} 

	def display_name(self, arg = None): 
		""" b.display_name(None) -> str

		This is the name for this Being that should appear in the event pane.
		not sure what arg should be for being. currently it only means something for items.
		"""
		return self.name

	def send_event(self, message): # IDEA: make an "Event" class whose contents are parsed and sent to the player (if he can see/hear the event).
		""" b.send_event(str) -> None

		Make a message appear on a new line in the event pane.
		"""
		self.current_level.send_event(message)

	def set_start_equipment(self, equipment_set):
		""" b.set_start_equipment(equipment_set) -> None

		Give the Being a set of equipment without forcing it to spend turns equipping.
		This should only be used when the Being is first created because it would be
		super OP in most other situations.
		"""
		self.equipment_set = equipment_set
		equipment = equipment_set.all_items()
		self.inventory.add_item_list(equipment)

	def restore_hp(self, amount):
		self.hit_points[0] = min(self.hit_points[0] + amount, self.hit_points[1])

	def take_damage(self, damage): #Should damage be passed as a list? See footnote 3. Similar 
		""" b.take_damage( int ) -> None

		Apply damage to this Being, reducing its current HP.
		"""
		current_hp = self.hit_points[0]
		self.hit_points[0] = max(0, current_hp - damage)
		"""
		if damage is passed as a list instead:
			for i in damageList[1::]:
                if resistances[i] < 0:
                    damageList[0]*=abs(resistances[i])
                else if resistances[i] < 0:
                    damageList[0]/= resistances[i]


		then do the rest of the stuff and pretend not to notice the absurd potential of polytyped attacks
		"""
		#Armor needs to go here, somehow.
		#should death_check be called here? need flowchart

	def add_status(self, status):
		""" b.add_status( Status ) -> None

		Add the status to this Being, thereby adding it to the current list of Statuses.
		Note that the status's actual action is handled by the current level's
		turn counter, not by the Being itself.
		"""
		status.target = self
		self.current_level.enqueue_delay(status, status.delay)
		self.status_list.append(status)

	def remove_status(self, status):
		""" b.remove_status( Status ) -> None

		Remove this status so that it no longer affects this Being.
		"""
		self.status_list.remove(status)
		self.current_level.remove_actor(status)
		#TODO: figure out how status should send messages in the player's case

	def take_status_effect(self, status):
		""" b.take_status( Status ) -> None

		Apply the status to this Being, make its effect occur.
		"""
		if status in self.status_list:
			status.take_effect()
			self.current_level.enqueue_delay(status, status.delay)	#TODO: consider rolling a value for status delay based on some base delay.

	def obtain_item(self, item):
		""" b.obtain_item( Item ) -> None

		The Being obtains the item, adding it to its inventory.
		"""
		self.inventory.add_item(item) #TODO: checks for stuff like full inventory? (might take place before here)

	def move_towards(self, target):
		""" b.move_towards( Being/Tile ) -> None

		Move towards the target's location unless there is an obstacle in the way.
		"""
		direction = self.direction_towards(target) #TODO: pathing
		dest_coords = self.coords_in_direction(direction)
		if(self.enemy_in_tile(dest_coords[0], dest_coords[1])):
			self.melee_attack(self.current_level.being_in_tile(dest_coords[0], dest_coords[1]))
		elif(self.current_level.open_tile(dest_coords[0], dest_coords[1])):
			self.move_to(dest_coords)
		#TODO: case for destination blocked

	def move_to(self, dest_coords):
		""" b.move_to( (int, int) ) -> None

		Move to a new location on the level specified by the given coordinates, assuming there is room.
		"""
		if(self.current_level.open_tile(dest_coords[0], dest_coords[1])):
			self.current_tile.remove_being()
			self.current_level.temp_place_being(self, dest_coords[0], dest_coords[1]) #TEMP method	

	def death_check(self):
		""" b.death_check( ) -> bool

		Checks if the Being is dead or not.
		"""
		if(self.hit_points[0] <= 0):
			self.die()
			return True
		return False

	def die(self):	#TEMP
		""" b.die( ) -> None

		Do whatever happens when this thing dies. Should be different for monsters and the player.
		"""
		self.send_event(self.display_name() + " died!")
		#TODO: other death stuff

	def melee_attack(self, target):
		""" b.melee_attack( Being ) -> None

		Strike a target that is in melee range.
		TODO: go into more detail if necessary.
		"""
		if(self.in_range(target, self.melee_range())): #Attack speed basically works.
			attack_speed = self.attack_speed()
			if not (self.attacked_last_turn):
				self.attack_buffer = 0			
			if self.attack_buffer == 0:
				attackCount = int(attack_speed)
				self.attack_buffer = attack_speed - (int(attack_speed))
			elif self.attack_buffer > 0: #Will be susceptible to weird floating-point shit, but might not be a problem.
				attackCount = int(attack_speed + attack_buffer)
				self.attack_buffer = (attack_speed + self.attack_buffer) - int(attack_speed + attack_buffer)
			else:
				print("Attack buffer shouldn't be negative and you have seriously blown it.")
			while attackCount > 0:
				if(self.melee_hit_roll(target)): 
					damage = self.melee_damage_roll(target) #Damage typing should be implemented here^3
					if(damage <= 0):
						self.send_event(target.display_name() + " shrugged off the attack.")
						break
					self.send_event(self.display_name() + " hit " + target.name + " for " + str(damage) + " damage!") #TEMPORARY. TODO: actually implement combat
					target.take_damage(damage) #NOTE: should modifiers apply before here, or not? (probably should)
					if(target.death_check()):
						break
				attackCount -= 1
			self.attacked_last_turn = True 
			return
				
		#TODO: case for missing because the target moved out of the way.

	def melee_hit_roll(self, target):
		""" b.melee_hit_roll( Being ) -> bool

		Check to see if this Being hits the target.
		"""
		weaponRoll = xdx(1, 20) + self.weapon_skill_aggregate()
		shield_value = target.shield_roll()
		if(weaponRoll >= target.dodge_value):
			if(weaponRoll >= shield_value):
				return True
			elif(weaponRoll < shield_value):
				self.send_event(self.display_name() + " was blocked by " + target.name)
				return False
		elif(weaponRoll < target.dodge_value):
				self.send_event(self.display_name() + " was evaded by a nimble " + target.name)
				return False
		return True #TODO: calculate chance to miss a melee attack here.

	def melee_damage_roll(self, target):
		""" b.melee_damage_roll( Being ) -> int

		See how much damage this Being does with a melee attack.
		"""
		base_attack = 5 #TODO: get this properly once we figure out combat mechanics
		min_attack = int(0.8 * base_attack)
		max_attack = int(1.2 * base_attack)
		return random_in_range(min_attack, max_attack) #NOTE: this method is subject to a lot of change depending on all the factors that affect melee combat.

	def melee_range(self):
		""" b.melee_range( ) -> int

		How many squares away this Being can strike with a melee attack.
		"""
		weapon = self.wielded_item()
		if weapon:
			return weapon.weapon_range #TODO: make sure this works for item. Might want getter w/ override
		return 1

	def weapon_skill_aggregate(self):
		""" b.weapon_skill_aggregate( ) -> int ?

		? (not sure what this will be in final verison)
		"""
		weapon = self.wielded_item()
		if weapon:
			return weapon.weapon_damage
		return 0

	def attack_speed(self):
		""" b.attack_speed( ) -> double

		A measure of how fast an attack from this being is, given the currently wielded weapon.
		"""
		weapon = self.wielded_item()
		if weapon:
			return weapon.weapon_speed
		return 5 #TEMP

	def melee_attack_delay(self):
		""" b.melee_attack_delay( ) -> int

		The number of units of time it takes for this Being to execute one melee attack action.
		"""
		attack_speed = self.attack_speed() #TODO: consider making this specifically grab melee attack speed.
		return 1 + 10/attack_speed #TEMP formula

	def shield_roll(self):
		""" b.shield_roll( ) -> int (or float?)

		Roll to generate a value for an attempt to block an attack with a shield.
		"""
		return 0 #TEMP

	def decrement_item(self, item):
		""" b.decrement_item( Item ) -> None

		Decrease the quantity of the given item in this Being's inventory by 1.
		NOTE: this may be a problem if the Being has multiple stacks of identical items. Not sure.
		"""
		self.inventory.decrement_item(item)

	def drop_all_items(self, display = False, instant = True): #display tells whether the drop actions should be displayed in the event pane.
		""" b.drop_all_items( bool, bool ) -> None

		Drop all items this Being has on the ground.
		If display is True, the item dropping is displayed on the event pane.
		If instant is True, the drop actions consume no time.
		"""
		#TODO: consider either removing the args if this is never used for any case besides a monster dying, or actually using them if it is.
		items = self.inventory.take_all_items()
		self.current_tile.add_item_list(items)

	def drop_item(self, (item, quantity)):
		""" b.drop_item( ( Item, int ) ) -> None

		The being drops the item on the ground like a filthy mongrel.
		"""
		dropped_quantity = min(item.current_quantity(), quantity)
		drop_item = item.create_copy(dropped_quantity)
		self.inventory.decrement_item(item, dropped_quantity)
		self.current_tile.add_item(drop_item)
		self.send_event(self.display_name() + " dropped " + drop_item.display_name() + ".")

	def remove_all_equipment(self): 
		""" b.remove_all_equipment( ) -> None

		Instantly unequip all equipment.
		Not used as an ingame action, only for special cases like a monster dying.
		"""
		self.equipment_set.remove_all_equipment()

	def confirm_wield_item(self, item):
		""" b.confirm_wield_item( Item ) -> None

		Once it is certain that this Being can wield an item, do so.
		"""
		if(self.equipment_set != None):
			self.equipment_set.wield_item(item)
			self.send_event(self.display_name() + " wielded " + item.display_name() + ".")

	def unwield_current_item(self, arg = None):
		""" b.unwield_current_item( None ) -> None

		Stop wielding whatever this Being is currently wielding.
		NOTE: this does not cover the possiblity of dual-wielding yet.
		"""
		if(self.wielding_item()):
			item_name = self.wielded_item().display_name()
			self.equipment_set.unwield_item_in_slot(RIGHT_HAND_SLOT)
			self.send_event(self.display_name() + " unwielded " + item_name + ".")

	def confirm_equip_item(self, item):
		""" b.confirm_equip_item( Item ) -> None

		Once it is certain that this Being can equip an item, do so.
		"""
		if(self.equipment_set != None):
			self.equipment_set.equip_item(item)
			self.send_event(self.display_name() + " equipped " + item.display_name() + ".")

	def unequip_item_in_slot(self, slot):
		""" b.confirm_unequip_item( str ) -> None

		Once it is certain that this Being can unequip an item, do so.
		"""
		if(self.has_equipment_in_slot(slot)):
			item_name = self.equipment_in_slot(slot).display_name()
			self.equipment_set.unequip_item_in_slot(slot)
			self.send_event(self.display_name() + " unequipped " + item_name + ".")

	def wielding_item(self):
		""" b.wielding_item( ) -> bool

		Checks whether the Being is currently wielding something.
		"""
		return self.equipment_set.item_is_in_slot(RIGHT_HAND_SLOT) #TODO: may need to change this for non-humanoids (and lefties, which are included in non-humanoids.)

	def wielded_item(self):
		""" b.wielded_item( ) -> Item

		Returns the item the Being is currently wielding.
		NOTE: not to be confused with wielding_item, which simply checks to see if an item is wielded.
		"""
		return self.equipment_set.get_item_in_slot(RIGHT_HAND_SLOT)

	def has_equipment_in_slot(self, slot):
		""" b.has_equipment_in_slot( str ) -> bool

		Checks whether the Being currently has something equipped in the given slot.
		"""
		return self.equipment_set.item_is_in_slot(slot)

	def equipment_in_slot(self, slot):
		""" b.equipment_in_slot( str ) -> Equipment

		Returns the equipment in the given slot.
		"""
		return self.equipment_set.get_item_in_slot(slot)

	def confirm_quaff_item(self, item):
		""" b.confirm_quaff_item( Item ) -> None

		Drink something in the player's inventory.
		Not sure whether we actually need the "dose" system.
		"""
		self.send_event(self.display_name() + " quaffed a " + item.display_name() + ".")
		item.take_effect(self)
		item.consume_dose()
		if(item.no_doses):
			self.decrement_item(item)
		#TODO

	def in_range(self, target, check_range):
		""" b.in_range(Being/Tile, int ) -> bool

		Check whether this being is in the given range of the given other being/tile.
		"""
		offset = self.offset_from(target)
		#distance = (int)(sqrt(pow(offset[0], 2) + pow(offset[1], 2)))	# we may want this-- it calculates a circle rather than a square, which is not accurate for roguelike geometry but looks nicer.
		distance = max(abs(offset[0]), abs(offset[1]))
		return check_range >= distance

	def enemy_in_tile(self, x, y):
		""" b.enemy_in_tile( int, int ) -> bool

		Check whether there is an enemy in the tile at the given coordinates.
		"""
		target_being = self.current_level.being_in_tile(x, y)
		return target_being != None and self.is_enemy(target_being)

	def is_enemy(self, being):
		""" b.is_enemy( Being ) -> bool

		Checks whether another Being is this Being's enemy. Currently, this is always the case.
		"""
		return True #TODO: figure out whether the being is actually an enemy

	def coordinates(self):
		""" b.coordinates( ) -> (int, int)

		Returns the current (x, y) coordinates of this being on the level.
		"""
		return self.current_tile.coordinates()

	def coords_in_direction(self, direction):
		""" b.coords_in_direction( (int, int) ) -> (int, int)

		Return the coordinates in a given direction, represented as:
		(-1, -1) = left/up, (-1, 0) = left, (-1, 1) = left/down
		(0, -1) = up, (0, 0) = current position, (0, 1) = down
		(1, -1) = right/up, (1, 0) = right, (1, 1) = right/down
		"""
		coords = self.coordinates()
		return (coords[0] + direction[0], coords[1] + direction[1])

	def direction_towards(self, target):
		""" b.direction_towards( Being/Tile ) -> (int, int)

		Returns the direction that the given target is in with respect to this Being.
		Uses the same directional notation as coords_in_direction.
		"""
		offset = self.offset_from(target)
		x_dir = Being.direction_from_diff(offset[0])
		y_dir = Being.direction_from_diff(offset[1])
		return (x_dir, y_dir)

	def clear_action_queue(self, arg = None):
		""" b.clear_action_queue( None ) -> None

		Removes all actions from this Being's action queue.
		"""
		self.action_queue.clear()

	def offset_from(self, target): #signed offset from target being
		""" b.offset_from( Being/Tile ) -> (int, int)

		Like direction_towards(), but includes distance instead of just direction.
		"""
		current_coords = self.coordinates()
		target_coords = target.coordinates()
		x_diff = int(target_coords[0] - current_coords[0])
		y_diff = int(target_coords[1] - current_coords[1])
		return (x_diff, y_diff)

	def current_symbol(self):
		""" b.current_symbol( ) -> char (or str?) /None

		This is the symbol that this Being uses to represent itself.
		Should be overridden by players and monsters.
		"""
		return None

	def color(self):
		""" b.color( ) -> Color

		Returns a pygame Color object to describe how this Being should be colored onscreen.
		"""
		return DEFAULT_COLOR

	def execute_action(self, action, arg, delay):
		""" b.execute_action( Method, ?, int ) -> None

		Takes a method as an arg and executes it with whatever argument is provided. The delay represents
		how long that action takes to complete, and prevents the Being from doing anything until the delay
		has passed.
		"""
		if action != self.melee_attack:
			self.attacked_last_turn = True
		action(arg)	
		self.current_level.enqueue_delay(self, delay)		

	def end_turn(self):
		""" b.end_turn( ) -> None

		Signals to the level's turn counter that this Being is done doing things for its turn.
		This allows other Beings to act.
		"""
		self.current_level.process_turns()

	def wait(self, arg = None):
		""" b.wait( None ) -> None

		This method does nothing, but is required to make wait actions works.
		"""
		pass

	@staticmethod
	def direction_from_diff(diff):
		""" direction_from_diff( int ) -> int

		Take a number and return its sign multiplied by 1.
		i.e., f(32) = 1, f(0) = 0, f(-32) = -1, f(1) = 1, etc.
		"""
		if(diff == 0): return 0
		return (int)(diff/abs(diff))

'''
1: Inheritance issue. The inheritance seems to go being --> player/monster --> player/monster inventory. Is it wrong to draw from lower down on the hierarchy to fill top spots in the hierarchy? Is this what the cool kids call spaghetti code? Will it make me trip over my cape?
3: Damage typing is a cold-hearted bastard because it makes you pass a list of mixed int and strings to determine what type(s) the damage is, and then makes all of the other functions that deal with taking damage or being swung at have to take that list as an argument and iterate over it to determine just the types and if the monster has corresp. resistances. So this dumb list has to be passed everywhere that the simple int would, and I'll try it out later.
4: Or if max(f(randomness, aggregate weapon value), g(calculated dodge value)) == f.
5: Having dodge-then-shield be calculated out rather some f(dodge, shield) is lower on obvious, meaningless math, but means that as far as game balance goes dodge and shield have to be pretty heavily mutually exclusive, or else even if both have diminishing marginal returns like we're good game designers and economists there'll be a sweet spot that's some ratio of both and getting in that spot will be obvious enough so that nobody will even have to whip out lagrange method or pretend to care.
'''
