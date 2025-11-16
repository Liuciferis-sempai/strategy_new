import pygame as py
from pygame.event import Event
import assets.root as root
from assets.processing_input.basic_input_process import BasicInputProcessor

class SpawnInputProcessor(BasicInputProcessor):
    def __init__(self, root_prcessor_input):
        super().__init__(root_prcessor_input)

    #@logger
    def process_keydown(self, event:py.event.Event):
        if self.process_keydown_for_inputfield(event): return root.update_gui()
        if self.process_keydown_base(event): return

        if event.key == py.K_ESCAPE:
            root.change_window_state("game")
    
    #@logger
    def process_mousebuttondown(self, event:py.event.Event):
        if self.process_mousebutton_for_inputfield(event): return root.update_gui()
        mouse_pos = event.pos
        if event.button == 1:
            rel_mouse_pos = (mouse_pos[0], mouse_pos[1]+root.game_manager.gui.spawn.y_offset)
            for button in root.game_manager.gui.spawn.buttons:
                if button.rect.collidepoint(rel_mouse_pos):
                    button.click()
        elif event.button == 4:
            root.game_manager.gui.spawn.y_offset += root.interface_size//8
        elif event.button == 5:
            root.game_manager.gui.spawn.y_offset -= root.interface_size//8