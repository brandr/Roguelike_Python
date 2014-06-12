""" This launches the game. Eventually, this should show the title screen and possibly
options to start the game, open the map editor, etc.
"""

from gamemanager import *

def runGame():
    """
    runGame () -> None

    Run the game. (Will add more description once it's actually implemented and does stuff.)
    """
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH)
    manager = GameManager()
    manager.runGame(screen)

if __name__ == "__main__":
    runGame()