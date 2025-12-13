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
        self.processor.click(self.text.strip())
        return super().click(button, mouse_pos)

class MessageLine(Button):
    def __init__(self, bg_color: tuple[int, int, int]|tuple[int, int, int, int], font_color: tuple[int, int, int], font_size: int, text: str, height: int, text_kwargs: dict, button_state: str, messanger_target: tuple[int, int, int]|None):
        super().__init__(text=text, text_kwargs=text_kwargs, height=height, color=bg_color, font_color=font_color, font_size=font_size, position=(10, 10), button_state=button_state, auto_width=True)
        self.messanger_target = messanger_target

    def click(self, button: int, mouse_pos: tuple[int, int]) -> bool:
        if self.messanger_target:
            root.game_manager.world_map.show_cell(self.messanger_target)
        return super().click(button, mouse_pos)