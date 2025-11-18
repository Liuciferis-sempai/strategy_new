import pygame as py
from ... import root
from ..basic_input_process import BasicInputProcessor
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...gamemanager import GameManager

class InventoryInputProcessor(BasicInputProcessor):
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
        if self.process_mousebutton_for_inputfield(mouse_pos): return root.update_gui()
        
        #if self.game_manager.gui.inventory.owner_inventory:
        #    if event.button == 1:
        #        for cell, _ in self.game_manager.gui.inventory.owner_inventory:
        #            if cell.rect.collidepoint(mouse_pos):
        #                self.game_manager.gui.inventory.click(event.button)
        #                return
        #    elif event.button == 3:
        #        for cell, _ in self.game_manager.gui.inventory.owner_inventory:
        #            if cell.rect.collidepoint(mouse_pos):
        #                self.game_manager.gui.inventory.click(event.button)
        #                return