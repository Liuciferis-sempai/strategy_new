import pygame as py
from ... import root
from ..basic_input_process import BasicInputProcessor
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...gamemanager import GameManager

class BuildingInputProcessor(BasicInputProcessor):
    def __init__(self, root_prcessor_input, game_manager: "GameManager"):
        super().__init__(root_prcessor_input, game_manager)

    #@logger
    def process_keydown(self, event:py.event.Event):
        if self.process_keydown_for_inputfield(event): return root.update_gui()
        if self.process_keydown_base(event):
            return
        if event.key == py.K_ESCAPE:
                self.game_manager.gui.building.close()
                root.change_window_state("game")
    
    #@logger
    def process_mousebuttondown(self, event:py.event.Event):
        mouse_pos = event.pos
        rel_mouse_pos = (mouse_pos[0], mouse_pos[1]+self.game_manager.gui.building.y_global_offset)

        if self.process_mousebutton_for_inputfield(rel_mouse_pos): return root.update_gui()

        if event.button == 1:
            if self.game_manager.gui.building.building.is_workbench:
                if self.game_manager.gui.building.building_reciept_button.rect.collidepoint(rel_mouse_pos):
                    self.game_manager.gui.building.building_reciept_button.click()
            if self.game_manager.gui.building.building.can_be_upgraded():
                if self.game_manager.gui.building.upgrade_building_button.rect.collidepoint(rel_mouse_pos):
                    self.game_manager.gui.building.upgrade_building_button.click()
        root.update_gui()