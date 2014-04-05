""" A being is a more general version of a player or monster.
"""

from tile import *

DEFAULT_COLOR = Color("#FFFFFF")

class Being:
	""" Being( ... ) -> Being

	Only one being can occupy a tile at a time.

	TODO: docstring
	"""
	def __init__(self, name):
		self.name = name
		self.current_level = None
		self.current_tile = None
		self.melee_range = 1 #TEMP
		self.inventory = Inventory()

	def display_name(self):
		return self.name

	def send_event(self, message):
		self.current_level.send_event(message)

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

	def melee_attack(self, being):
		if(self.in_range(being, self.melee_range)):
			self.send_event(self.name + " attacked " + being.name + "!") #TEMPORARY. TODO: actually implement combat
		#TODO: case for missing because the target moved out of the way.

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
		self.current_level.enqueue_delay(self, action, arg, delay)		

	def end_turn(self):
		self.current_level.process_turns()

	def wait(self, arg):
		pass

	@staticmethod
	def direction_from_diff(diff):
		if(diff == 0): return 0
		return (int)(diff/abs(diff))