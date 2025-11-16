import pygame as py
from ... import root
from ..basic_input_process import BasicInputProcessor

class ShareMenuInputProcessor(BasicInputProcessor):
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
        mouse_pos = event.pos
        if self.process_mousebutton_for_inputfield(mouse_pos): return root.update_gui()
        
        if event.button in [1, 3]:
            for cell, _ in root.game_manager.gui.sharemenu.share_starter_inventory:
                if cell.rect.collidepoint(mouse_pos):
                    root.game_manager.gui.sharemenu.click(cell, "starter", event.button)
                    return
            if isinstance(root.game_manager.gui.sharemenu.share_target_inventory, list):
                for cell, _ in root.game_manager.gui.sharemenu.share_target_inventory:
                    if cell.rect.collidepoint(mouse_pos):
                        root.game_manager.gui.sharemenu.click(cell, "target", event.button)
                        return
            elif isinstance(root.game_manager.gui.sharemenu.share_starter_inventory, dict):
                for inventory_type in root.game_manager.gui.sharemenu.share_target_inventory.keys(): #type: ignore
                    for cell, _ in root.game_manager.gui.sharemenu.share_target_inventory[inventory_type]:
                        if cell.rect.collidepoint(mouse_pos):
                            root.game_manager.gui.sharemenu.click(cell, "target", event.button)
                            return