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
        """GM.runGame ( Surface ) -> None

        Run the game using a pygame screen.

        Currently uses a bunch of temporary elements for testing gameplay.
        Will change depending on what we are currently testing.
        Eventually, this should probably open up a title screen or something.
        """
        pygame.display.set_caption("DIS A ROGUELIKE")
        timer = pygame.time.Clock()

        # TEMP for testing vvv
        # comment and uncomment to change what is on the level.

        # weapons
        sword_1 = MeleeWeapon("Master Sword", AXE)
        sword_2 = MeleeWeapon("Biggoron's Axe", LONG_BLADE, True) #TODO: implement 2H weapons

        # armor
        shield_1 = Armor("Hylian Shield", LEFT_HAND_SLOT)
        hat_1 = Armor("Fairy Hat", HEAD_SLOT)
        chest_1 = Armor("Kokiri Tunic", CHEST_SLOT)
        gloves_1 = Armor("Leather Gloves", GLOVES_SLOT)
        ring_1 = Armor("Fire Ring", RING1_SLOT)
        ring_2 = Armor("Ice Ring", RING2_SLOT)
        cloak_1 = Armor("Zora Cloak", CLOAK_SLOT)

        health_potion = HealingPotion()
        poison_potion = PoisonPotion()
        ammo_1 = Ammo("Wooden Arrow", 20)

        monster_sword = MeleeWeapon("Deku axe", AXE)
        monster_shield = Armor("Deku Shield", LEFT_HAND_SLOT)

        player_1 = Player("Link") 
        #TODO: later, we should consider a better way to build equipmentsets from groups of equipment. Maybe read in and parse some file?
        player_equipment = EquipmentSet(HUMANOID)
        player_equipment.wield_item(sword_1)
        player_equipment.equip_item(shield_1)
        player_equipment.equip_item(hat_1)
        player_equipment.equip_item(chest_1)
        player_equipment.equip_item(gloves_1)
        player_equipment.equip_item(ring_1)
        player_equipment.equip_item(ring_2)
        player_equipment.equip_item(cloak_1)

        player_1.set_start_equipment(player_equipment)
        player_1.obtain_item(health_potion)
        player_1.obtain_item(poison_potion)
        player_1.obtain_item(ammo_1)
        player_1.obtain_item(sword_2)

        monster_1 = Monster("Moblin")
        monster_equipment = EquipmentSet(HUMANOID) #TODO: this is the long-term plan for starting monster/player equipment: make the equipmentset first, and then set it.
        monster_equipment.wield_item(monster_sword)
        monster_equipment.equip_item(monster_shield)
        monster_1.set_start_equipment(monster_equipment)
        #monster_1.obtain_item(monster_sword)

        monster_2 = Monster("Bokoblin")

        test_level = Level(25, 25, 1) 
        test_level.add_wall(15, 15)
        test_level.add_wall(16, 15)

        test_level.add_player(player_1, 4, 4)
        test_level.add_monster(monster_1, 8, 8)
        #test_level.add_monster(monster_2, 18, 16)

        map_pane = MapPane(player_1)                # TODO: turn these 4 lines into their own method somewhere in the screen/manager mess.
        character_pane = CharacterPane(player_1)
        event_pane = EventPane(player_1)
        main_screen_panes = [character_pane, map_pane, event_pane] 

        #inventory_item_pane = InventoryItemPane() #not putting args in yet, because this could apply to the player, tiles, or other stuff

        test_level.plan_monster_turns()            #an initial requirement to set the turncounter in motion.
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
            screen_manager.update_objects()
            screen_manager.update_current_screen()
            self.draw_panes(screen_manager)
            pygame.display.update()

    def draw_panes(self, screen_manager):
        """ gm.draw_panes( ScreenManager ) -> None

        Update the screen by making it draw all its current panes.
        """
        screen_manager.draw_panes()
