from .sample import Button
from ... import root

class SpawnPawn(Button):
    def __init__(self, width: int, height: int, pawn_type: str, message: str, is_allowed: bool, img: str):
        super().__init__(width=width, height=height, img=img, text="", button_state="")
        self.pawn_type = pawn_type
        self.message = message
        self.is_allowed = is_allowed

    def click(self, button: int, mouse_pos: tuple[int, int]) -> bool:
        if button != 1: return False
        if self.is_allowed:
            root.game_manager.town_manager.get_town_by_coord(root.game_manager.get_chosen_cell_coord()).spawn(self.pawn_type)
        else:
            root.game_manager.messenger.print(self.message, {"pawn_type": self.pawn_type}, "warning")
        return super().click(button, mouse_pos)