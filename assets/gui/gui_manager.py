#import pygame as py
from .buttons import *
from .infoboxs import *
from .contentbox import *
from .statistikbox import *
from .textfield import *
from .iconbox import *
from .listof import *
from .guis.gui_game import GUIGame
from .guis.gui_policy import PolicyGUIManager
from .guis.gui_technology import GUITechnology
from .guis.gui_building import GUIBuildings
from .guis.gui_writing import GUIWriting
from .guis.gui_reciept import GUIReciept
from .guis.gui_sharemenu import GUIShareMenu
from .guis.gui_fraction import GUIFraction
from .guis.gui_inventory import GUIInventory
from .guis.gui_spawn import GUISpawn
from .. import root
from ..auxiliary_stuff import timeit
from ..root import loading
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..gamemanager import GameManager

class GUI:
    def __init__(self, game_manager: "GameManager"):
        self.game_manager = game_manager
        loading.draw("Initializing GUIBuildings...")
        self.building = GUIBuildings(game_manager)
        loading.draw("Initializing GUIFraction...")
        self.fraction = GUIFraction(game_manager)
        loading.draw("Initializing GUIGame...")
        self.game = GUIGame(game_manager)
        loading.draw("Initializing GUIGPolicy...")
        self.policy = PolicyGUIManager(game_manager)
        loading.draw("Initializing GUIReciept...")
        self.reciept = GUIReciept(game_manager)
        loading.draw("Initializing GUIShareMenu...")
        self.sharemenu = GUIShareMenu(game_manager)
        loading.draw("Initializing GUITechnology...")
        self.technology = GUITechnology(game_manager)
        loading.draw("Initializing GUIWriting...")
        self.writing = GUIWriting(game_manager)
        loading.draw("Initializing GUIInventory...")
        self.inventory = GUIInventory(game_manager)
        loading.draw("Initializing GUISpawn...")
        self.spawn = GUISpawn(game_manager)

        logger.info("gui ended initialization", "GUI.initialize()")

    def change_position_for_new_screen_sizes(self):
        self.game.change_position_for_new_screen_sizes()
        self.building.change_position_for_new_screen_sizes()
        self.sharemenu.change_position_for_new_screen_sizes()
        self.inventory.change_position_for_new_screen_sizes()
        self.policy.update_positions()
        self.reciept.change_position_for_new_screen_sizes()

    def close_all_extra_windows(self):
        self.game.hide_jobs()
        self.game.hide_action_list()
        self.game.hide_info()
        self.game.hide_scheme_list()
        #self.game.main_info_window_content_close()
    
    def pass_func(self):
        pass

    def show_info_under_mouse(self):
        pass

    def draw(self):
        pass #will be set in root.py

    def move_up(self):
        pass

    def move_down(self):
        pass

    def move_left(self):
        pass

    def move_right(self):
        pass