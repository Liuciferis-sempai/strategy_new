from .sample import Button
import root
from auxiliary_stuff.functions import update_gui

class FractionNameEditButton(Button):
    def __init__(self):
        super().__init__(text="Edit", width=50, height=50, color=(200, 200, 200, 0), font_size=20, position=(10, 10))
    
    def click(self):
        root.change_window_state("writing")
        root.game_manager.gui.writing.writing = "Fraction Name"
        root.game_manager.gui.writing.start_writing()
        super().click()

class InputSubmitButton(Button):
    def __init__(self):
        super().__init__(text="Submit", width=100, height=50, color=(200, 200, 200), font_size=20, position=(10, 10))
    
    def click(self):
        root.game_manager.gui.writing.submit_input()
        super().click()

#Building's buttons
class WorkbenchButton(Button):
    def __init__(self):
        super().__init__(text="", img="reciept.png", width=100, height=100, position=(10, 10))

    def click(self):
        root.game_manager.gui.reciept.open()
        root.change_window_state("reciept")
        update_gui()
        super().click()