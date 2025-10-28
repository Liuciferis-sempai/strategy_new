import pygame as py
import assets.root as root
from assets.processing_input.default_input_process import DefaultInputProcessor

class FractionInputProcessor(DefaultInputProcessor):
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
        if root.game.gui.fraction.fraction_name_edit_button.rect.collidepoint(mouse_pos):
                root.game.gui.fraction.fraction_name_edit_button.click()
        root.update_gui()