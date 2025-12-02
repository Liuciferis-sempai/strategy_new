import pygame as py
from ... import root
from ..basic_input_process import BasicInputProcessor
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...gamemanager import GameManager

class PolicyInputProcessor(BasicInputProcessor):
    def __init__(self, root_prcessor_input, game_manager: "GameManager"):
        super().__init__(root_prcessor_input, game_manager)

    #@logger
    def process_keydown(self, event:py.event.Event):
        if event.key == py.K_ESCAPE:
            root.change_window_state("game")

    #@logger
    def process_mousebuttondown(self, event:py.event.Event, rel_mouse_pos:tuple[int, int]):
        #if event.button == 1:
        #    self.game_manager.gui.policy.click(rel_mouse_pos)
        if event.button == 4:
            self.game_manager.gui.policy.move_up()
        elif event.button == 5:
            self.game_manager.gui.policy.move_down()
        root.update_gui()