import pygame as py
import assets.root as root
from assets.processing_input.default_input_process import DefaultInputProcessor

class BuildingInputProcessor(DefaultInputProcessor):
    def __init__(self, root_prcessor_input):
        super().__init__(root_prcessor_input)

    #@logger
    def process_keydown(self, event:py.event.Event):
        if self.process_keydown_base(event):
            return
        if event.key == py.K_ESCAPE:
                root.change_window_state("game")
    
    #@logger
    def process_mousebuttondown(self, event:py.event.Event):
        mouse_pos = event.pos
        if event.button == 1:
            if root.game.gui.building.building_reciept_button.rect.collidepoint(mouse_pos):
                root.game.gui.building.building_reciept_button.click()
            if root.game.gui.building.upgrade_building_button.rect.collidepoint(mouse_pos):
                root.game.gui.building.upgrade_building_button.click()
        root.update_gui()