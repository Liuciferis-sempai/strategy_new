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
from ...auxiliary_stuff import *
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ...gamemanager import GameManager

from ...managers.pawns.pawn import Pawn
from ...managers.buildings.building import Building
from ...managers.resources.resource_type import ResourceType

class GUIInventory:
    def __init__(self, game_manager: "GameManager"):
        self.game_manager = game_manager

        self.owner: Pawn|Building|None = None
        self.owner_ico: Icon = Icon(root.window_size[0]//8, int(root.window_size[1]*0.7), img="none.png")
        self.owner_inventory: Inventory|None = None
        self.inventory_cells: dict[str, list[tuple[Icon, TextField]]] = {}
        self.inventory_names: list[TextField] = []
        self.owner_type: str = "none"

        self.cell_size = int(root.interface_size//3)

    def open(self):
        if not self.game_manager.is_chosen_pawn_default():
            self.owner = self.game_manager.get_chosen_pawn()
            self.owner_type = "pawn"
        elif not self.game_manager.is_chosen_building_defult():
            self.owner = self.game_manager.get_chosen_building()
            self.owner_type = "building"
        else:
            logger.error("can not open pawn or building", "GUIInventory.open()")
            back_window_state()
            return
    
        if hasattr(self.owner, "is_scheme"):
            if self.owner.is_scheme: #type: ignore
                self.owner_inventory = self.owner.scheme_inventory #type: ignore
                self.set_inventory()
                self.change_position_for_new_screen_sizes()
                return
        
        self.owner_inventory = self.owner.inventory
        self.set_inventory()
        self.change_position_for_new_screen_sizes()
    
    def set_inventory(self):
        if not self.owner_inventory or not self.owner: return
        inventory = self.owner_inventory.content_to_dict()
        max_size = self.owner_inventory.size_to_dict()
        self.inventory_cells = {}
        for category in inventory:
            self.inventory_names.append(
                TextField(text=category, font_size=50)
            )
            self.inventory_cells[category] = []
            for i in range(max_size[category]):
                if i < len(inventory[category]):
                    cell = (
                        Icon(width=self.cell_size, height=self.cell_size, img=inventory[category][i].name),
                        TextField(text=str(inventory[category][i].amount), font_size=50)
                    )
                else:
                    cell = (
                        Icon(width=self.cell_size, height=self.cell_size, img="empty_inventory_cell.png"),
                        TextField(text="", font_size=50)
                    )
                self.inventory_cells[category].append(cell)

        if self.owner_type == "pawn":
            self.owner_ico.update_image(new_img=self.owner.data.get("ico", "none.png"), spec_path="data/pawns/ico")
        elif self.owner_type == "building":
            self.owner_ico.update_image(new_img=self.owner.data.get("img", "none.png"), spec_path="data/buildings/img")
    
    def change_position_for_new_screen_sizes(self):
        if not self.owner_inventory: return
        ico_x, ico_y = self.cell_size//4, root.window_size[1]//2 - self.owner_ico.height//2

        self.owner_ico.change_position((ico_x, ico_y))
        y_offset = 0
        x_offset = 0

        inventory = self.owner_inventory.content_to_dict()

        for i, category in enumerate(inventory.keys()):
            self.inventory_names[i].change_position((ico_x + self.owner_ico.width + 10, ico_y + (self.cell_size + 10)*y_offset))
            y_offset += 1
            for cell, amount in self.inventory_cells[category]:
                x_pos = ico_x + self.owner_ico.width + 10 + (cell.width+10)*x_offset
                if x_pos + cell.width > root.window_size[0]-self.cell_size//4:
                    y_offset += 1
                    x_offset = 0
                    x_pos = ico_x + self.owner_ico.width + 10 + (cell.width+10)*x_offset
                y_pos = ico_y + (cell.height+10)*y_offset

                cell.change_position((x_pos, y_pos)) 
                amount.change_position((x_pos + (cell.width - amount.text_rect.width - 5), y_pos + amount.text_rect.height//2))
                x_offset += 1
            y_offset += 1
            x_offset = 0
    
    def click(self, *args, **kwargs):
        pass

    def draw(self):
        if not self.owner_inventory or not self.owner: return
        root.screen.fill((100, 100, 100))

        self.owner_ico.draw()
        for i, cat in enumerate(self.inventory_cells):
            self.inventory_names[i].draw()
            for cell, amount in self.inventory_cells[cat]:
                cell.draw()
                amount.draw()

        root.need_update_gui = False
    
    def move_up(self):
        self.game_manager.add_y_offset(1)
        self.change_position_for_new_screen_sizes()

    def move_down(self):
        self.game_manager.add_y_offset(-1)
        self.change_position_for_new_screen_sizes()

    def move_left(self):
        pass

    def move_right(self):
        pass