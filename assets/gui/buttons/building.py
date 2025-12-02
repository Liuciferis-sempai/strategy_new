from .sample import Button
from ... import root
from ...auxiliary_stuff import update_gui

class UpgradeBuildingButton(Button):
    def __init__(self, width: int, height: int):
        super().__init__(text="upgrade", width=width, height=height, position=(10, 10), font_size=40, button_state="building")

    def click(self, button: int, mouse_pos: tuple[int, int]) -> bool:
        if button != 1: return False
        root.game_manager.get_chosen_building().set_upgrade_mod()
        root.change_window_state("game")
        update_gui()
        return super().click(button, mouse_pos)