""" A pane showing the player's attributes.
"""

from pane import *

CHARACTER_PANE_X = 40
CHARACTER_PANE_Y = 8

CHARACTER_PANE_WIDTH = 450
CHARACTER_PANE_HEIGHT = 64

class CharacterPane(Pane):
	""" CharacterPane ( ... ) -> CharacterPane

	TODO: describe a CharacterPane and what it does

	Attributes:

	TODO

	"""

	def __init__(self, player):
		Pane.__init__(self, CHARACTER_PANE_X, CHARACTER_PANE_Y, CHARACTER_PANE_WIDTH, CHARACTER_PANE_HEIGHT)
		self.player = player
		
	def player_update(self):
		player_info = Surface((CHARACTER_PANE_WIDTH, CHARACTER_PANE_HEIGHT))
		
		font = pygame.font.Font(None, 14) 

		player_name_text = "Player: " + self.player.name
		player_hp_text = "HP: " 
		player_mp_text = "MP: "

		column_1 = [player_name_text, player_hp_text, player_mp_text]

		columns = [column_1]

		for j in range len(columns):
			c = columns[j]
			for i in range(len(c)):
				rendered_text = font.render(c[i], 0, WHITE)
				player_info.blit(rendered_text, (8 + 24*j, 8 + 16*i))
		self.update(player_info)