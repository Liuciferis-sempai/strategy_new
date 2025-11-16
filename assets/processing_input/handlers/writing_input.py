import pygame as py
from ... import root
from ..basic_input_process import BasicInputProcessor

class WritingInputProcessor(BasicInputProcessor):
    def __init__(self, root_prcessor_input):
        super().__init__(root_prcessor_input)

    #@logger
    def process_keydown(self, event:py.event.Event):
        if self.process_keydown_for_inputfield(event): return root.update_gui()
        if self.process_keydown_base(event): return

        if event.key == py.K_RETURN:
            root.game_manager.gui.writing.submit_input()
        elif event.key == py.K_BACKSPACE:
            root.game_manager.gui.writing.input = root.game_manager.gui.writing.input[:-1]
        elif event.key == py.K_ESCAPE:
            root.game_manager.gui.writing.close(False)
        else:
            if len(root.game_manager.gui.writing.input) < 20:
                root.game_manager.gui.writing.input += event.unicode
        root.game_manager.gui.writing.update_input_field()
    
    #@logger
    def process_mousebuttondown(self, event:py.event.Event):
        mouse_pos = event.pos
        if self.process_mousebutton_for_inputfield(mouse_pos): return root.update_gui()
        
        if root.game_manager.gui.writing.submit_button.rect.collidepoint(mouse_pos):
                root.game_manager.gui.writing.submit_button.click()
        root.update_gui()