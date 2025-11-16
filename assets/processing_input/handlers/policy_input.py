import pygame as py
from ... import root
from ..basic_input_process import BasicInputProcessor

class PolicyInputProcessor(BasicInputProcessor):
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
        mouse_pos = event.pos
        if self.process_mousebutton_for_inputfield(mouse_pos): return root.update_gui()
        
        if event.button == 4:
            root.game_manager.gui.policy.scroll_up()
        elif event.button == 5:
            root.game_manager.gui.policy.scroll_down()
        root.update_gui()