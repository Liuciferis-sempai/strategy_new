import pygame as py
import os
from .. import root
from ..root import logger, read_json_file
import copy
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..gamemanager import GameManager

from .buildings.scientific.scientific import Scientific

class ScientificManager:
    def __init__(self, game_manager: "GameManager"):
        self.game_manager = game_manager

        self.scientifics: list[Scientific] = []
        self.bloocked_scientific_ids: list[int] = []

    def build_scientific(self, id: int, scientific_type: Scientific|None, coord: tuple[int, int, int], fraction_id: int, building_data: dict = {}) -> Scientific:
        if id not in self.bloocked_scientific_ids and id >= 0: self.bloocked_scientific_ids.append(id)
        else: return self.build_scientific(id+1,scientific_type, coord, fraction_id, building_data)
    
        if not scientific_type:
            scientific = Scientific(id=id, coord=coord, fraction_id=fraction_id, data=None, building_data=building_data, is_default=False)
        else:
            scientific = scientific_type
        
        self.scientifics.append(scientific)
        return scientific
    
    def remove_scientific(self, scientific: Scientific) -> bool:
        if scientific in self.scientifics:
            self.scientifics.remove(scientific)
            scientific.destroy()
            return True
        return False
    
    def turn(self):
        for scientific in self.scientifics:
            scientific.turn()