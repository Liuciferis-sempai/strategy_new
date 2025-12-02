from .sample import Button
from ... import root

class UseReciept(Button):
    def __init__(self, width: int, height: int, reciept_id: str, message: str, is_allowed: bool, img: str):
        super().__init__(width=width, height=height, img=img, text="", button_state="reciept")
        self.reciept_id = reciept_id
        self.message = message
        self.is_allowed = is_allowed
    
    def click(self, button: int, mouse_pos: tuple[int, int]) -> bool:
        if button != 1: return False
        if self.is_allowed:
            root.game_manager.reciept_manager.use_recipe(self.reciept_id)
        else:
            root.game_manager.messenger.print("reciept_is_not_allowed", {"reciept_id": self.reciept_id}, "warning")
        return super().click(button, mouse_pos)