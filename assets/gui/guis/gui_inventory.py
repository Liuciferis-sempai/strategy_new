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

class GUIInventory:
    def __init__(self):
        self.owner = None
        self.owner_inventory = []
        self.owner_inventory_names = []
        self.owner_inventory_org = []
        self.owner_ico = None
        self.owner_type = "pawn"
    
    def change_position_for_new_screen_sizes(self):
        if root.window_size[0] >= 1900 and root.window_size[1] >= 1000:
            self.cell_size = root.interface_size//2
        else:
            self.cell_size = root.interface_size//4

    def set_inventory(self):
        if self.owner:
            if hasattr(self.owner, "is_scheme"):
                if self.owner.is_scheme: #type: ignore
                    self.owner_inventory_org = self.owner.scheme_inventory #type: ignore
                    self._set_inventory(self.owner.scheme_inventory, self.owner.scheme_inventory_size) #type: ignore
                    return
                self.owner_inventory_org = self.owner.inventory
            self._set_inventory(self.owner.inventory, self.owner.inventory_size)
        else:
            logger.error("No owner found", "GUIInventory.set_inventory()")
    
    def _set_inventory(self, inventory: list|dict, max_inventory: int|dict):
        if isinstance(inventory, list):
            self.owner_inventory = []
            for i in range(max_inventory): #type: ignore
                if i < len(inventory):
                    self.owner_inventory.append([Icon(self.cell_size, self.cell_size, img=inventory[i].name), TextField(text=str(inventory[i].amout), font_size=50, width=0, height=0)]) #type: ignore
                else:
                    self.owner_inventory.append([Icon(self.cell_size, self.cell_size, img="empty_inventory_cell.png"), TextField(text="", font_size=50, width=0, height=0)]) #type: ignore
        else:
            self.owner_inventory = {}
            self.owner_inventory_names = []
            for inventory_type in inventory.keys(): #type: ignore
                self.owner_inventory_names.append(TextField(text=inventory_type, font_size=50, width=0, height=0))
                self.owner_inventory[inventory_type] = []
                for i in range(max_inventory[inventory_type]): #type: ignore
                    if i < len(inventory[inventory_type]):
                        self.owner_inventory[inventory_type].append([Icon(self.cell_size, self.cell_size, img=inventory[inventory_type][i].name), TextField(text=str(inventory[inventory_type][i].amout), font_size=50, width=0, height=0)]) #type: ignore
                    else:
                        self.owner_inventory[inventory_type].append([Icon(self.cell_size, self.cell_size, img="empty_inventory_cell.png"), TextField(text="", font_size=50, width=0, height=0)]) #type: ignore

        if self.owner_type == "pawn":
            self.owner_ico = Icon(root.window_size[0]//8, int(root.window_size[1]*0.7), img=self.owner.data.get("ico", "none.png"), spec_path="data/pawns/ico") #type: ignore
        elif self.owner_type == "building":
            self.owner_ico = Icon(root.window_size[0]//8, int(root.window_size[1]//2), img=self.owner.data.get("img", "none.png"), spec_path="data/buildings/img")#type: ignore 
    
    def open(self):
        if not root.game_manager.is_opened_pawn_default():
            self.owner = root.game_manager.pawns_manager.get_pawn_by_id(root.game_manager.get_opened_pawn().id)
            self.owner_type = "pawn"
        elif not root.game_manager.is_chosen_cell_default():
            self.owner = root.game_manager.buildings_manager.get_building_by_coord(root.game_manager.get_chosen_cell_coord())
            self.owner_type = "building"
        
        self.change_position_for_new_screen_sizes()
        self.set_inventory()
    
    def click(self, *args, **kwargs):
        pass
    
    #@timeit
    def draw(self):
        root.screen.fill((100, 100, 100))

        if self.owner_ico and self.owner:
            ico_x, ico_y = self.cell_size//4, root.window_size[1]//2 - self.owner_ico.height//2

            self.owner_ico.change_position((ico_x, ico_y))
            self.owner_ico.draw()

            y_offset = 0
            x_offset = 0
            if isinstance(self.owner_inventory, list):
                for cell, amout in self.owner_inventory:
                    x_pos = ico_x + self.owner_ico.width + 10 + (cell.width+10)*x_offset
                    if  x_pos + cell.width > root.window_size[0]-self.cell_size//4:
                        y_offset += 1
                        x_offset = 0
                        x_pos = ico_x + self.owner_ico.width + 10 + (cell.width+10)*x_offset
                    y_pos = ico_y + (cell.height+10)*y_offset

                    cell.change_position((x_pos, y_pos))
                    amout.change_position((x_pos + (cell.width - amout.text_rect.width - 5), y_pos + amout.text_rect.height//2))
                    x_offset += 1

            elif isinstance(self.owner_inventory, dict):
                for i, inventory_type in enumerate(self.owner_inventory_org.keys()): #type: ignore
                    self.owner_inventory_names[i].change_position((ico_x + self.owner_ico.width + 10, ico_y + (self.cell_size + 10)*y_offset))
                    y_offset += 1
                    for cell, amout in self.owner_inventory[inventory_type]:
                        x_pos = ico_x + self.owner_ico.width + 10 + (cell.width+10)*x_offset
                        if x_pos + cell.width > root.window_size[0]-self.cell_size//4:
                            y_offset += 1
                            x_offset = 0
                            x_pos = ico_x + self.owner_ico.width + 10 + (cell.width+10)*x_offset
                        y_pos = ico_y + (cell.height+10)*y_offset

                        cell.change_position((x_pos, y_pos)) 
                        amout.change_position((x_pos + (cell.width - amout.text_rect.width - 5), y_pos + amout.text_rect.height//2))
                        x_offset += 1
                    y_offset += 1
                    x_offset = 0
        else:
            logger.error(f"self.owner or self.owner_ico is not difinded. self.owner_ico: {self.owner_ico}; self.owner: {self.owner}", "GUIInventory.draw()")
        root.need_update_gui = False
    
    def move_up(self):
        pass

    def move_down(self):
        pass

    def move_left(self):
        pass

    def move_right(self):
        pass