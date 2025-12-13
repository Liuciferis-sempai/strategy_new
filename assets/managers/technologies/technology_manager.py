from ...auxiliary_stuff import *
import pygame as py
import os
from ... import root
from ...auxiliary_stuff import *
from .tech import Tech
from .techtree import Techtree
from ...root import loading, logger
from typing import TYPE_CHECKING
import copy

if TYPE_CHECKING:
    from ...gamemanager import GameManager

from ...managers.fraction.fraction import Fraction

class TechnologyManager:
    def __init__(self, game_manager: "GameManager"):
        self.game_manger = game_manager

        self.technologies: list[dict] = []
        loading.draw("Loading technologies...")
        self.load_techs()

    def load_techs(self):
        for techfile in os.listdir("data/technologies"):
            if techfile.endswith(".json"):
                tech_data = read_json_file(f"data/technologies/{techfile}")
                self.technologies.append(tech_data)
    
    def get_technology(self, tech_id: str) -> dict:
        for technology in self.technologies:
            if technology["id"] == tech_id:
                return copy.deepcopy(technology)
        
        logger.warning(f"technology {tech_id} not found", f"TechnologyManager.get_technology({tech_id})")
        return {}.copy()
    
    def create_techtree(self, tech_tree_data: list[dict], fraction_id: int) -> Techtree:
        if is_empty(tech_tree_data): tech_tree_data = copy.deepcopy(self.technologies)
        return Techtree(tech_tree_data, fraction_id)
    
    def reseach_technology(self, technology_id: str, fraction_id: int = -1):
        technology = self.get_technology(technology_id)
        if is_empty(technology): return
        if not has(technology, "effect"): return

        for effect in technology["effect"]:
            if has(effect, "trigger"):
                if not self.game_manger.trigger(effect["trigger"], is_parsed=False, calling_fraction_id=fraction_id): continue
            self.game_manger.execute_effect(effect["result"], is_parsed=False, calling_fraction_id=fraction_id)