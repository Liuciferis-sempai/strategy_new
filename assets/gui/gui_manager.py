#import pygame as py
from .buttons import *
from .infoboxs import *
from .contentbox import *
from .statistikbox import *
from .textfield import *
from .iconbox import *
from .listof import *
from .guis.gui_game import GUIGame
from .guis.gui_policy import GUIGPolicy
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

class GUI:
    def initialize(self):
        loading.draw("Initializing GUIBuildings...")
        self.building = GUIBuildings()
        loading.draw("Initializing GUIFraction...")
        self.fraction = GUIFraction()
        loading.draw("Initializing GUIGame...")
        self.game = GUIGame()
        loading.draw("Initializing GUIGPolicy...")
        self.policy = GUIGPolicy()
        loading.draw("Initializing GUIReciept...")
        self.reciept = GUIReciept()
        loading.draw("Initializing GUIShareMenu...")
        self.sharemenu = GUIShareMenu()
        loading.draw("Initializing GUITechnology...")
        self.technology = GUITechnology()
        loading.draw("Initializing GUIWriting...")
        self.writing = GUIWriting()
        loading.draw("Initializing GUIInventory...")
        self.inventory = GUIInventory()
        loading.draw("Initializing GUISpawn...")
        self.spawn = GUISpawn()

    def change_position_for_new_screen_sizes(self):
        self.game.change_position_for_new_screen_sizes()
        self.building.change_position_for_new_screen_sizes()
        self.sharemenu.change_position_for_new_screen_sizes()
        self.inventory.change_position_for_new_screen_sizes()
        self.policy.update_positions()

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