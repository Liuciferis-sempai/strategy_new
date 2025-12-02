from .sample import Button
from ... import root
from ...auxiliary_stuff import update_gui

class FractionButton(Button):
    def __init__(self):
        super().__init__(text="Fraction", width=100, height=50, color=(200, 200, 200), font_size=20, position=(10, 10))
    
    def click(self):
        root.change_window_state("fraction")
        root.game_manager.gui.fraction.open_player_fraction()
        super().click()

class TechnologyButton(Button):
    def __init__(self):
        super().__init__(text="Technology", width=100, height=50, color=(200, 200, 200), font_size=20, position=(10, 10))
    
    def click(self):
        root.change_window_state("technology")
        root.game_manager.gui.technology.open()
        super().click()

class PolicyButton(Button):
    def __init__(self):
        super().__init__(text="Policy", width=100, height=50, color=(200, 200, 200), font_size=20, position=(10, 10))
    
    def click(self):
        root.change_window_state("policy")
        root.game_manager.gui.policy.open()
        super().click()
    
class NextTurnButton(Button):
    def __init__(self):
        super().__init__(text="", img="next_turn.png", width=50, height=50, color=(200, 200, 200), font_size=20, position=(10, 10))

    def click(self):
        super().click()
        #gui.gui.turn_counter.change_value(1) #после сделать нормальную функцию для смены хода
        root.game_manager.turn_manager.do_step()
        root.game_manager.world_map.unchose_cell()

class BuildingButton(Button):
    def __init__(self):
        super().__init__(text="Open", width=100, height=50, color=(200, 200, 200), font_size=20, position=(10, 10))

    def click(self):
        root.game_manager.gui.building.open()
        root.change_window_state("building")
        update_gui()
        super().click()

class CancelUpgradeButton(Button):
    def __init__(self):
        super().__init__(text="Cancel", width=100, height=50, color=(200, 200, 200), font_size=20, position=(10, 10))
    
    def click(self):
        root.game_manager.get_chosen_building().cancel_upgrade_mod()
        update_gui()
        super().click()

class RecieptButton(Button):
    def __init__(self):
        super().__init__(text="Reciept", width=100, height=50, color=(200, 200, 200), font_size=20, position=(10, 10))

    def click(self):
        root.game_manager.gui.building.open()
        root.game_manager.gui.reciept.open()
        root.change_window_state("reciept")
        update_gui()
        super().click()

class OpenInventoryButton(Button):
    def __init__(self):
        super().__init__(text="Inventory", width=100, height=50, color=(200, 200, 200), font_size=20, position=(10, 10))

    def click(self):
        root.game_manager.gui.inventory.open()
        root.change_window_state("inventory")
        update_gui()
        super().click()

class OpneSpawnButton(Button):
    def __init__(self):
        super().__init__(text="Spawn", width=100, height=50, color=(200, 200, 200), font_size=20, position=(10, 10))

    def click(self):
        root.game_manager.gui.spawn.open()
        root.change_window_state("spawn")
        super().click()

class JobButton(Button):
    def __init__(self, text:str, position:tuple[int, int]):
        super().__init__(text=text, width=200, height=20, color=(200, 200, 200), font_size=20, position=position)

class ShowJobButton(Button):
    def __init__(self):
        super().__init__(text="Job", width=100, height=50, color=(200, 200, 200), font_size=20, position=(10, 10))

    def click(self):
        root.game_manager.gui.game.show_jobs()
        super().click()

class SchemeListButton(Button):
    def __init__(self):
        super().__init__(text="Schemes", width=100, height=50, color=(200, 200, 200), font_size=20, position=(10, 10))
    
    def click(self):
        root.game_manager.gui.game.open_scheme_list()
        update_gui()
        super().click()