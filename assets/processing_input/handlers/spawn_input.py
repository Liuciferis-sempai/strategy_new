import pygame as py
from pygame.event import Event
from ... import root
from ..basic_input_process import BasicInputProcessor
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...gamemanager import GameManager

class SpawnInputProcessor(BasicInputProcessor):
    def __init__(self, root_prcessor_input, game_manager: "GameManager"):
        super().__init__(root_prcessor_input, game_manager)

    #@logger
    def process_keydown(self, event:py.event.Event):
        if self.process_keydown_for_inputfield(event): return root.update_gui()
        if self.process_keydown_base(event): return

        if event.key == py.K_ESCAPE:
            root.change_window_state("game")
    
    #@logger
    def process_mousebuttondown(self, event:py.event.Event):
        mouse_pos = event.pos
        rel_mouse_pos = (mouse_pos[0], mouse_pos[1]+self.game_manager.gui.spawn.y_offset)
        if self.process_mousebutton_for_inputfield(rel_mouse_pos): return root.update_gui()
        
        if event.button == 1:
            for button in self.game_manager.gui.spawn.buttons:
                if button.rect.collidepoint(rel_mouse_pos):
                    button.click()
        elif event.button == 4:
            self.game_manager.gui.spawn.y_offset += root.interface_size//8
        elif event.button == 5:
            self.game_manager.gui.spawn.y_offset -= root.interface_size//8