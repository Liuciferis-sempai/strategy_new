from .. import root
from ..root import logger
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..gamemanager import GameManager
    from .resources.resource_type import ResourceType

from .buildings.building import Building
from .pawns.pawn import Pawn
from .buildings.towns.town import Town
from ..world.cell import Cell

class TriggerManager:
    def __init__(self, game_manager: "GameManager"):
        self.game_manager = game_manager

    def has_tech(self, tech_id: str, fraction_id: int=-1, **kwargs) -> bool:
        if fraction_id == -1: fraction_id = root.player_id
        
        fraction = self.game_manager.fraction_manager.get_fraction_by_id(fraction_id)
        if tech_id in fraction.technologies:
            return True
        self.game_manager.messenger.set_buffer("no_tech", {"tech": tech_id}, "warning")
        return False
    
    def has_no_tech(self, tech_id: str, fraction_id: int=-1, **kwargs) -> bool:
        return not self.has_tech(tech_id, fraction_id)
    
    def has_policy(self, policy_id: str, fraction_id: int=-1, **kwargs) -> bool:
        if fraction_id == -1: fraction_id = root.player_id

        fraction = self.game_manager.fraction_manager.get_fraction_by_id(fraction_id)
        for policy in fraction.policies:
            if policy_id == policy.id:
                return True
        self.game_manager.messenger.set_buffer("no_policy", {"policy": policy_id}, "warning")
        return False
    
    def has_no_policy(self, tech_id: str, fraction_id: int=-1, **kwargs) -> bool:
        is_ = self.has_tech(tech_id, fraction_id)
        return not is_

    def target_has_resources(self, resources: dict, target: Building|Town|Pawn, **kwargs) -> bool:
        if target:
            if isinstance(target, Town): target = self.game_manager.buildings_manager.get_building_by_coord(target.coord)

            sum_of = {}
            for resource in resources:
                sum_of[resource] = 0

            if isinstance(target.inventory, list):
                sum_of = self._check_resource(resources, target.inventory, sum_of)
            elif isinstance(target.inventory, dict):
                for category in target.inventory:
                    sum_of = self._check_resource(resources, target.inventory[category], sum_of)
            else:
                logger.error(f"False target inventory type ({target.inventory};{type(target.inventory)}) by {target}", f"TriggerManager.target_has_resources({resources}, {target}, ...)")
                return False

            for resource in sum_of:
                if sum_of[resource] < resources[resource]:
                    self.game_manager.messenger.set_buffer("has_not_en_res", {"targer": target.name})
                    return False
        return True

    def _check_resource(self, resources: dict[str, int], target_inventory: list["ResourceType"], sum_of: dict[str, int]) -> dict[str, int]:
        for item in target_inventory:
            for resource in resources:
                if resource == item.name:
                    if sum_of.get(resource, False):
                        sum_of[resource] = item.amount
                    else:
                        sum_of[resource] += item.amount
        return sum_of

    #def _check_for_resourse_in_storage(self, resource: str, resources: dict, building: dict) -> tuple[bool, str]:
    #    for r in building["storage"]:
    #        if resource == r:
    #            if resources[resource] <= building["storage"][r]:
    #                return (True, "")
    #    return (False, "")

    def true(self, *args, **kwargs) -> bool:
        return True

    def false(self, *args, **kwargs) -> bool:
        self.game_manager.messenger.set_buffer("always_false")
        return False

    def stand_on_cell(self, pawn: "Pawn", cell_type: str|bool = False, cell_has: str|bool = False, **kwargs) -> bool:
        cell = self.game_manager.world_map.get_cell_by_coord(pawn.coord)
        if cell_type:
            if isinstance(cell_type, bool): return False
            return self.is_cell_type(cell, cell_type)
        elif cell_has:
            if isinstance(cell_has, bool): return False
            return self.has_cell(cell, cell_has)
                
        return False
    
    def is_cell_type(self, cell: Cell, cell_type: str) -> bool:
        if cell.data.get("type", "") == cell_type:
            return True
        else:
            self.game_manager.messenger.set_buffer("pawn_must_be_on_cell_type", {"cell": cell_type})
            return False

    def has_cell(self, cell: Cell, cell_has: str) -> bool:
        '''
        check if cell has something
        cell_has => object_cat:object_id
        or
        cell_has => object_cat:any #if u need any
        expl: 'building:storage' or 'pawn:any'
        '''
        if cell_has == "scheme":
            return self.has_cell_scheme(cell)
        elif "fauna" in cell_has:
            return self.has_cell_fauna(cell, cell_has)
        elif "flora" in cell_has:
            return self.has_cell_flora(cell, cell_has)
        elif "pawn" in cell_has:
            return self.has_cell_pawn(cell, cell_has)
        elif "building" in cell_has:
            return self.has_cell_building(cell, cell_has)
        return False

    def has_cell_scheme(self, cell: Cell) -> bool:
        if cell.buildings == {}:
            self.game_manager.messenger.set_buffer("no_building_there")
            return False
        else:
            if "scheme" in cell.buildings["name"]:
                return True
            else:
                self.game_manager.messenger.set_buffer("there_are_no_scheme")
                return False

    def has_cell_fauna(self, cell: Cell, cell_has: str) -> bool:
        if cell.fauna == {}:
            self.game_manager.messenger.set_buffer("cell_has_no_fauna")
            return False
        else:
            nec_fauna = cell_has.replace("fauna:", "")
            if cell.fauna["name"] == nec_fauna or nec_fauna == "any":
                return True
            else:
                self.game_manager.messenger.set_buffer("no_necessary_fauna_there", {"nec_fauna": nec_fauna})
                return False
    
    def has_cell_flora(self, cell: Cell, cell_has: str) -> bool:
        if cell.flora == {}:
            self.game_manager.messenger.set_buffer("cell_has_no_flora")
            return False
        else:
            nec_flora = cell_has.replace("flora:", "")
            if cell.flora["name"] == nec_flora or nec_flora == "any":
                return True
            else:
                self.game_manager.messenger.set_buffer("no_necessary_flora_there", {"nec_flora": nec_flora})
                return False
    
    def has_cell_pawn(self, cell: Cell, cell_has: str) -> bool:
        if cell.pawns == []:
            self.game_manager.messenger.set_buffer("cell_has_no_pawn")
            return False
        else:
            nec_pawn = cell_has.replace("flora:", "")
            if nec_pawn == "any": return True
            for pawn in cell.pawns:
                if pawn["type"] == nec_pawn:
                    return True
            self.game_manager.messenger.set_buffer("no_necessary_pawn_there", {"nec_pawn": nec_pawn})
            return False
    
    def has_cell_building(self, cell: Cell, cell_has: str) -> bool:
        if cell.buildings == {}:
            self.game_manager.messenger.set_buffer("cell_has_no_building")
            return False
        else:
            nec_building = cell_has.replace("building:", "")
            if cell.buildings["type"] == nec_building:
                return True
            else:
                self.game_manager.messenger.set_buffer("no_necessary_building_there", {"nec_building": nec_building})
                return False

    def target_is_near(self, pawn: "Pawn", coord: tuple[int, int, int], distance: int|str, **kwargs) -> bool:
        target = self.game_manager.world_map.get_cell_by_coord(coord)

        if isinstance(distance, str):
            distance = int(pawn.data.get("distance", 1))

        if target:
            if abs(pawn.coord[0]-target.coord[0]) <= distance and abs(pawn.coord[1]-target.coord[1]) <= distance:
                return True
            logger.warning(f"target is too far. pawn stand on {pawn.coord}, target stand on {target.coord}. distance must be {distance} or less", f"TriggerManager.target_is_near({pawn}, {coord}, {distance})")
            self.game_manager.messenger.set_buffer("target_is_too_far")
            return False
        else:
            logger.warning(f"target is not recognized. target coord {coord}", f"TriggerManager.target_is_near({pawn}, {coord}, {distance})")
            self.game_manager.messenger.set_buffer("no_target_there")
            return False

    def compare_inventory(self, pawn: "Pawn", pay_inv: str, **kwargs) -> bool:
        building = self.game_manager.buildings_manager.get_building_by_coord(self.game_manager.get_chosen_cell_coord())
        if building.is_scheme:
            total = {}
            for resource in building.scheme_inventory.get_inventory(pay_inv):
                if total.get(resource, False):
                    total[resource.name] += resource.amount
                else:
                    total[resource.name] = resource.amount
            for resource, amount in building.data["cost"].items():
                if total.get(resource, False):
                    if total[resource] < amount:
                        logger.warning(f"not enought of resource {resource}. required: {amount}, available: {total[resource]}", f"TriggerManager.compare_inventory({pawn}, {pay_inv})")
                        self.game_manager.messenger.set_buffer("not_en_res")
                        return False
                else:
                    logger.warning(f"scheme has no resource {resource}", f"TriggerManager.compare_inventory({pawn}, {pay_inv})")
                    self.game_manager.messenger.set_buffer("not_en_res")
                    return False
        return True