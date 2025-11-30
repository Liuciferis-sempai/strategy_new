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
from ...auxiliary_stuff import timeit, back_window_state
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from managers.buildings.towns.town import Town
    from ...gamemanager import GameManager

class GUISpawn:
    def __init__(self, game_manager: "GameManager"):
        self.game_manager = game_manager

        self.spawns: list[dict] = []
        self.buttons: list[SpawnPawn] = []
        self.item_width = root.interface_size//4
        self.item_height = root.interface_size//4

    def change_position_for_new_screen_sizes(self):
        y_offset = self.game_manager.get_y_offset()

        y = 10
        for spawn in self.spawns:
            x = 0
            spawn["pawn_img"].change_position((x+10, y_offset + y))
            x += self.item_width+10

            for resorce, amount in zip(spawn["resorces"], spawn["amount"]):
                resorce.change_position((x+10, y+y_offset))
                x += self.item_width+10
                amount.change_position((x+10, y+y_offset))
                x += self.item_width+10

            x += self.item_width//2
            spawn["time"].change_position((x+10, y+y_offset))
            x += self.item_width+10
            spawn["time_cost"].change_position((x+10, y+y_offset))
            x += self.item_width+10
            spawn["allowed"].change_position((root.window_size[0]-self.item_width-10, y+y_offset))
            x += self.item_width+10

    def open(self):
        opened_building = self.game_manager.get_chosen_building()
        if not opened_building.is_town:
            logger.error("opened spawn for not town!", "GUISpawn.open()")
            back_window_state()
            return
        town = opened_building.town
        pawns = self.game_manager.pawns_manager.get_all_pawns_sample_for_fraction(root.player_id)

        self.spawns = []
        for pawn in pawns:
            if not pawn.get("cost"): continue
            self.spawns.append({})
            is_allowed = (True, "")

            if not self._town_has_necessary_buildings(town, pawn): is_allowed = (False, "town_has_not_nec_building")
            if not self._town_has_enought_people(town, pawn): is_allowed = (False, "town_has_not_en_pp")
            if not self._town_has_enought_resources(town, pawn): is_allowed = (False, "town_has_not_en_res")

            allowed_img = "allowed.png" if is_allowed[0] else "not_allowed.png"
            allowed_button = SpawnPawn(width=self.item_width, height=self.item_height, img=allowed_img, pawn_type=f"{pawn["type"]}", is_allowed=is_allowed[0], message=is_allowed[1])
            self.spawns[-1]["allowed"] = allowed_button
            self.buttons.append(allowed_button)
            
            self.spawns[-1]["pawn_img"] = Icon(self.item_width, self.item_height, img=pawn["img"], spec_path="data/pawns/img")
            self.spawns[-1]["time"] = Icon(self.item_width, self.item_height, img="time.png")
            self.spawns[-1]["time_cost"] = TextField(self.item_width, self.item_height, text=str(pawn["cost"]["time"]))

            self.spawns[-1]["resorces"] = [
                Icon(self.item_width, self.item_height, img=resource) for resource in pawn["cost"]["resources"].keys()
            ]
            self.spawns[-1]["amount"] = [
                TextField(self.item_width, self.item_height, text=str(amount)) for amount in pawn["cost"]["resources"].values()
            ]
        self.change_position_for_new_screen_sizes()
            
    def _town_has_enought_people(self, town: "Town", pawn: dict) -> bool:
        for pop in town.popgroups:
            if pop.has_enough_quality(pawn["cost"]["people"]["quality"]):
                if len(pop.size["adult"]) >= pawn["cost"]["people"]["amount"]:
                    return True
        return False

    def _town_has_enought_resources(self, town: "Town", pawn: dict) -> bool:
        if self.game_manager.trigger_manager.target_has_resources(pawn["cost"]["resources"], town):
            return True
        for building in town.conection:
            if building.is_storage:
                if self.game_manager.trigger_manager.target_has_resources(pawn["cost"]["resources"], building):
                    return True
        return False

    def _town_has_necessary_buildings(self, town: "Town", pawn: dict) -> bool:
        necessary_buildings = pawn.get("necessaty_buildings", [])
        if necessary_buildings == []:
            return True
    
        buildings = [(b.type, b.level) for b in town.conection]
        for building in necessary_buildings:
            if building not in buildings:
                return False
        return True

    def close(self):
        pass

    def update_positions(self):
        pass

    def draw(self):
        root.screen.fill((0, 0, 0))

        for spawn in self.spawns:
            for item in spawn.values():
                if isinstance(item, list):
                    for subitem in item:
                        subitem.draw()
                else:
                    item.draw()

        root.need_update_gui = False
    
    def move_up(self):
        self.game_manager.add_y_offset(root.interface_size//8)
        update_gui()

    def move_down(self):
        self.game_manager.add_y_offset(-root.interface_size//8)
        update_gui()

    def move_left(self):
        pass

    def move_right(self):
        pass