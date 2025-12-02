import pygame as py
from ... import root
from ..basic_input_process import BasicInputProcessor
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...gamemanager import GameManager

class RecieptInputProcessor(BasicInputProcessor):
    def __init__(self, root_prcessor_input, game_manager: "GameManager"):
        super().__init__(root_prcessor_input, game_manager)

    #@logger
    def process_keydown(self, event:py.event.Event):
        if event.key == py.K_ESCAPE:
            root.change_window_state("building")
    
    #@logger
    def process_mousebuttondown(self, event:py.event.Event, rel_mouse_pos:tuple[int, int]):
        #if event.button == 1:
        #    for button in self.game_manager.gui.reciept.buttons:
        #        if button.rect.collidepoint(rel_mouse_pos):
        #            button.click()
        if event.button == 4:
            root.game_manager.gui.reciept.move_up()
        elif event.button == 5:
            root.game_manager.gui.reciept.move_down()
        root.update_gui()