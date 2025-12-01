import pygame as py
import os
from .. import root
from ..root import logger, read_json_file
import copy
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..gamemanager import GameManager

from .buildings.workbench.workbench import Workbench

class WorkbenchManager:
    def __init__(self, game_manager: "GameManager"):
        self.game_manager = game_manager

        self.workbenchs: list[Workbench] = []
        self.bloocked_workbench_ids: list[int] = []

    def build_workbench(self, id: int, workbench_type: Workbench|None, coord: tuple[int, int, int], fraction_id: int, building_data: dict = {}) -> Workbench:
        if id not in self.bloocked_workbench_ids and id >= 0: self.bloocked_workbench_ids.append(id)
        else: return self.build_workbench(id+1, workbench_type, coord, fraction_id)
    
        if not workbench_type:
            workbench = Workbench(id, coord=coord, fraction_id=fraction_id, building_data=building_data, is_default=False)
        else:
            workbench = workbench_type
        
        self.workbenchs.append(workbench)
        return workbench
    
    def remove_workbench(self, workbench: Workbench) -> bool:
        if workbench in self.workbenchs:
            self.workbenchs.remove(workbench)
            workbench.destroy()
            return True
        return False
    
    def turn(self):
        for workbench in self.workbenchs:
            workbench.turn()