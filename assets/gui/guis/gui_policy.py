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
from ...auxiliary_stuff import timeit
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from managers.policy.policycard import PolicyCard
    from ...gamemanager import GameManager

class GUIGPolicy:
    def __init__(self, game_manager: "GameManager"):
        self.game_manager = game_manager

        self.policies: list[PolicyCard] = []
    
    def open(self):
        self.game_manager.policy_table.load_policies_for_player()
        self.policies = self.game_manager.fraction_manager.get_player_fraction().policies
    
    def draw(self):
        root.screen.fill((0, 0, 0))
        for policy in self.policies:
            policy.draw()
        root.need_update_gui = False

    def update_positions(self):
        x = 0
        y = 0
        for policy in self.policies:
            if root.interface_size*x+root.interface_size//2+root.interface_size > root.window_size[0]:
                x = 0
                y += 1
            policy.rect.topleft = (root.interface_size*x+root.interface_size//2, (root.interface_size*2)*y+root.interface_size//2)
            x += 1
    
    def scroll_up(self):
        for policy in self.policies:
            policy.rect.y += root.interface_size//2
        update_gui()

    def scroll_down(self):
        for policy in self.policies:
            policy.rect.y -= root.interface_size//2
        update_gui()
    
    def move_up(self):
        self.scroll_up()

    def move_down(self):
        self.scroll_down()

    def move_left(self):
        pass

    def move_right(self):
        pass