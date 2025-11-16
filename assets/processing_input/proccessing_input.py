import pygame as py
import assets.root as root
from assets.world.cell import Cell
from assets.auxiliary_stuff import update_gui
from .handlers.building_input import BuildingInputProcessor
from .handlers.fraction_input import FractionInputProcessor
from .handlers.game_input import GameInputProcessor
from .handlers.inventory_input import InventoryInputProcessor
from .handlers.policy_input import PolicyInputProcessor
from .handlers.reciept_input import RecieptInputProcessor
from .handlers.sharemenu_input import ShareMenuInputProcessor
from .handlers.technology_input import TechnologyInputProcessor
from .handlers.writing_input import WritingInputProcessor
from .handlers.spawn_input import SpawnInputProcessor

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from assets.gamemanager import GameManager

class InputKeyProcessor:
    def __init__(self,):
        
        self.building_input = BuildingInputProcessor(self)
        self.fraction_input = FractionInputProcessor(self)
        self.game_input = GameInputProcessor(self)
        self.inventory_input = InventoryInputProcessor(self)
        self.policy_input = PolicyInputProcessor(self)
        self.reciept_input = RecieptInputProcessor(self)
        self.share_menu_input = ShareMenuInputProcessor(self)
        self.technology_input = TechnologyInputProcessor(self)
        self.writing_input = WritingInputProcessor(self)
        self.spawn = SpawnInputProcessor(self)

        self.is_ctrl_pressed = False
        self.is_shift_pressed = False
        self.is_alt_pressed = False

        self.k_a_pressed = False
        self.k_d_pressed = False
        self.k_s_pressed = False
        self.k_w_pressed = False

    def is_move_button_pressed(self):
        if any([self.k_a_pressed, self.k_d_pressed, self.k_s_pressed, self.k_w_pressed]):
            return True
    
    def move(self):
        if not root.input_field_active:
            if self.k_w_pressed:
                root.game_manager.gui.move_up()
            elif self.k_s_pressed:
                root.game_manager.gui.move_down()
            if self.k_a_pressed:
                root.game_manager.gui.move_left()
            elif self.k_d_pressed:
                root.game_manager.gui.move_right()
        else:
            self.k_a_pressed = False
            self.k_d_pressed = False
            self.k_s_pressed = False
            self.k_w_pressed = False

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
        elif event.key == py.K_w:
            self.k_w_pressed = False
        elif event.key == py.K_s:
            self.k_s_pressed = False
        elif event.key == py.K_a:
            self.k_a_pressed = False
        elif event.key == py.K_d:
            self.k_d_pressed = False

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