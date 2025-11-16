from .sample import Button
import assets.root as root

class UseReciept(Button):
    def __init__(self, width: int, height: int, value: str, is_allowed: bool, img: str):
        super().__init__(width=width, height=height, img=img, text="")
        self.value = value
        self.is_allowed = is_allowed
    
    def click(self):
        super().click()
        if self.is_allowed:
            root.game_manager.reciept_manager.use_recipe(self.value)
        else:
            root.game_manager.messenger.print("reciept_is_not_allowed", "warning")