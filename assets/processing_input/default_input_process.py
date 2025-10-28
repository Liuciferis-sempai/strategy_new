import pygame as py
import assets.root as root
from assets.world.cell import Cell

class DefaultInputProcessor:
    def __init__(self, root_prcessor_input):
        self.root_processor = root_prcessor_input

        self.is_ctrl_pressed = False
        self.is_shift_pressed = False
        self.is_alt_pressed = False

        self.k_a_pressed = False
        self.k_d_pressed = False
        self.k_s_pressed = False
        self.k_w_pressed = False

        self.default_cell = Cell()
        self.cell_under_mouse = self.default_cell
    
    #@logger
    def process_keydown_base(self, event:py.event.Event) -> bool:
        if event.key == py.K_LCTRL or event.key == py.K_RCTRL:
            self.is_ctrl_pressed = True
            return True
        elif event.key == py.K_LSHIFT or event.key == py.K_RSHIFT:
            self.is_shift_pressed = True
            return True
        elif event.key == py.K_LALT or event.key == py.K_RALT:
            self.is_alt_pressed = True
            return True

        elif event.key == py.K_ESCAPE:
            timed_variable = root.window_state
            root.window_state = root.last_window_state
            root.last_window_state = timed_variable
            root.update_gui()
        return False