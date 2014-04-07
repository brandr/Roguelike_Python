"""This is the screen used to play the game."""

from screenmanager import *

BACKGROUND_COLOR = Color("#FFFFFF")
WIN_WIDTH = 800
WIN_HEIGHT = 640
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
DEPTH = 32
FLAGS = 0

class GameManager:
    """GameManager () -> GameManager

    This is the screen used to play the game.
    (Will add more description as more stuff is implemented.)

    Attributes: None
    """
    def __init__(self):
        pass

    def runGame(self, master_screen):
        """GM.runGame (...) -> None

        Run the game using a pygame screen.

        (add more description later)
        """
        pygame.display.set_caption("DIS A ROGUELIKE")
        timer = pygame.time.Clock()

        #TEMP for testing vvv
        # comment and uncomment to change what is on the level.

        sword_1 = MeleeWeapon("Master Sword")
        shield_1 = Armor("Hylian Shield", LEFT_HAND_SLOT)
        hat_1 = Armor("Fairy Hat", CHEST_SLOT)
        gloves_1 = Armor("Leather Gloves", GLOVES_SLOT)

        monster_sword = MeleeWeapon("Deku stick")

        player_1 = Player("Link") 
        player_1.obtain_item(sword_1)
        player_1.obtain_item(shield_1)
        player_1.obtain_item(hat_1)
        player_1.obtain_item(gloves_1)

        monster_1 = Monster("Moblin")
        monster_1.obtain_item(monster_sword)

        monster_2 = Monster("Bokoblin")

        test_level = Level(25, 25, 1) 
        test_level.add_wall(15, 15)
        test_level.add_wall(16, 15)

        test_level.add_player(player_1, 4, 4)
        #test_level.add_monster(monster_1, 8, 8)
        #test_level.add_monster(monster_2, 18, 16)

        map_pane = MapPane(player_1)                # TODO: turn these 4 lines into their own method somewhere in the screen/manager mess.
        character_pane = CharacterPane(player_1)
        event_pane = EventPane(player_1)
        main_screen_panes = [character_pane, map_pane, event_pane] 

        #inventory_item_pane = InventoryItemPane() #not putting args in yet, because this could apply to the player, tiles, or other stuff

        test_level.plan_monster_turns()
        game_controls = MainGameControls(player_1) #TODO: consider how controls may parse buttons differently for different screens.
        control_manager = ControlManager(game_controls)
        main_screen = GuiScreen(control_manager, main_screen_panes)
        screen_manager = ScreenManager(master_screen, main_screen, player_1)

        player_1.start_game() 

        #TEMP for testing ^^^

        while 1:
            timer.tick(100)

            for e in pygame.event.get():
                screen_manager.process_event(e)
            screen_manager.update_current_screen()
            self.draw_panes(screen_manager)
            pygame.display.update()

    def draw_panes(self, screen_manager):
        screen_manager.draw_panes()