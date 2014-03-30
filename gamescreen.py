"""This is the screen used to play the game."""

from mappane import *
from controls import *

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

        #temp for testing

        test_level = Level(25, 25, 1) 
        map_pane = MapPane(test_level)
        player_1 = Player() #TODO: args
        test_level.add_player(player_1, 4, 4)

        game_controls = Controls(player_1)
        #temp for testing

        #start_level = dungeon.start_level() havent made dungeon or levels yet.

        #start_level.addPlayer(player)

        while 1:
            timer.tick(100)

            for e in pygame.event.get():
                game_controls.process_event(e)
                #if e.type == QUIT: raise(SystemExit)
                #if e.type == KEYDOWN and e.key == K_ESCAPE:
                #    raise (SystemExit)

            #TODO: put key presses and associated values here, unless this is handled by another class.

        # draw background
            #for y in range(32):
            #    for x in range(32):
            map_pane.level_update(player_1)
            screen.blit(map_pane.draw_pane_image(), (map_pane.x_off, map_pane.y_off))
            pygame.display.update()
                    #screen.blit(bg, (x * 32, y * 32))
           #TODO: perform proper updates based on keyboard input here.
           #player.current_level.update(screen, up, down, left, right, running)