import pygame as py
from ..buttons import *
from ..infoboxs import *
from ..contentbox import *
from ..statistikbox import *
from ..textfield import *
from ..iconbox import *
from ..listof import *
from ..inputfield import *
from ... import root
from ...root import logger
from ...auxiliary_stuff import timeit, get_cell_side_size
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from managers.policy.policycard import PolicyCard
    from ...gamemanager import GameManager

class GUIGPolicy:
    def __init__(self, game_manager: "GameManager"):
        self.game_manager = game_manager
        self.y_offset = 0

        self.policies: list[PolicyCard] = []
        self.move_distace = get_cell_side_size()//4
    
    def open(self):
        self.game_manager.policy_table.update_positions()
        self.policies = self.game_manager.fraction_manager.get_player_fraction().policies
    
    def draw(self):
        root.screen.fill((0, 0, 0))
        for policy in self.policies:
            policy.draw()
        root.need_update_gui = False

    def update_positions(self):
        self.game_manager.policy_table.update_positions()

    def check_click(self, mouse_pos: tuple[int, int]):
        for policy in self.policies:
            if policy.rect.collidepoint(mouse_pos):
                logger.info(f"clicked policy {policy.name}", "GUIGPolicy.check_click()")
                print(policy.get_info(), policy) # @TODO make a display of information
                return
    
    def scroll_up(self):
        if self.y_offset + self.move_distace < 0:
            self.y_offset += self.move_distace
            for policy in self.policies:
                policy.rect.y += self.move_distace
            update_gui()

    def scroll_down(self):
        if self.policies[-1].rect.top > 0:
            self.y_offset -= self.move_distace
            for policy in self.policies:
                policy.rect.y -= self.move_distace
            update_gui()
    
    def move_up(self):
        self.scroll_up()

    def move_down(self):
        self.scroll_down()

    def move_left(self):
        pass

    def move_right(self):
        pass