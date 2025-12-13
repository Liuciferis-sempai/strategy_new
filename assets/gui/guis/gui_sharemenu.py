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

class GUIShareMenu:
    def __init__(self, game_manager: "GameManager"):
        self.game_manager = game_manager

        self.starter: Pawn|Building|None = None
        self.starter_ico: Icon = Icon(root.window_size[0]//8, int(root.window_size[1]*0.7), img="none.png")
        self.starter_inventory: Inventory|None = None
        self.starter_inventory_cells: dict[str, list[tuple[InventoryCellButton, TextField]]] = {}
        self.starter_inventory_names: list[TextField] = []
        self.starter_type: str = "none"

        self.target: Pawn|Building|None = None
        self.target_ico: Icon = Icon(root.window_size[0]//8, int(root.window_size[1]*0.7), img="none.png")
        self.target_inventory: Inventory|None = None
        self.target_inventory_cells: dict[str, list[tuple[InventoryCellButton, TextField]]] = {}
        self.target_inventory_names: list[TextField] = []
        self.target_type: str = "none"

        self.cell_size = int(root.interface_size//3)

    def open(self, target: str):
        if not self.game_manager.is_chosen_pawn_default():
            self.starter = self.game_manager.get_chosen_pawn()
            self.starter_type = "pawn"
        elif not self.game_manager.is_chosen_building_default():
            self.starter = self.game_manager.get_chosen_building()
            self.starter_type = "building"
        else:
            logger.error("unknow share starter", f"GUIShareMenu.open({target})")
            return
        self.starter_inventory = self.starter.inventory
        
        self.target = self.game_manager.get_pawn(pawn_type=target, coord=self.game_manager.get_target_coord())
        self.target_type = "pawn"
        if not self.target:
            self.target = self.game_manager.get_building(coord=self.game_manager.get_target_coord())
            self.target_type = "building"
            if not self.target:
                logger.error("unknow share target", f"GUIShareMenu.open({target})")
                return
        if isinstance(self.target, Building) and self.target.is_scheme:
            self.target_inventory = self.target.scheme_inventory
        else:
            self.target_inventory = self.target.inventory
        
        self.set_inventories()
        self.change_position_for_new_screen_sizes()
    
    def set_inventories(self):
        if not self.starter or not self.target or not self.starter_inventory or not self.target_inventory: return

        self.starter_inventory_cells = {}
        self.starter_inventory_names = []
        self.target_inventory_cells = {}
        self.target_inventory_names = []

        starter_inventory = self.starter_inventory.content_to_dict()
        starter_inventory_size = self.starter_inventory.size_to_dict()
        target_inventory = self.target_inventory.content_to_dict()
        target_inventory_size = self.target_inventory.size_to_dict()

        for category in starter_inventory:
            self.starter_inventory_names.append(
                TextField(text=category, font_size=50)
            )
            self.starter_inventory_cells[category] = []
            for i in range(starter_inventory_size[category]):
                if i < len(starter_inventory[category]):
                    cell = (
                        InventoryCellButton(width=self.cell_size, height=self.cell_size, img=starter_inventory[category][i].name, resource_name=starter_inventory[category][i].name, resource_amount=starter_inventory[category][i].amount),
                        TextField(text=str(starter_inventory[category][i].amount), font_size=50)
                    )
                else:
                    cell = (
                        InventoryCellButton(width=self.cell_size, height=self.cell_size, img="empty_inventory_cell.png", resource_name="none", resource_amount=0),
                        TextField(text="", font_size=50)
                    )
                self.starter_inventory_cells[category].append(cell)
        if self.starter_type == "pawn":
            self.starter_ico.update_image(new_img=self.starter.data.get("ico", "none.png"), spec_path="data/pawns/ico")
        elif self.starter_type == "building":
            self.starter_ico.update_image(new_img=self.starter.data.get("img", "none.png"), spec_path="data/buildings/img")
        
        for category in target_inventory:
            self.target_inventory_names.append(
                TextField(text=category, font_size=50)
            )
            self.target_inventory_cells[category] = []
            for i in range(target_inventory_size[category]):
                if i < len(target_inventory[category]):
                    cell = (
                        InventoryCellButton(width=self.cell_size, height=self.cell_size, img=target_inventory[category][i].name, resource_name=target_inventory[category][i].name, resource_amount=target_inventory[category][i].amount),
                        TextField(text=str(target_inventory[category][i].amount), font_size=50)
                    )
                else:
                    cell = (
                        InventoryCellButton(width=self.cell_size, height=self.cell_size, img="empty_inventory_cell.png", resource_name="none", resource_amount=0),
                        TextField(text="", font_size=50)
                    )
                self.target_inventory_cells[category].append(cell)
        if self.target_type == "pawn":
            self.target_ico.update_image(new_img=self.target.data.get("ico", "none.png"), spec_path="data/pawns/ico")
        elif self.target_type == "building":
            self.target_ico.update_image(new_img=self.target.data.get("img", "none.png"), spec_path="data/buildings/img")
    
    def change_position_for_new_screen_sizes(self):
        if not self.starter_inventory or not self.target_inventory: return

        margin = self.cell_size//4
        starter_inventory_margin = self.starter_ico.width+margin*2
        target_inventory_margin = self.target_ico.width+margin*2

        self.starter_ico.change_position((margin, root.window_size[1]//2 - self.starter_ico.height//2))
        self.target_ico.change_position((root.window_size[0]-margin-self.target_ico.width, root.window_size[1]//2 - self.target_ico.height//2))

        y_offset = self.game_manager.get_y_offset()
        x_offset = self.game_manager.get_x_offset()
        for i, category in enumerate(self.starter_inventory_cells):
            self.starter_inventory_names[i].change_position((starter_inventory_margin, root.window_size[1]//2 - self.starter_ico.height//2 + (self.cell_size+10)*y_offset))
            y_offset += 1
            for cell, amount in self.starter_inventory_cells[category]:
                if starter_inventory_margin + (self.cell_size+10)*(x_offset+1) > root.window_size[0]//2+margin:
                    y_offset += 1
                    x_offset = 0

                cell.change_position(
                    (starter_inventory_margin + (self.cell_size+10)*x_offset,
                    root.window_size[1]//2 - self.starter_ico.height//2 + (self.cell_size+10)*y_offset)
                    )
                amount.change_position(
                    (starter_inventory_margin + (self.cell_size+10)*x_offset + (self.cell_size - amount.text_rect.width - 5),
                    root.window_size[1]//2 - self.starter_ico.height//2 + (self.cell_size+10)*y_offset + amount.text_rect.height//2))
                x_offset += 1

        y_offset = self.game_manager.get_y_offset()
        x_offset = self.game_manager.get_x_offset()
        for i, category in enumerate(self.target_inventory_cells):
            self.target_inventory_names[i].change_position(
                        (root.window_size[0] - target_inventory_margin - self.cell_size+10 - self.cell_size,
                        root.window_size[1]//2 - self.starter_ico.height//2 + (self.cell_size+10)*y_offset))
            y_offset += 1
            for cell, amount in self.target_inventory_cells[category]:
                if target_inventory_margin + (self.cell_size+10)*(x_offset+1) > root.window_size[0]//2-margin:
                    y_offset += 1
                    x_offset = self.game_manager.get_x_offset()

                cell.change_position(
                    (root.window_size[0] - target_inventory_margin - (self.cell_size+10)*x_offset - self.cell_size,
                    root.window_size[1]//2 - self.target_ico.height//2 + (self.cell_size+10)*y_offset)
                    )
                amount.change_position(
                    (root.window_size[0] - target_inventory_margin - (self.cell_size+10)*x_offset - (self.cell_size - amount.text_rect.width - 5),
                    root.window_size[1]//2 - self.target_ico.height//2 + (self.cell_size+10)*y_offset + amount.text_rect.height//2))
                x_offset += 1
            x_offset = 0
            y_offset += 1
    
    def draw(self):
        root.screen.fill((100, 100, 100))

        self.starter_ico.draw()
        for i, cat in enumerate(self.starter_inventory_cells):
            self.starter_inventory_names[i].draw()
            for cell, amount in self.starter_inventory_cells[cat]:
                cell.draw()
                amount.draw()

        self.target_ico.draw()
        for i, cat in enumerate(self.target_inventory_cells):
            self.target_inventory_names[i].draw()
            for cell, amount in self.target_inventory_cells[cat]:
                cell.draw()
                amount.draw()

        root.need_update_gui = False

    def click(self, button: int, mouse_pos: tuple[int, int]):
        if not self.starter or not self.target or not self.target_inventory or not self.starter_inventory: return
        if mouse_pos[0] < root.window_size[0]//2:
            for category in self.starter_inventory_cells:
                for cell, _ in self.starter_inventory_cells[category]:
                    if cell.rect.collidepoint(mouse_pos):
                        resource = self.starter_inventory.get_resource(resource_name=cell.resource_name, resource_amount="all" if button == 1 else 1, with_remove=True)
                        if not resource: return
                        self.target_inventory.add_resouce(resource=resource)
                        self.open(self.target.type.strip())
                        update_gui()
                        return
        elif mouse_pos[0] > root.window_size[0]//2:
            for category in self.target_inventory_cells:
                for cell, _ in self.target_inventory_cells[category]:
                    if cell.rect.collidepoint(mouse_pos):
                        resource = self.target_inventory.get_resource(resource_name=cell.resource_name, resource_amount="all" if button == 1 else 1, with_remove=True)
                        if not resource: return
                        self.starter_inventory.add_resouce(resource=resource)
                        self.open(self.target.type.strip())
                        update_gui()
                        return
    
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