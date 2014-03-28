""" This launches the game. Eventually, this should show the title screen and possibly
options to start the game, open the map editor, etc.
"""

from pygame import *
from gamescreen import *

# these are constants used by pygame. We may want to change where these are stored, or change their values.

def runGame():
    """
    runGame () -> None

    Run the game. (Will add more description once it's actually implemented and does stuff.)
    """
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH)
    mainScreen = GameScreen()
    #mainScreen.runGame(screen, dungeon) #may use a version more like this later on.
    mainScreen.runGame(screen)

if __name__ == "__main__":
    runGame()