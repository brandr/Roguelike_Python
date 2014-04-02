"""This is the screen used to play the game."""

from mappane import *
from characterpane import *
from eventpane import *
from controlmanager import *

BACKGROUND_COLOR = Color("#FFFFFF")
WIN_WIDTH = 800
WIN_HEIGHT = 640
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
DEPTH = 32
FLAGS = 0

class GameScreen:
    """GameScreen () -> GameScreen

    This is the screen used to play the game.
    (Will add more description as more stuff is implemented.)

    Attributes: None
    """
    def __init__(self):
        pass

    def runGame(self, screen):
        """GS.runGame (...) -> None

        Run the game using a pygame screen.

        (add more description later)
        """
        pygame.display.set_caption("DIS A ROGUELIKE")
        timer = pygame.time.Clock()

        #TEMP for testing
        player_1 = Player("Link") 
        monster_1 = Monster("Moblin")
        sword_1 = MeleeWeapon("Master Sword")

        test_level = Level(25, 25, 1) 
        test_level.add_wall(15, 15)
        test_level.add_wall(16, 15)

        map_pane = MapPane(test_level)
        character_pane = CharacterPane(player_1)
        event_pane = EventPane(player_1)
        main_screen_panes = [character_pane, map_pane, event_pane]

        test_level.add_player(player_1, 4, 4)
        test_level.add_monster(monster_1, 8, 8)
        test_level.add_item(sword_1, 8, 10)

        player_1.start_game()   

        test_level.plan_monster_turns()
        game_controls = MainGameControls(player_1) #TODO: consider how controls may parse buttons differently for different screens.
        control_manager = ControlManager(game_controls)
        
        #TEMP for testing

        while 1:
            timer.tick(100)

            for e in pygame.event.get():
                control_manager.process_event(e)

            map_pane.level_update(player_1)
            character_pane.player_update()
            #event_pane.update()

            self.draw_panes(screen, main_screen_panes)
            
            pygame.display.update()

    def draw_panes(self, screen, panes):
        for p in panes:
            screen.blit(p.draw_pane_image(), (p.x_off, p.y_off))
    

                    #screen.blit(bg, (x * 32, y * 32))
           #TODO: perform proper updates based on keyboard input here.
           #player.current_level.update(screen, up, down, left, right, running)