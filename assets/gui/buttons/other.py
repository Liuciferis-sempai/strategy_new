from .sample import Button
from ... import root
from ...auxiliary_stuff import update_gui

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..listof import ListOf

class ListButton(Button):
    def __init__(self, text:str, position:tuple[int, int], button_state: str, processor: "ListOf"):
        super().__init__(text=text, width=200, height=20, color=(200, 200, 200), font_size=20, position=position, button_state=button_state)
        self.processor = processor
    
    def click(self, button: int, mouse_pos: tuple[int, int]) -> bool:
        if button != 1: return False
        self.processor.click(self.text)
        return super().click(button, mouse_pos)