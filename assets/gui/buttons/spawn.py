from .sample import Button
from ... import root

class SpawnPawn(Button):
    def __init__(self, width: int, height: int, value: str, message: str, is_allowed: bool, img: str):
        super().__init__(width=width, height=height, img=img, text="")
        self.value = value
        self.message = message
        self.is_allowed = is_allowed

    def click(self):
        if self.is_allowed:
            root.game_manager.town_manager.get_town_by_coord(root.game_manager.get_chosen_cell_coord()).spawn(self.value)
        else:
            root.game_manager.messenger.print(self.message, "warning")