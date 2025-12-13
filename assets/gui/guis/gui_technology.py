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
from ...managers.technologies.techtree import Techtree

class GUITechnology:
    def __init__(self, game_manager: "GameManager"):
        self.game_manager = game_manager
        self.techtree: Techtree = Techtree([], -1)
    
    def open(self):
        self.techtree = root.game_manager.fraction_manager.get_player_fraction().techs

    def draw(self):
        root.screen.fill((0, 0, 0))
        self.techtree.draw()
        root.need_update_gui = False
    
    def move_up(self):
        self.techtree.scroll_up()
    
    def move_down(self):
        self.techtree.scroll_down()
    
    def move_left(self):
        self.techtree.scroll_left()
    
    def move_right(self):
        self.techtree.scroll_right()