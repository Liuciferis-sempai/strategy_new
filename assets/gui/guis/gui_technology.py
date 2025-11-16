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

class GUITechnology:
    def __init__(self):
        pass
    
    def open(self):
        pass

    def draw(self):
        root.screen.fill((0, 0, 0))
        root.game_manager.tech_tree.draw()
        root.need_update_gui = False
    
    def move_up(self):
        root.game_manager.tech_tree.scroll_up()

    def move_down(self):
        root.game_manager.tech_tree.scroll_down()

    def move_left(self):
        root.game_manager.tech_tree.scroll_left()

    def move_right(self):
        root.game_manager.tech_tree.scroll_right()