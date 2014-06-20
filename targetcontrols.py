from controls import *

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
    def __init__(self, action, action_range, target_style, player):
        controls.__init__(self)
        self.initialize_control_map(TARGET_CONTROL_MAP)
        self.action = action
        self.action_range = action_range
        self.target_style = "smite"
        self.player = player

    def action():
        self.player.send_event("Firing!")
        self.exit_to_main_game_controls()


    def process_event(self, event): #Overridden from the control class.
        """ c.process_event( EVent ) -> None

        Process a keyboard event and execute the associated action.
        In this context, cancels firing if the action isn't in the map.
        Gun safety!
        """
        if event.type == QUIT:
            raise(SystemExit)
        if event.type == KEYDOWN:
            if event.unicode in(self.control_map):
                action = self.control_map[event.unicode]
                action(self, event.unicode)
            elif event.key in(self.control_map):
                action = self.control_map[event.key]
                action(self, event.key)
            else:
                self.exit_to_main_game_controls
                self.player.send_event("I guess not.")


exit = Controls.exit_to_main_game_screen
fire = TargetControls.action

TARGET_CONTROL_MAP = {
    ' ': fire, 'f': fire
}
