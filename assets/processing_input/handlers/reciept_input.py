import pygame as py
import assets.root as root
from assets.processing_input.default_input_process import DefaultInputProcessor

class RecieptInputProcessor(DefaultInputProcessor):
    def __init__(self, root_prcessor_input):
        super().__init__(root_prcessor_input)

    #@logger
    def process_keydown(self, event:py.event.Event):
        if self.process_keydown_base(event):
            return
        if event.key == py.K_ESCAPE:
                root.change_window_state("building")
                root.game.gui.reciept.reciept_y_offset = 0
    
    #@logger
    def process_mousebuttondown(self, event:py.event.Event):
        mouse_pos = event.pos
        if event.button == 1 and root.game.gui.reciept.reciepts != None:
            root.game.reciept_manager.use_recipe(mouse_pos)
        elif event.button == 4:
            root.game.gui.reciept.reciept_y_offset += root.interface_size//8
        elif event.button == 5:
            root.game.gui.reciept.reciept_y_offset -= root.interface_size//8
        root.update_gui()