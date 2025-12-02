from .sample import Button
from ... import root
from ...auxiliary_stuff import update_gui

class FractionButton(Button):
    def __init__(self):
        super().__init__(text="Fraction", width=100, height=50, color=(200, 200, 200), font_size=20, position=(10, 10), button_state="game")
    
    def click(self, button: int, mouse_pos: tuple[int, int]) -> bool:
        if button != 1: return False
        root.change_window_state("fraction")
        root.game_manager.gui.fraction.open_player_fraction()
        return super().click(button, mouse_pos)

class TechnologyButton(Button):
    def __init__(self):
        super().__init__(text="Technology", width=100, height=50, color=(200, 200, 200), font_size=20, position=(10, 10), button_state="game")
    
    def click(self, button: int, mouse_pos: tuple[int, int]) -> bool:
        if button != 1: return False
        root.change_window_state("technology")
        root.game_manager.gui.technology.open()
        return super().click(button, mouse_pos)

class PolicyButton(Button):
    def __init__(self):
        super().__init__(text="Policy", width=100, height=50, color=(200, 200, 200), font_size=20, position=(10, 10), button_state="game")
    
    def click(self, button: int, mouse_pos: tuple[int, int]) -> bool:
        if button != 1: return False
        root.change_window_state("policy")
        root.game_manager.gui.policy.open()
        return super().click(button, mouse_pos)
    
class NextTurnButton(Button):
    def __init__(self):
        super().__init__(text="", img="next_turn.png", width=50, height=50, color=(200, 200, 200), font_size=20, position=(10, 10), button_state="game")

    def click(self, button: int, mouse_pos: tuple[int, int]) -> bool:
        if button != 1: return False
        #gui.gui.turn_counter.change_value(1) #после сделать нормальную функцию для смены хода
        root.game_manager.turn_manager.do_step()
        root.game_manager.world_map.unchose_cell()
        return super().click(button, mouse_pos)

class BuildingButton(Button):
    def __init__(self):
        super().__init__(text="Open", width=100, height=50, color=(200, 200, 200), font_size=20, position=(10, 10), button_state="game", auto_process = False)

    def click(self, button: int, mouse_pos: tuple[int, int]) -> bool:
        if button != 1: return False
        root.game_manager.gui.building.open()
        root.change_window_state("building")
        update_gui()
        return super().click(button, mouse_pos)

class CancelUpgradeButton(Button):
    def __init__(self):
        super().__init__(text="Cancel", width=100, height=50, color=(200, 200, 200), font_size=20, position=(10, 10), button_state="game", auto_process = False)
    
    def click(self, button: int, mouse_pos: tuple[int, int]) -> bool:
        if button != 1: return False
        root.game_manager.get_chosen_building().cancel_upgrade_mod()
        update_gui()
        return super().click(button, mouse_pos)

class RecieptButton(Button):
    def __init__(self):
        super().__init__(text="Reciept", width=100, height=50, color=(200, 200, 200), font_size=20, position=(10, 10), button_state="game", auto_process = False)

    def click(self, button: int, mouse_pos: tuple[int, int]) -> bool:
        if button != 1: return False
        root.game_manager.gui.building.open()
        root.game_manager.gui.reciept.open()
        root.change_window_state("reciept")
        update_gui()
        return super().click(button, mouse_pos)

class OpenInventoryButton(Button):
    def __init__(self):
        super().__init__(text="Inventory", width=100, height=50, color=(200, 200, 200), font_size=20, position=(10, 10), button_state="game", auto_process = False)

    def click(self, button: int, mouse_pos: tuple[int, int]) -> bool:
        if button != 1: return False
        root.game_manager.gui.inventory.open()
        root.change_window_state("inventory")
        update_gui()
        return super().click(button, mouse_pos)

class OpneSpawnButton(Button):
    def __init__(self):
        super().__init__(text="Spawn", width=100, height=50, color=(200, 200, 200), font_size=20, position=(10, 10), button_state="game", auto_process = False)

    def click(self, button: int, mouse_pos: tuple[int, int]) -> bool:
        if button != 1: return False
        root.game_manager.gui.spawn.open()
        root.change_window_state("spawn")
        return super().click(button, mouse_pos)

class ShowJobButton(Button):
    def __init__(self):
        super().__init__(text="Job", width=100, height=50, color=(200, 200, 200), font_size=20, position=(10, 10), button_state="game", auto_process = False)

    def click(self, button: int, mouse_pos: tuple[int, int]) -> bool:
        if button != 1: return False
        root.game_manager.gui.game.show_jobs()
        return super().click(button, mouse_pos)

class SchemeListButton(Button):
    def __init__(self):
        super().__init__(text="Schemes", width=100, height=50, color=(200, 200, 200), font_size=20, position=(10, 10), button_state="game", auto_process = False)
    
    def click(self, button: int, mouse_pos: tuple[int, int]) -> bool:
        if button != 1: return False
        root.game_manager.gui.game.open_scheme_list()
        update_gui()
        return super().click(button, mouse_pos)