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
		
	def player_update(self): 	#TODO: as this gets more complex, consider creating GUI methods in the Pane class to make text components easier to place.
		player_info = Surface((CHARACTER_PANE_WIDTH, CHARACTER_PANE_HEIGHT))
		
		#font = pygame.font.Font(None, 14) 

		player_name_text = "Player: " + self.player.name
		player_hp_label_text = "HP: " 
		player_mp_label_text = "MP: "

		column_1 = [player_name_text, player_hp_label_text, player_mp_label_text]

		turn_count_text = "Turn count: " + str(self.player.current_level.turn_count())

		column_2 = [turn_count_text]

		columns = [column_1, column_2]

		for j in range(len(columns)):
			c = columns[j]
			for i in range(len(c)):
				rendered_text = self.font.render(c[i], 0, WHITE)
				player_info.blit(rendered_text, (8 + 72*j, 8 + 16*i))

		player_hp_text = self.player.hp_display()
		player_mp_text = self.player.mp_display()

		rendered_hp_text = self.font.render(player_hp_text, 0, RED)
		rendered_mp_text = self.font.render(player_mp_text, 0, BLUE)

		player_info.blit(rendered_hp_text, (28, 8 + 16))
		player_info.blit(rendered_mp_text, (28, 8 + 32))

		self.update(player_info)