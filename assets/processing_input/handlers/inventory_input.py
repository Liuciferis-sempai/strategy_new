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
        if event.key == py.K_ESCAPE:
            root.change_window_state("game")

    #@logger
    def process_mousebuttondown(self, event:py.event.Event, rel_mouse_pos:tuple[int, int]):
        #if self.game_manager.gui.inventory.owner_inventory:
        #    if event.button == 1:
        #        for cell, _ in self.game_manager.gui.inventory.owner_inventory:
        #            if cell.rect.collidepoint(rel_mouse_pos):
        #                self.game_manager.gui.inventory.click(event.button)
        #                return
        #    elif event.button == 3:
        #        for cell, _ in self.game_manager.gui.inventory.owner_inventory:
        #            if cell.rect.collidepoint(rel_mouse_pos):
        #                self.game_manager.gui.inventory.click(event.button)
        #                return
        pass