import pygame as py
import os
import assets.root as root
from assets.root import logger, read_json_file
from .town import Town
from .popgroup import PopGroup
import copy

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from assets.gamemanager import GameManager

class TownManager:
    def __init__(self,):
        
        self.grouptypes: list[dict] = []
        self.towns: list[Town] = []
        self.allowed_town_id = 0
        self.load_grouptypes()

    def load_grouptypes(self):
        self.grouptypes = []
        for pawnsfile in os.listdir("data/pops/data"):
            if pawnsfile.endswith(".json"):
                type = read_json_file(f"data/pops/data/{pawnsfile}")
                self.grouptypes.append(type)

    def build_town(self, town_: str|dict|Town, coord: tuple[int, int, int], fraction_id: int) -> Town:
        if isinstance(town_, str):
            town = Town(self.allowed_town_id, town_, coord, fraction_id, is_default=False)
        elif isinstance(town_, dict):
            town = Town(self.allowed_town_id, town_["name"], coord, fraction_id, town_.copy(), False)
        else:
            town = town_
        
        if isinstance(town, Town):
            self.allowed_town_id += 1
            self.towns.append(town)
            fraction = root.game_manager.fraction_manager.get_fraction_by_id(fraction_id)
            fraction.towns.append(town)
            fraction.statistics["town_count"] += 1
            return town
        else:
            logger.error(f"can not create town", f"TownManager.build_town({town_}, {coord}, {fraction_id})")
            return Town()
    
    def create_pop_group(self, popgroup: str, pop_size: dict = {"aged": [1], "adult": [2, 5, 3], "children": [1, 1]}) -> PopGroup:
        for group in self.grouptypes:
            if group["name"] == popgroup:
                return PopGroup(group["name"], copy.deepcopy(group), pop_size.copy())

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