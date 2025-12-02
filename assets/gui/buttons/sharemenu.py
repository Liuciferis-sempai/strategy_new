from .sample import Button
from ... import root

class InventoryCellButton(Button):
    def __init__(self, width: int, height: int, resource_name: str, resource_amount: int, img: str):
        super().__init__(width=width, height=height, img=img, text="", button_state="share_menu")
        self.resource_name = resource_name
        self.resource_amount = resource_amount
    
    def click(self, button: int, mouse_pos: tuple[int, int]) -> bool:
        print(button)
        if button != 1 and button != 3: return False
        root.game_manager.gui.sharemenu.click(button, mouse_pos)
        return super().click(button, mouse_pos)