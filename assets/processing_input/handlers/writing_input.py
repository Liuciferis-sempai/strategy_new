import pygame as py
import assets.root as root
from assets.processing_input.default_input_process import DefaultInputProcessor

class WritingInputProcessor(DefaultInputProcessor):
    def __init__(self, root_prcessor_input):
        super().__init__(root_prcessor_input)

    #@logger
    def process_keydown(self, event:py.event.Event):
        if self.process_keydown_base(event):
            return
        
        if event.key == py.K_RETURN:
            root.game.gui.writing.submit_input()
        elif event.key == py.K_BACKSPACE:
            root.input = root.input[:-1]
        elif event.key == py.K_ESCAPE:
            root.game.gui.writing.close(False)
        else:
            if len(root.input) < 20:
                root.input += event.unicode
        root.game.gui.writing.update_input_field()
    
    #@logger
    def process_mousebuttondown(self, event:py.event.Event):
        mouse_pos = event.pos
        if root.game.gui.writing.submit_button.rect.collidepoint(mouse_pos):
                root.game.gui.writing.submit_button.click()
        root.update_gui()