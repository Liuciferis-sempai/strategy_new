from .sample import Button
from ... import root
from ...auxiliary_stuff import update_gui

class UpgradeBuildingButton(Button):
    def __init__(self, width: int, height: int):
        super().__init__(text="upgrade", width=width, height=height, position=(10, 10), font_size=40)

    def click(self):
        root.game_manager.get_chosen_building().set_upgrade_mod()
        root.change_window_state("game")
        update_gui()
        super().click()