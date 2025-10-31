import pygame as py
import assets.root as root
from assets.world.cell import Cell
from assets.functions import update_gui
from assets.processing_input.handlers.building_input import BuildingInputProcessor
from assets.processing_input.handlers.fraction_input import FractionInputProcessor
from assets.processing_input.handlers.game_input import GameInputProcessor
from assets.processing_input.handlers.inventory_input import InventoryInputProcessor
from assets.processing_input.handlers.policy_input import PolicyInputProcessor
from assets.processing_input.handlers.reciept_input import RecieptInputProcessor
from assets.processing_input.handlers.sharemenu_input import ShareMenuInputProcessor
from assets.processing_input.handlers.technology_input import TechnologyInputProcessor
from assets.processing_input.handlers.writing_input import WritingInputProcessor

class InputKeyProcessor:
    def __init__(self):
        self.building_input = BuildingInputProcessor(self)
        self.fraction_input = FractionInputProcessor(self)
        self.game_input = GameInputProcessor(self)
        self.inventory_input = InventoryInputProcessor(self)
        self.policy_input = PolicyInputProcessor(self)
        self.reciept_input = RecieptInputProcessor(self)
        self.share_menu_input = ShareMenuInputProcessor(self)
        self.technology_input = TechnologyInputProcessor(self)
        self.writing_input = WritingInputProcessor(self)

    def pass_func(self, *args, **kwargs):
        pass

    #PROCESS_KEYDOWN----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #@logger
    def process_keydown(self, event:py.event.Event):
        pass

    #PROCESS_KEYUP------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #@logger
    def process_keyup(self, event:py.event.Event):
        if event.key == py.K_LCTRL or event.key == py.K_RCTRL:
            self.is_ctrl_pressed = False
            return
        elif event.key == py.K_LSHIFT or event.key == py.K_RSHIFT:
            self.is_shift_pressed = False
            return
        elif event.key == py.K_LALT or event.key == py.K_RALT:
            self.is_alt_pressed = False
            return
        elif root.window_state == "game":
            if event.key == py.K_w:
                self.game_input.k_w_pressed = False
            elif event.key == py.K_s:
                self.game_input.k_s_pressed = False
            elif event.key == py.K_a:
                self.game_input.k_a_pressed = False
            elif event.key == py.K_d:
                self.game_input.k_d_pressed = False

    #PROCESS_MOUSEDOWN--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #@logger
    def process_mousebuttondown(self, event:py.event.Event):
        pass #will be replaced in root.change_window_state

    #PROCESS_MOUSEUP----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #@logger
    def process_mousebuttonup(self, event:py.event.Event):
        pass #there are no functions yet

    #PROCESS_MOUSEMOTION------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #@logger
    def process_mousemotion(self, event:py.event.Event):
        pass #there are no functions yet