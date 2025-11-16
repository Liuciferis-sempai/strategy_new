from .sample import Button
import assets.root as root
from assets.auxiliary_stuff import update_gui

class UpgradeBuildingButton(Button):
    def __init__(self, width: int, height: int):
        super().__init__(text="upgrade", width=width, height=height, position=(10, 10), font_size=40)

    def click(self):
        root.game_manager.buildings_manager.get_building_by_coord(root.game_manager.get_chosen_cell_coord()).set_upgrade_mod(True)
        root.change_window_state("game")
        update_gui()
        super().click()