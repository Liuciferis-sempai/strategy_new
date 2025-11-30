import pygame as py
from ...buttons import *
from ...infoboxs import *
from ...contentbox import *
from ...statistikbox import *
from ...textfield import *
from ...iconbox import *
from ...listof import *
from ...inputfield import *
from .... import root
from ....root import logger
from ....auxiliary_stuff import timeit, get_cell_side_size
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from managers.policy.policycard import PolicyCard
    from ....gamemanager import GameManager

class GUIGPolicyStack:
    def __init__(self, game_manager: "GameManager"):
        self.game_manager = game_manager

        self.policies: list[PolicyCard] = []
        self.move_distace = get_cell_side_size()//4

    def open(self, policy):
        self.policies = self.game_manager.fraction_manager.get_player_fraction().policies

    def draw(self):
        root.screen.fill((0, 0, 0))
        for policy in self.policies:
            policy.draw()
        root.need_update_gui = False

    def update_positions(self):
        card_size = root.game_manager.policy_table.card_size
        x = 0
        y = 0
        for policy in self.policies:
            if card_size*x+card_size//2+card_size > root.window_size[0]:
                x = 0
                y += 1
            policy.change_position((card_size*x+card_size//2, card_size*2*y))
            x += 1
        if y == 0:
            for x, policy in enumerate(self.policies):
                policy.change_position((card_size*x+card_size//2, root.window_size[1]//2-card_size))
    
    def click(self, mouse_pos: tuple[int, int]):
        pass # @TODO write click scripte

    def move_up(self):
        if self.y_offset + self.move_distace*0.8 < 0:
            self.y_offset += self.move_distace
            for policy in self.policies:
                policy.rect.y += self.move_distace
            update_gui()

    def move_down(self):
        if self.policies[-1].rect.top > 0:
            self.y_offset -= self.move_distace
            for policy in self.policies:
                policy.rect.y -= self.move_distace
            update_gui()

    def move_left(self):
        pass

    def move_right(self):
        pass