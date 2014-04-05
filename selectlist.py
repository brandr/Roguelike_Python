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

	def list_message(self):
		message = ""
		length = len(self.object_list)
		for i in range(length - 1):
			o = self.object_list[i]
			message += self.index_letter_string(i) + o.display_name() + ", "
		last_object = self.object_list[length - 1]
		message += self.index_letter_string(length - 1) + last_object.display_name() + ", (?)"
		return message

	def select_object_at_index(self, index):
		return self.object_list[index]

	def select_object_from_letter(self, letter):
		index = ALPHABET.index(letter)
		return self. select_object_at_index(index)

	def length(self):
		return len(self.object_list)

	def index_letter_string(self, index):
		return "(" + ALPHABET[index] + ")"

	def index_letter(self, index):
		return ALPHABET[index]

ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"