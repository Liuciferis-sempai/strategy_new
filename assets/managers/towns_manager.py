import pygame as py
import os
from .. import root
from ..root import logger, read_json_file
from .buildings.towns.popgroup import PopGroup
import copy
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..gamemanager import GameManager

from .buildings.towns.town import Town

class TownManager:
    def __init__(self, game_manager: "GameManager"):
        self.game_manager = game_manager

        self.grouptypes: list[dict] = []
        self.towns: list[Town] = []
        self.blooked_town_ids: list[int] = []
        self.load_grouptypes()

    def load_grouptypes(self):
        self.grouptypes = []
        for pawnsfile in os.listdir("data/pops/data"):
            if pawnsfile.endswith(".json"):
                type = read_json_file(f"data/pops/data/{pawnsfile}")
                self.grouptypes.append(type)

    def build_town(self, id: int, town_: str|dict|Town, coord: tuple[int, int, int], fraction_id: int, building_data: dict = {}) -> Town:
        if id not in self.blooked_town_ids and id >= 0: self.blooked_town_ids.append(id)
        else: return self.build_town(id+1, town_, coord, fraction_id)
        if isinstance(town_, str):
            town = Town(id, town_, coord, fraction_id, building_data, is_default=False)
        elif isinstance(town_, dict):
            town = Town(id, town_["name"], coord, fraction_id, town_.copy(), building_data, False)
        else:
            town = town_
        
        if isinstance(town, Town):
            self.towns.append(town)
            fraction = self.game_manager.fraction_manager.get_fraction_by_id(fraction_id)
            fraction.towns.append(town)
            fraction.statistics["town_count"] += 1
            return town
        else:
            logger.error(f"can not create town", f"TownManager.build_town({id}town_, {coord}, {fraction_id})")
            return Town()

    def remove_town(self, town_: Town) -> bool:
        if town_ in self.towns:
            self.towns.remove(town_)
            town_.destory()
            fraction = self.game_manager.fraction_manager.get_fraction_by_id(town_.fraction_id)
            if town_ in fraction.towns:
                fraction.towns.remove(town_)
                fraction.statistics["town_count"] -= 1
            return True
        return False
    
    def create_pop_group(self, popgroup: str, pop_size: dict | None = None) -> PopGroup:
        if pop_size is None:
            pop_size = {"aged": [70], "adult": [21, 23, 19], "children": [5, 8]}
        for group in self.grouptypes:
            if group["name"] == popgroup:
                return PopGroup(group["name"], copy.deepcopy(group), copy.deepcopy(pop_size))

        logger.error(f"unknow popgroup {popgroup}", f"TownManager.create_pop_group({popgroup}, {pop_size})")
        return PopGroup("unknow", {})

    def get_town_by_id(self, town_id: int) -> Town:
        for town in self.towns:
            if town.id == town_id:
                return town
        return Town()
    
    def get_town_by_coord(self, coord: tuple[int, int, int]) -> Town:
        for town in self.towns:
            if town.coord == coord:
                return town
        return Town()