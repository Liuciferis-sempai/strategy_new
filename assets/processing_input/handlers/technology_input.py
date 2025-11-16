import pygame as py
import root
from processing_input.basic_input_process import BasicInputProcessor

class TechnologyInputProcessor(BasicInputProcessor):
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
        
        if event.button == 1:
            root.game_manager.tech_tree.collidepoint(mouse_pos)
        elif event.button == 3:
            root.game_manager.tech_tree.set_none_tech()
        elif event.button == 4:
            if self.root_processor.is_shift_pressed:
                root.game_manager.tech_tree.scroll_left()
            else:
                root.game_manager.tech_tree.scroll_up()
        elif event.button == 5:
            if self.root_processor.is_shift_pressed:
                root.game_manager.tech_tree.scroll_right()
            else:
                root.game_manager.tech_tree.scroll_down()
        root.update_gui()