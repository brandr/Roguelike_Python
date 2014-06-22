from controls import *
from pygame import Color
from effect import Effect

DEFAULT_TARGET_SYMBOL = '_'
CYAN = Color("#00FFFF")

class TargetControls(Controls):
    """
    TargetControls(Method, ?) -> TargetControls
    Allows the player to select individual squares at range. Depending
    on the reason the player is selecting squares (possible reasons are
    line-of-sight-attack (spell/ranged attack) or smite-targeted effect
    (looking at something/spells), the class will either draw a line
    between the two points or not, and will indicate in both cases
    whether or not the indicated square is out of range.

    Attributes:
        action (method): What to do to the selected square.
        action_range (integer): The range of the passed method.
        target_style: The type of targeting to use.
        player: The player who is doing the targeting.

    """
    def __init__(self, action, action_range, target_style, player, arg):
        Controls.__init__(self)
        self.initialize_control_map(TARGET_CONTROL_MAP)
        self.action = action
        self.action_range = action_range
        self.target_style = target_style
        self.player = player
        self.arg = arg
        self.target_tile = self.player.current_tile

        self.draw_effects()

    def fire_action(self, key = None):
        """ tc.fire_action(None) -> None

        Perform the associated firing action upon the current target.
        """
        self.player.send_event("Firing!")
        self.clear_effects()
        coords = self.target_tile.coordinates()
        self.exit_to_main_game_controls()
        self.action(self.arg, coords[0], coords[1])

    def move_input(self, key):
        """ tc.move_input( str ) -> None

        Convert an inputted movement key (arrow keys or numpad) into a direction,
        and then move the targeting reticule in that direction.
        """
        if(key in TARGET_DIRECTION_MAP):
            direction = TARGET_DIRECTION_MAP[key]
            self.move_target(direction)

    def move_target(self, direction):
        """ tc.move_target( ( int, int ) ) -> None

        Move the targeting reticule in the given direction,
        unless it cannot move in that direction either because it is outside the
        possible range or because it is not in the level.
        """
        coords = self.target_tile.coordinates()
        x, y = coords[0] + direction[0], coords[1] + direction[1]
        level = self.player.current_level
        if level.valid_tile(x, y):
            new_tile = level.tile_at(x, y)
            if self.player.in_range(new_tile, self.action_range):
                self.clear_effects()
                self.target_tile = new_tile
                self.draw_effects()

    def clear_effects(self):
        """ tc.clear_effects( ) -> None

        Tell the level to clear its visual effects.
        """
        self.player.current_level.clear_effects()

    def draw_effects(self):
        """ tc.draw_effects( ) -> None

        Draw the visual effects based on the targeting style for these TargetControls.
        """
        if self.target_style in TARGET_STYLE_EFFECT_MAP:
            effect_method = TARGET_STYLE_EFFECT_MAP[self.target_style]
            effect_method(self)
        self.draw_target_tile_effect()

    def draw_target_tile_effect(self):
        """ tc.draw_target_tile_effect( ) -> None

        Draw a cyan underscore (subject to change) on the currently targeted tile.
        """
        self.target_tile.set_effect(DEFAULT_TARGET_SYMBOL, CYAN)
        self.target_tile.update()

    def draw_smite_effect(self):
        """ tc.draw_smite_effect( ) -> None

        Does nothing for now, because smite targeting has no associated visual effects.
        """
        pass

        #TODO: move the algorithm in this method to level, alter it so that tiles are traversed in order from starttile to endtile,
        #      and use the tile list it creates when making the fired projectile traverse the given path.
    def draw_line_effect(self):
        """ tc.draw_line_effect( ) -> None

        Draws a line between the player and the current target.
        """

        if self.player.in_range(self.target_tile, 1):
            return
        
        level = self.player.current_level
        start_tile = self.player.current_tile
        end_tile = self.target_tile
        tile_line = level.tile_line(start_tile, end_tile)

        for t in tile_line:
            t.set_effect('*', CYAN)
        #self.draw_target_tile_effect()

        #TEMP FOR TESTING
        #tile_line[0].set_effect('$', Color("#FF0000"))
        #TEMP FOR TESTING

    def exit_to_main_game_controls(self, key = None):
        """ tc.exit_to_main_game_controls( None ) -> None

        Quit these targetining controls and resume the main game controls.
        """
        self.clear_effects()
        Controls.exit_to_main_game_controls(self)

exit = TargetControls.exit_to_main_game_controls
fire = TargetControls.fire_action
move = TargetControls.move_input

TARGET_CONTROL_MAP = {
    K_UP:move, K_DOWN:move, K_LEFT:move, K_RIGHT:move,          # arrow keys

    K_KP1:move, K_KP2:move, K_KP3:move, K_KP4:move, K_KP5:move, # numpad keys (might change 5 at some point)
    K_KP6:move, K_KP7:move, K_KP8:move, K_KP9:move,

    K_RETURN: fire, 'f': fire
}

TARGET_DIRECTION_MAP = {
    K_UP:(0, -1), K_DOWN:(0, 1), K_LEFT:(-1, 0), K_RIGHT:(1,0),

    K_KP1:(-1, 1), K_KP2:(0, 1), K_KP3:(1, 1), K_KP4:(-1, 0), K_KP5:(0, 0),
    K_KP6:(1, 0), K_KP7:(-1, -1), K_KP8:(0, -1), K_KP9:(1, -1)
}

SMITE = "smite"
LINE = "line"

TARGET_STYLE_EFFECT_MAP = {
    SMITE:TargetControls.draw_smite_effect,
    LINE:TargetControls.draw_line_effect
}
