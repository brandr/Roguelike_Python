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
        self.player.send_event("Firing!")
        self.clear_effects()
        coords = self.target_tile.coordinates()
        self.action(self.arg, coords[0], coords[1])
        self.exit_to_main_game_controls()

    def move_input(self, key):
        if(key in TARGET_DIRECTION_MAP):
            direction = TARGET_DIRECTION_MAP[key]
            self.move_target(direction)

    def move_target(self, direction):
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
        self.player.current_level.clear_effects()

    def draw_effects(self):
        if self.target_style in TARGET_STYLE_EFFECT_MAP:
            effect_method = TARGET_STYLE_EFFECT_MAP[self.target_style]
            effect_method(self)
        self.draw_target_tile_effect()

    def draw_target_tile_effect(self):
        self.target_tile.set_effect(DEFAULT_TARGET_SYMBOL, CYAN)
        self.target_tile.update()

    def draw_smite_effect(self):
        pass

    def draw_line_effect(self):
        if self.player.in_range(self.target_tile, 1):
            return
        
        level = self.player.current_level
        line_tiles = []
        start_tile = self.player.current_tile
        end_tile = self.target_tile

        x_dist = end_tile.x - start_tile.x
        y_dist = end_tile.y - start_tile.y

        if abs(x_dist) > abs(y_dist): # x is the independent variable
            slope = float( float(y_dist)/float(x_dist) )
            min_x = min(start_tile.x, end_tile.x)
            max_x = max(start_tile.x, end_tile.x)
            current_x = min_x + 1
            if start_tile.x < end_tile.x:
                start_y = start_tile.y
            else:
                start_y = end_tile.y
            while current_x < max_x:
                x_off = current_x - min_x
                current_y = int(x_off*slope + start_y)
                line_tiles.append(level.tile_at(current_x, current_y))
                current_x += 1      
        else:                         # y is the independent variable
            slope = float( float(x_dist)/float(y_dist) )
            min_y = min(start_tile.y, end_tile.y)
            max_y = max(start_tile.y, end_tile.y)
            current_y = min_y + 1
            if start_tile.y < end_tile.y:
                start_x = start_tile.x
            else:
                start_x = end_tile.x
            while current_y < max_y:
                y_off = current_y - min_y
                current_x = int(y_off*slope + start_x)
                line_tiles.append(level.tile_at(current_x, current_y))
                current_y += 1
        # TODO
        for t in line_tiles:
            t.set_effect('*', CYAN)

    def exit_to_main_game_controls(self, key = None):
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
