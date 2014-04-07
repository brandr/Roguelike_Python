""" A pane showing a list of selectable objects.
"""

from pane import *

SELECT_LIST_PANE_X = 40
SELECT_LIST_PANE_Y = 8

SELECT_LIST_PANE_WIDTH = 450
SELECT_LIST_PANE_HEIGHT = 450

SELECT_LIST_LINE_HEIGHT = 16

class SelectListPane(Pane):
	""" SelectListPane( SelectList ) -> SelectListPane
	TODO
	Attributes:
	select_list: the list of selectable objects.
	"""
	def __init__(self, select_list):
		Pane.__init__(self, SELECT_LIST_PANE_X, SELECT_LIST_PANE_Y, SELECT_LIST_PANE_WIDTH, SELECT_LIST_PANE_HEIGHT)
		self.select_list = select_list

	def update(self):
		select_info = Surface((SELECT_LIST_PANE_WIDTH, SELECT_LIST_PANE_HEIGHT))
		for i in range(self.select_list.length()):
			o = self.select_list.select_object_at_index(i)
			name = o.display_name(True)
			object_text = self.select_list.index_letter_string(i) + " " + name
			rendered_text = self.rendered_text(object_text)
			select_info.blit(rendered_text, (8, SELECT_LIST_LINE_HEIGHT*i)) #TODO: multiple columns
		Pane.update(self, select_info)