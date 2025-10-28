import pygame as py
import assets.root as root
from assets.processing_input.default_input_process import DefaultInputProcessor

class TechnologyInputProcessor(DefaultInputProcessor):
    def __init__(self, root_prcessor_input):
        super().__init__(root_prcessor_input)

    #@logger
    def process_keydown(self, event:py.event.Event):
        if self.process_keydown_base(event):
            return

        if event.key == py.K_w:
            root.game.tech_tree.scroll_up()
        elif event.key == py.K_s:
            root.game.tech_tree.scroll_down()
        elif event.key == py.K_a:
            root.game.tech_tree.scroll_left()
        elif event.key == py.K_d:
            root.game.tech_tree.scroll_right()
        elif event.key == py.K_ESCAPE:
            root.change_window_state("game")
    
    #@logger
    def process_mousebuttondown(self, event:py.event.Event):
        mouse_pos = event.pos
        if event.button == 1:
            root.game.tech_tree.collidepoint(mouse_pos)
        elif event.button == 3:
            root.game.tech_tree.set_none_tech()
        elif event.button == 4:
            if self.is_shift_pressed:
                root.game.tech_tree.scroll_left()
            else:
                root.game.tech_tree.scroll_up()
        elif event.button == 5:
            if self.is_shift_pressed:
                root.game.tech_tree.scroll_right()
            else:
                root.game.tech_tree.scroll_down()
        root.update_gui()