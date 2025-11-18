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
    from ...gamemanager import GameManager

class GUITechnology:
    def __init__(self, game_manager: "GameManager"):
        self.game_manager = game_manager
    
    def open(self):
        pass

    def draw(self):
        root.screen.fill((0, 0, 0))
        self.game_manager.tech_tree.draw()
        root.need_update_gui = False
    
    def move_up(self):
        self.game_manager.tech_tree.scroll_up()

    def move_down(self):
        self.game_manager.tech_tree.scroll_down()

    def move_left(self):
        self.game_manager.tech_tree.scroll_left()

    def move_right(self):
        self.game_manager.tech_tree.scroll_right()