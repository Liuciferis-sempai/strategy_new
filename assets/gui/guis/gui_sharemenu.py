from ..buttons import *
from ..infoboxs import *
from ..contentbox import *
from ..statistikbox import *
from ..textfield import *
from ..iconbox import *
from ..listof import *
import assets.root as root
from assets.root import logger
import pygame as py
from assets.decorators import timeit

class GUIShareMenu:
    def __init__(self):
        self.share_starter = None
        self.share_target = None
        self.share_starter_inventory = []
        self.share_target_inventory = []
        self.share_starter_inventory_org = []
        self.share_target_inventory_names = []
        self.share_starter_ico = None
        self.share_target_ico = None
        self.share_target_type = "pawn"
    
    def change_position_for_new_screen_sizes(self):
        if root.window_size[0] >= 1900 and root.window_size[1] >= 1000:
            self.cell_size = root.interface_size//2
        else:
            self.cell_size = root.interface_size//4
    
    def set_inventories(self):
        if self.share_target and self.share_starter:
            if hasattr(self.share_target, "is_scheme"):
                if self.share_target.is_scheme: #type: ignore
                    logger.info("share target is scheme", "GUIShereMenu.set_inventories()", f"{self.share_target.is_scheme}") #type: ignore
                    self.share_starter_inventory_org = self.share_target.scheme_inventory #type: ignore
                    self._set_inventories(self.share_target.scheme_inventory, self.share_target.scheme_inventory_size) #type: ignore
                    return
            self.share_starter_inventory_org = self.share_target.inventory #type: ignore
            self._set_inventories(self.share_target.inventory, self.share_target.inventory_size) #type: ignore

    def _set_inventories(self, target_inventory: list|dict, max_target_inventory: int|dict):
        if self.share_target and self.share_starter:
            self.share_starter_inventory = []
            for i in range(self.share_starter.data.get("inventory_size", 1)):
                if i < len(self.share_starter.inventory):
                    self.share_starter_inventory.append([Icon(self.cell_size, self.cell_size, img=self.share_starter.inventory[i].name), TextField(text=str(self.share_starter.inventory[i].amout), font_size=50, width=0, height=0)]) #type: ignore
                else:
                    self.share_starter_inventory.append([Icon(self.cell_size, self.cell_size, img="empty_inventory_cell.png"), TextField(text="", font_size=50, width=0, height=0)]) #type: ignore

            if isinstance(target_inventory, list):
                self.share_target_inventory = []
                for i in range(max_target_inventory): #type: ignore
                    if i < len(target_inventory):
                        self.share_target_inventory.append([Icon(self.cell_size, self.cell_size, img=target_inventory[i].name), TextField(text=str(target_inventory[i].amout), font_size=50, width=0, height=0)]) #type: ignore
                    else:
                        self.share_target_inventory.append([Icon(self.cell_size, self.cell_size, img="empty_inventory_cell.png"), TextField(text="", font_size=50, width=0, height=0)]) #type: ignore
            else:
                self.share_target_inventory = {}
                self.share_target_inventory_names = []
                for inventory_type in target_inventory.keys(): #type: ignore
                    self.share_target_inventory_names.append(TextField(text=inventory_type, font_size=50, width=0, height=0))
                    self.share_target_inventory[inventory_type] = []
                    for i in range(max_target_inventory[inventory_type]): #type: ignore
                        if i < len(target_inventory[inventory_type]):
                            self.share_target_inventory[inventory_type].append([Icon(self.cell_size, self.cell_size, img=target_inventory[inventory_type][i].name), TextField(text=str(target_inventory[inventory_type][i].amout), font_size=50, width=0, height=0)]) #type: ignore
                        else:
                            self.share_target_inventory[inventory_type].append([Icon(self.cell_size, self.cell_size, img="empty_inventory_cell.png"), TextField(text="", font_size=50, width=0, height=0)]) #type: ignore
            
            self.share_starter_ico = Icon(root.window_size[0]//8, int(root.window_size[1]*0.7), img=self.share_starter.data.get("ico", "none.png"), spec_path="data/pawns/ico")
            if self.share_target_type == "pawn":
                self.share_target_ico = Icon(root.window_size[0]//8, int(root.window_size[1]*0.7), img=self.share_target.data.get("ico", "none.png"), spec_path="data/pawns/ico")
            elif self.share_target_type == "building":
                self.share_target_ico = Icon(root.window_size[0]//8, int(root.window_size[1]//2), img=self.share_target.data.get("img", "none.png"), spec_path="data/buildings/img")
        else:
            logger.error("Share starter or target not found", f"GUIShareMenu._set_inventories({target_inventory}, {max_target_inventory})")
    
    def open(self, target:str):
        self.share_starter = root.handler.pawns_manager.get_pawn_by_id(root.handler.get_opened_pawn().id)
        self.share_target = root.handler.pawns_manager.get_pawn_by_name(target, root.handler.gui.game.get_target_coord())

        if self.share_target.is_default:
            self.share_target = root.handler.buildings_manager.get_building_by_coord(root.handler.gui.game.get_target_coord())
            self.share_target_type = "building"
        else:
            self.share_target_type = "pawn"
        
        self.change_position_for_new_screen_sizes()
        self.set_inventories()
    
    def click(self, cell: Icon, inventory_type: str, button: int):
        if inventory_type == "starter":
            for inv_cell, amout in self.share_starter_inventory:
                if inv_cell == cell:
                    if cell.img != "empty_inventory_cell.png": #type: ignore
                        if self.share_target.has_free_space(): #type: ignore
                            self.share_target.add_resource(cell.img, int(int(amout.text)//2) if button == 3 else int(amout.text)) #type: ignore
                            self.share_starter.remove_resource(cell.img, int(int(amout.text)//2) if button == 3 else int(amout.text)) #type: ignore
                            self.set_inventories()
                            update_gui()
                            return
        elif inventory_type == "target":
            if isinstance(self.share_target_inventory, list):
                for inv_cell, amout in self.share_target_inventory:
                    if inv_cell == cell:
                        if cell.img != "empty_inventory_cell.png": #type: ignore
                            if self.share_starter.has_free_space(): #type: ignore
                                self.share_starter.add_resource(cell.img, int(int(amout.text)//2) if button == 3 else int(amout.text)) #type: ignore
                                self.share_target.remove_resource(cell.img, int(int(amout.text)//2) if button == 3 else int(amout.text)) #type: ignore
                                self.set_inventories()
                                update_gui()
                                return
            elif isinstance(self.share_target_inventory, dict):
                for inventory_type in self.share_target.inventory.keys(): #type: ignore
                    for inv_cell, amout in self.share_target_inventory[inventory_type]: #type: ignore
                        if inv_cell == cell:
                            if cell.img != "empty_inventory_cell.png": #type: ignore
                                if self.share_starter.has_free_space(): #type: ignore
                                    self.share_starter.add_resource(cell.img, int(int(amout.text)//2) if button == 3 else int(amout.text)) #type: ignore
                                    self.share_target.remove_resource(cell.img, int(int(amout.text)//2) if button == 3 else int(amout.text), inventory_type) #type: ignore
                                    self.set_inventories()
                                    update_gui()
                                    return
        else:
            logger.error(f"Unknown inventory type '{inventory_type}' in GUIShareMenu click method", f"GUIShareMenu.click({cell}, {inventory_type}, {button})")
            #print("unknown inventory type")
    
    #@timeit
    def draw(self):
        root.screen.fill((100, 100, 100))
        py.draw.line(root.screen, (255, 255, 255), (root.window_size[0]//2, 0), (root.window_size[0]//2, root.window_size[1]), 2)

        self.share_starter_ico.change_position((root.cell_sizes[root.cell_size_scale][0]//4, root.window_size[1]//2 - self.share_starter_ico.height//2)) #type: ignore
        self.share_starter_ico.draw() #type: ignore

        self.share_target_ico.change_position((root.window_size[0]-root.cell_sizes[root.cell_size_scale][0]//4-self.share_target_ico.width, root.window_size[1]//2 - self.share_target_ico.height//2)) #type: ignore
        self.share_target_ico.draw() #type: ignore

        y_offset = 0
        x_offset = 0
        for cell, amout in self.share_starter_inventory:
            if root.cell_sizes[root.cell_size_scale][0]//4+self.share_starter_ico.width+root.cell_sizes[root.cell_size_scale][0]//4 + (cell.width+10)*(x_offset+1) > root.window_size[0]//2+root.cell_sizes[root.cell_size_scale][0]//4: #type:ignore
                y_offset += 1
                x_offset = 0

            cell.change_position((root.cell_sizes[root.cell_size_scale][0]//2+self.share_starter_ico.width + (cell.width+10)*x_offset, root.window_size[1]//2 - self.share_starter_ico.height//2 + (cell.height+10)*y_offset)) #type: ignore
            amout.change_position((root.cell_sizes[root.cell_size_scale][0]//2+self.share_starter_ico.width + (cell.width+10)*x_offset + (cell.width - amout.text_rect.width - 5), root.window_size[1]//2 - self.share_starter_ico.height//2 + (cell.height+10)*y_offset + amout.text_rect.height//2)) #type: ignore
            x_offset += 1

        y_offset = 0
        x_offset = 0
        if isinstance(self.share_target_inventory, list):
            for cell, amout in self.share_target_inventory:
                if root.window_size[0] - root.cell_sizes[root.cell_size_scale][0]//2 - self.share_target_ico.width - cell.width - (cell.width+10)*x_offset < root.window_size[0]//2-root.cell_sizes[root.cell_size_scale][0]//4: #type:ignore
                    y_offset += 1
                    x_offset = 0

                cell.change_position((root.window_size[0] - root.cell_sizes[root.cell_size_scale][0]//2 - self.share_target_ico.width - cell.width - (cell.width+10)*x_offset, root.window_size[1]//2 - self.share_target_ico.height//2 + (cell.height+10)*y_offset)) #type: ignore
                amout.change_position((root.window_size[0] - root.cell_sizes[root.cell_size_scale][0]//2 - self.share_target_ico.width - cell.width - (cell.width+10)*x_offset + (cell.width - amout.text_rect.width - 5), root.window_size[1]//2 - self.share_target_ico.height//2 + (cell.height+10)*y_offset + amout.text_rect.height//2)) #type: ignore
                x_offset += 1
        elif isinstance(self.share_target_inventory, dict):
            for i, inventory_type in enumerate(self.share_starter_inventory_org.keys()): #type: ignore
                self.share_target_inventory_names[i].change_position((root.window_size[0]//2+10, root.window_size[1]//2 - self.share_target_ico.height//2 + (cell.height+10)*y_offset)) #type:ignore
                y_offset += 1
                for cell, amout in self.share_target_inventory[inventory_type]:
                    if root.window_size[0] - root.cell_sizes[root.cell_size_scale][0]//2 - self.share_target_ico.width - cell.width - (cell.width+10)*x_offset < root.window_size[0]//2-root.cell_sizes[root.cell_size_scale][0]//4: #type:ignore
                        y_offset += 1
                        x_offset = 0

                    cell.change_position((root.window_size[0] - root.cell_sizes[root.cell_size_scale][0]//2 - self.share_target_ico.width - cell.width - (cell.width+10)*x_offset, root.window_size[1]//2 - self.share_target_ico.height//2 + (cell.height+10)*y_offset)) #type: ignore
                    amout.change_position((root.window_size[0] - root.cell_sizes[root.cell_size_scale][0]//2 - self.share_target_ico.width - cell.width - (cell.width+10)*x_offset + (cell.width - amout.text_rect.width - 5), root.window_size[1]//2 - self.share_target_ico.height//2 + (cell.height+10)*y_offset + amout.text_rect.height//2)) #type: ignore
                    x_offset += 1
                y_offset += 1
                x_offset = 0
    
        root.need_update_gui = False