import pygame as py
from ... import root
from ..basic_input_process import BasicInputProcessor
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...gamemanager import GameManager

class WritingInputProcessor(BasicInputProcessor):
    def __init__(self, root_prcessor_input, game_manager: "GameManager"):
        super().__init__(root_prcessor_input, game_manager)

    #@logger
    def process_keydown(self, event:py.event.Event):
        if event.key == py.K_RETURN:
            self.game_manager.gui.writing.submit_input()
        elif event.key == py.K_BACKSPACE:
            self.game_manager.gui.writing.input = self.game_manager.gui.writing.input[:-1]
        elif event.key == py.K_ESCAPE:
            self.game_manager.gui.writing.close(False)
        else:
            if len(self.game_manager.gui.writing.input) < 20:
                self.game_manager.gui.writing.input += event.unicode
        self.game_manager.gui.writing.update_input_field()
    
    #@logger
    def process_mousebuttondown(self, event:py.event.Event, rel_mouse_pos:tuple[int, int]):
        #if self.game_manager.gui.writing.submit_button.rect.collidepoint(rel_mouse_pos):
        #        self.game_manager.gui.writing.submit_button.click()
        #root.update_gui()
        pass