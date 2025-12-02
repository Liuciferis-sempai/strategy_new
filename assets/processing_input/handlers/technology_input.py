import pygame as py
from ... import root
from ..basic_input_process import BasicInputProcessor
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...gamemanager import GameManager

class TechnologyInputProcessor(BasicInputProcessor):
    def __init__(self, root_prcessor_input, game_manager: "GameManager"):
        super().__init__(root_prcessor_input, game_manager)

    #@logger
    def process_keydown(self, event:py.event.Event):
        if event.key == py.K_ESCAPE:
            root.change_window_state("game")
    
    #@logger
    def process_mousebuttondown(self, event:py.event.Event, rel_mouse_pos:tuple[int, int]):
        #if event.button == 1:
        #    self.game_manager.tech_tree.collidepoint(rel_mouse_pos)
        if event.button == 3:
            self.game_manager.tech_tree.set_none_tech()
        elif event.button == 4:
            if self.root_processor.is_shift_pressed:
                self.game_manager.tech_tree.scroll_left()
            else:
                self.game_manager.tech_tree.scroll_up()
        elif event.button == 5:
            if self.root_processor.is_shift_pressed:
                self.game_manager.tech_tree.scroll_right()
            else:
                self.game_manager.tech_tree.scroll_down()
        root.update_gui()