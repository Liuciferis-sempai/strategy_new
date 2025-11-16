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

class GUIFraction:
    def __init__(self):
        self.fraction_name_edit_button = FractionNameEditButton()
    
    def open_player_fraction(self):
        self.player_fraction = root.game_manager.fraction_manager.get_player_fraction()
        if not self.player_fraction:
            logger.error("Cannot find player fraction", "GUIFraction.open_player_fraction()")
            return
        self.fraction_name = py.font.Font(None, 30).render(self.player_fraction.name, False, (255, 255, 255))                   #Textfield?
        self.fraction_symbol = py.font.Font(None, 30).render(self.player_fraction.symbol, False, self.player_fraction.color)    #Textfield?
        self.fraction_name_edit_button.change_position((self.fraction_name.get_width() + self.fraction_symbol.get_width() + 20, 5))
        self.statistics_box = Statistikbox(data=self.player_fraction.statistics)
        self.research_field = TextField(root.interface_size*2, 60, position=(10, int(root.interface_size*2.5)), text=self.player_fraction.research_technology)

    def draw(self):
        root.screen.fill((0, 0, 0))

        root.screen.blit(self.fraction_name, (5, 25- self.fraction_symbol.get_height()//2))
        root.screen.blit(self.fraction_symbol, (5 + self.fraction_name.get_width() + 5, 25 - self.fraction_symbol.get_height()//2))
        root.screen.blit(self.fraction_name_edit_button.image, self.fraction_name_edit_button.rect)
        self.statistics_box.draw()

        self.research_field.draw()

        root.need_update_gui = False
    
    def move_up(self):
        pass

    def move_down(self):
        pass

    def move_left(self):
        pass

    def move_right(self):
        pass