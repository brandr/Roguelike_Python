# coding=utf-8
""" A list from which one or more objects may be selected.
These objects may be items, monsters, spells, etc.
"""

from item import Item

class SelectList:
	""" SelectList( Class, List ) -> SelectList

	A list containing items (or other objects) belonging to some class,
	which can have some action performed upon on one or more of them.

	Attributes:

	list_class: the Class that the objects in the list all belong to.

	object_list: the objects in the SelectList.

	toggles: a list of booleans tracking which objects are currently selected.
	"""
	def __init__(self, list_class, object_list):
		self.list_class = list_class
		self.object_list = object_list
		self.toggles = []
		self.quantities = []
		self.initialize_toggles()

	def initialize_toggles(self):
		""" sl.initialize_toggles( ) -> None 

		Set all current toggled to False, signifying that nothing is selected.
		"""
		for i in range(len(self.object_list)):
			self.toggles.append(False)
			self.quantities.append(1)

	def list_message(self):
		""" sl.list_message( ) -> str 

		Gives a comma-separated list of objects in this SelectList.
		"""
		message = ""
		length = len(self.object_list)
		for i in range(length - 1):
			o = self.object_list[i]
			message += self.index_letter_string(i) + o.display_name(True) + ", "
		last_object = self.object_list[length - 1]
		message += self.index_letter_string(length - 1) + last_object.display_name(True) + ", (?)"
		return message

	def toggled_objects(self):
		""" sl.toggled_objects( ) -> [ Object ]

		Gives a list of all currently selected objects.
		"""
		objects = []
		for i in range(len(self.object_list)):
			if(self.toggles[i]):
				next_object = (self.object_list[i], self.quantities[i])
				objects.append(next_object)
		return objects

	def toggle(self, letter, quantity = None):
		""" sl.toggle( char, int ) -> None

		Select the object corresponding to the given letter.
		"""
		#print quantity
		index = ALPHABET.index(letter)
		current = self.toggles[index]
		self.toggles[index] = not current
		self.quantities[index] = quantity

	def none_toggled(self):
		""" sl.none_toggled( ) -> bool

		Returns True if nothing is selected.
		"""
		for t in self.toggles:
			if t == True: return False
		return True

	def select_object_at_index(self, index):
		""" sl.select_object_at_index( int ) -> Object

		Returns the object corresponding to the given index.
		"""
		return self.object_list[index]

	def select_object_from_letter(self, letter):
		""" sl.select_object_from_letter( char ) -> Object

		Returns the object corresponding to the given letter.
		"""
		index = ALPHABET.index(letter)
		return self.select_object_at_index(index)

	def length(self):
		""" sl.length( ) -> int

		Returns the number of selectable objects.
		"""
		return len(self.object_list)

	def index_letter_string(self, index):
		""" sl.index_letter_string( int ) -> str

		Give the string that should represent the index of an object.
		"""
		return "(" + ALPHABET[index] + ")"

	def index_toggle_string(self, index):
		""" sl.index_toggle_string( int ) -> str

		A string on the selectlist screen indicating whether an object is selected or not.
		"""
		toggled = self.toggles[index]
		if(toggled):
			if self.quantities[index]: return "#"
			else: return "+"
		return u"·"

	def index_letter(self, index):
		""" sl.index_letter( int ) -> str

		Gives the letter corresponding to the given index.
		"""
		return ALPHABET[index]

ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"