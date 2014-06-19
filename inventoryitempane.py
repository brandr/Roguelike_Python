""" A pane listing the items found in an Inventory.
"""

from pane import *

INVENTORY_ITEM_PANE_X = 8
INVENTORY_ITEM_PANE_Y = 8

INVENTORY_ITEM_PANE_WIDTH = 450
INVENTORY_ITEM_PANE_HEIGHT = 450

ITEM_LINE_HEIGHT = 16

class InventoryItemPane(Pane):
	""" InventoryItemPane( Inventory ) -> InventoryItemPane

	A pane used to view and interact with an inventory.

	Attribtues:

	inventory: The inventory being viewed through this pane.
	"""

	def __init__(self, inventory):
		Pane.__init__(self, INVENTORY_ITEM_PANE_X, INVENTORY_ITEM_PANE_Y, INVENTORY_ITEM_PANE_WIDTH, INVENTORY_ITEM_PANE_HEIGHT)
		self.inventory = inventory

	def update(self):
		""" iip.update( ) -> None

		Updates the pane based on the inventory's contents.
		"""
		item_info = Surface((INVENTORY_ITEM_PANE_WIDTH, INVENTORY_ITEM_PANE_HEIGHT))
		for i in range(self.inventory.item_count()):
			item = self.inventory.item_at_index(i)
			item_name = item.display_name(True)
			item_text = self.rendered_text(item_name)
			item_info.blit(item_text, (8, ITEM_LINE_HEIGHT*i)) #TODO: multiple item columns
		#TODO
		Pane.update(self, item_info)