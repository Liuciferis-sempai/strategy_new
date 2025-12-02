from .sample import Button
from ... import root
from ...auxiliary_stuff.functions import update_gui

class FractionNameEditButton(Button):
    def __init__(self):
        super().__init__(text="Edit", width=50, height=50, color=(200, 200, 200, 0), font_size=20, position=(10, 10), button_state="fraction")
    
    def click(self, button: int, mouse_pos: tuple[int, int]) -> bool:
        if button != 1: return False
        root.change_window_state("writing")
        root.game_manager.gui.writing.writing = "Fraction Name"
        root.game_manager.gui.writing.start_writing()
        return super().click(button, mouse_pos)

class InputSubmitButton(Button):
    def __init__(self):
        super().__init__(text="Submit", width=100, height=50, color=(200, 200, 200), font_size=20, position=(10, 10), button_state="fraction")
    
    def click(self, button: int, mouse_pos: tuple[int, int]) -> bool:
        if button != 1: return False
        root.game_manager.gui.writing.submit_input()
        return super().click(button, mouse_pos)

#Building's buttons
class WorkbenchButton(Button):
    def __init__(self):
        super().__init__(text="", img="reciept.png", width=100, height=100, position=(10, 10), button_state="fraction")

    def click(self, button: int, mouse_pos: tuple[int, int]) -> bool:
        if button != 1: return False
        root.game_manager.gui.reciept.open()
        root.change_window_state("reciept")
        update_gui()
        return super().click(button, mouse_pos)