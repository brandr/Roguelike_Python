""" A list from which one or more objects may be selected.
These objects may be items, monsters, spells, etc.
"""

class SelectList:
	""" SelectList( Class, List ) -> SelectList

	TODO
	"""
	def __init__(self, list_class, object_list):
		self.list_class = list_class
		self.object_list = object_list
		self.toggles = []
		self.initialize_toggles()

	def initialize_toggles(self):
		for i in range(len(self.object_list)):
			self.toggles.append(False)

	def list_message(self):
		message = ""
		length = len(self.object_list)
		for i in range(length - 1):
			o = self.object_list[i]
			message += self.index_letter_string(i) + o.display_name(True) + ", "
		last_object = self.object_list[length - 1]
		message += self.index_letter_string(length - 1) + last_object.display_name(True) + ", (?)"
		return message

	def toggled_objects(self):
		objects = []
		for i in range(len(self.object_list)):
			if(self.toggles[i]):
				objects.append(self.select_object_at_index(i))
		return objects

	def toggle(self, letter):
		index = ALPHABET.index(letter)
		current = self.toggles[index]
		self.toggles[index] = not current

	def none_toggled(self):
		for t in self.toggles:
			if t == True: return False
		return True

	def select_object_at_index(self, index):
		return self.object_list[index]

	def select_object_from_letter(self, letter):
		index = ALPHABET.index(letter)
		return self. select_object_at_index(index)

	def length(self):
		return len(self.object_list)

	def index_letter_string(self, index):
		return "(" + ALPHABET[index] + ")"

	def index_toggle_string(self, index):
		toggled = self.toggles[index]
		if(toggled):
			return "+"
		return u"·"

	def index_letter(self, index):
		return ALPHABET[index]

ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"