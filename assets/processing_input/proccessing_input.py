import pygame as py
from .. import root
from ..world.cell import Cell
from ..auxiliary_stuff import update_gui
from .basic_input_process import BasicInputProcessor
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
    from ..gamemanager import GameManager

class InputKeyProcessor:
    def __init__(self, game_manager: "GameManager"):
        self.game_manager = game_manager
        
        self.basic_input_processor = BasicInputProcessor(self, game_manager)

        self.building_input = BuildingInputProcessor(self, game_manager)
        self.fraction_input = FractionInputProcessor(self, game_manager)
        self.game_input = GameInputProcessor(self, game_manager)
        self.inventory_input = InventoryInputProcessor(self, game_manager)
        self.policy_input = PolicyInputProcessor(self, game_manager)
        self.reciept_input = RecieptInputProcessor(self, game_manager)
        self.share_menu_input = ShareMenuInputProcessor(self, game_manager)
        self.technology_input = TechnologyInputProcessor(self, game_manager)
        self.writing_input = WritingInputProcessor(self, game_manager)
        self.spawn = SpawnInputProcessor(self, game_manager)

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
                self.game_manager.gui.move_up()
            elif self.k_s_pressed:
                self.game_manager.gui.move_down()
            if self.k_a_pressed:
                self.game_manager.gui.move_left()
            elif self.k_d_pressed:
                self.game_manager.gui.move_right()
            update_gui()
            #self.game_manager.world_map.draw()
            #self.game_manager.messenger.draw()
        else:
            self.k_a_pressed = False
            self.k_d_pressed = False
            self.k_s_pressed = False
            self.k_w_pressed = False

    def pass_func(self, *args, **kwargs):
        pass

    #PROCESS_KEYDOWN----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def keydown(self, event: py.event.Event):
        if self.basic_input_processor.process_keydown_for_inputfield(event): return root.update_gui()
        if self.basic_input_processor.process_keydown_base(event): return

        self.process_keydown(event)

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
    def mousebuttondown(self, event:py.event.Event):
        mouse_pos = event.pos
        rel_mouse_pos = (mouse_pos[0]+self.game_manager.get_x_offset(), mouse_pos[1]+self.game_manager.get_y_offset())

        if self.basic_input_processor.process_mousebutton_for_inputfield(rel_mouse_pos): return root.update_gui()
        
        for button in self.game_manager.buttons.get(root.window_state, []):
            if button.rect.collidepoint(rel_mouse_pos) and button.auto_process:
                if button.click(event.button, rel_mouse_pos): return

        self.process_mousebuttondown(event, rel_mouse_pos)

    #@logger
    def process_mousebuttondown(self, event:py.event.Event, rel_mouse_pos:tuple[int, int]):
        pass #will be replaced in root.change_window_state

    #PROCESS_MOUSEUP----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #@logger
    def process_mousebuttonup(self, event:py.event.Event):
        pass #there are no functions yet

    #PROCESS_MOUSEMOTION------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #@logger
    def process_mousemotion(self, event:py.event.Event):
        pass #there are no functions yet