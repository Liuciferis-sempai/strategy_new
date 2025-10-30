import pygame as py
import assets.root as root
from assets.processing_input.basic_input_process import BasicInputProcessor

class FractionInputProcessor(BasicInputProcessor):
    def __init__(self, root_prcessor_input):
        super().__init__(root_prcessor_input)

    #@logger
    def process_keydown(self, event:py.event.Event):
        if self.process_keydown_for_inputfield(event): return root.update_gui()
        if self.process_keydown_base(event):
            return
        if event.key == py.K_ESCAPE:
            root.change_window_state("game")

    #@logger
    def process_mousebuttondown(self, event:py.event.Event):
        if self.process_mousebutton_for_inputfield(event): return root.update_gui()
        mouse_pos = event.pos
        if root.game_manager.gui.fraction.fraction_name_edit_button.rect.collidepoint(mouse_pos):
                root.game_manager.gui.fraction.fraction_name_edit_button.click()
        root.update_gui()