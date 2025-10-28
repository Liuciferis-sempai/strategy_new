import pygame as py
import assets.root as root
from assets.processing_input.default_input_process import DefaultInputProcessor

class ShareMenuInputProcessor(DefaultInputProcessor):
    def __init__(self, root_prcessor_input):
        super().__init__(root_prcessor_input)

    #@logger
    def process_keydown(self, event:py.event.Event):
        if self.process_keydown_base(event):
            return

        if event.key == py.K_ESCAPE:
            root.change_window_state("game")
    
    #@logger
    def process_mousebuttondown(self, event:py.event.Event):
        mouse_pos = event.pos
        if event.button in [1, 3]:
            for cell, _ in root.game.gui.sharemenu.share_starter_inventory:
                if cell.rect.collidepoint(mouse_pos):
                    root.game.gui.sharemenu.click(cell, "starter", event.button)
                    return
            if isinstance(root.game.gui.sharemenu.share_target_inventory, list):
                for cell, _ in root.game.gui.sharemenu.share_target_inventory:
                    if cell.rect.collidepoint(mouse_pos):
                        root.game.gui.sharemenu.click(cell, "target", event.button)
                        return
            elif isinstance(root.game.gui.sharemenu.share_starter_inventory, dict):
                for inventory_type in root.game.gui.sharemenu.share_target_inventory.keys(): #type: ignore
                    for cell, _ in root.game.gui.sharemenu.share_target_inventory[inventory_type]:
                        if cell.rect.collidepoint(mouse_pos):
                            root.game.gui.sharemenu.click(cell, "target", event.button)
                            return