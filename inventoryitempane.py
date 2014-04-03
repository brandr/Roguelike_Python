""" A pane listing the items found in an Inventory.
"""

from pane import *

INVENTORY_ITEM_PANE_X = 8
INVENTORY_ITEM_PANE_Y = 8

INVENTORY_ITEM_PANE_WIDTH = 450
INVENTORY_ITEM_PANE_HEIGHT = 360

class InventoryItemPane(Pane):
	""" InventoryItemPane( ... ) -> InventoryItemPane

	#TODO
	"""

	def __init__(self, inventory):
		Pane.__init__(self, INVENTORY_ITEM_PANE_X, INVENTORY_ITEM_PANE_Y, INVENTORY_ITEM_PANE_WIDTH, INVENTORY_ITEM_PANE_HEIGHT)
		self.inventory = inventory