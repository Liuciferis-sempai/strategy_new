import pygame as py
import assets.root as root
#from assets.processing_input.proccessing_input import InputKeyProcessor

class BasicInputProcessor:
    def __init__(self, root_prcessor_input):
        self.root_processor = root_prcessor_input

    def process_keydown_for_inputfield(self, event:py.event.Event) -> bool:
        if root.input_field_active:
            if event.key != py.K_CARET:
                root.game_manager.get_chosen_inputfield().key_down(event)
                return True
        return False

    def process_mousebutton_for_inputfield(self, mouse_pos: tuple[int, int]) -> bool:
        for inputfield in root.game_manager.input_fields:
            if inputfield.rect.collidepoint(mouse_pos) and not inputfield.hidden:
                inputfield.click()
                return True
        root.input_field_active = False
        return False

    #@logger
    def process_keydown_base(self, event:py.event.Event) -> bool:
        if event.key == py.K_LCTRL or event.key == py.K_RCTRL:
            self.root_processor.is_ctrl_pressed = True
            return True
        elif event.key == py.K_LSHIFT or event.key == py.K_RSHIFT:
            self.root_processor.is_shift_pressed = True
            return True
        elif event.key == py.K_LALT or event.key == py.K_RALT:
            self.root_processor.is_alt_pressed = True
            return True
        elif event.key == py.K_w:
            self.root_processor.k_w_pressed = True
        elif event.key == py.K_a:
            self.root_processor.k_a_pressed = True
        elif event.key == py.K_s:
            self.root_processor.k_s_pressed = True
        elif event.key == py.K_d:
            self.root_processor.k_d_pressed = True

        return False