from .. import root
from ..root import logger
from typing import TYPE_CHECKING, TypeGuard
from ..auxiliary_stuff import *

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

    def check(self, trigger) -> bool:
        if hasattr(self, trigger["type"]):
            return getattr(self, trigger["type"])(**trigger)

        logger.error(f"trigger {trigger["type"]} does not exist", f"TriggerManager.check({trigger})")
        return False

    def has_tech(self, tech_id: str, fraction_id: int=-1, **kwargs) -> bool:
        if fraction_id == -1: fraction_id = root.player_id
        
        fraction = self.game_manager.fraction_manager.get_fraction_by_id(fraction_id)
        if tech_id in fraction.researched_technology:
            return True
        self.game_manager.messenger.set_buffer("no_tech", {"tech": tech_id}, None, "warning")
        return False
    
    def has_no_tech(self, tech_id: str, fraction_id: int=-1, **kwargs) -> bool:
        return not self.has_tech(tech_id, fraction_id)
    
    def has_policy(self, policy_id: str, fraction_id: int=-1, **kwargs) -> bool:
        if fraction_id == -1: fraction_id = root.player_id

        fraction = self.game_manager.fraction_manager.get_fraction_by_id(fraction_id)
        for policy in fraction.policies:
            if policy_id == policy.id:
                return True
        self.game_manager.messenger.set_buffer("no_policy", {"policy": policy_id}, None, "warning")
        return False
    
    def has_no_policy(self, tech_id: str, fraction_id: int=-1, **kwargs) -> bool:
        is_ = self.has_tech(tech_id, fraction_id)
        return not is_

    def inventory_has_resources(self, resources: dict[str, int]|list[ResourceType], inventory: Inventory, **kwargs) -> bool:
        if isinstance(resources, dict):
            for resource, amount in resources.items():
                if not inventory.has_resource(resource_name=resource, resource_amount=amount):
                    return False
        elif isinstance(resources, list):
            for resource in resources:
                if not inventory.has_resource(resource=resource):
                    return False
        else: return False
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
        cell = self.game_manager.get_cell(coord=pawn.coord)
        if cell_type:
            if isinstance(cell_type, bool): return False
            return self.is_cell_type(cell, cell_type)
        elif cell_has:
            if isinstance(cell_has, bool): return False
            return self.has_cell(cell, cell_has)
                
        return False
    
    def is_cell_type(self, cell: Cell, cell_type: str, **kwargs) -> bool:
        if cell.data.get("type", "") == cell_type:
            return True
        else:
            self.game_manager.messenger.set_buffer("pawn_must_be_on_cell_type", {"cell": cell_type})
            return False

    def has_cell(self, cell: Cell, cell_has: str, **kwargs) -> bool:
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
        if is_empty(cell.buildings):
            self.game_manager.messenger.set_buffer("no_building_there")
            return False
        else:
            if "scheme" in cell.buildings["name"]:
                return True
            else:
                self.game_manager.messenger.set_buffer("there_are_no_scheme")
                return False

    def has_cell_fauna(self, cell: Cell, cell_has: str) -> bool:
        if is_empty(cell.fauna):
            self.game_manager.messenger.set_buffer("cell_has_no_fauna")
            return False
        else:
            nec_fauna = cell_has.replace("fauna:", "")
            if equal(cell.fauna["name"], nec_fauna):
                return True
            else:
                self.game_manager.messenger.set_buffer("no_necessary_fauna_there", {"nec_fauna": nec_fauna})
                return False
    
    def has_cell_flora(self, cell: Cell, cell_has: str) -> bool:
        if is_empty(cell.flora):
            self.game_manager.messenger.set_buffer("cell_has_no_flora")
            return False
        else:
            nec_flora = cell_has.replace("flora:", "")
            if equal(cell.flora["name"], nec_flora):
                return True
            else:
                self.game_manager.messenger.set_buffer("no_necessary_flora_there", {"nec_flora": nec_flora})
                return False
    
    def has_cell_pawn(self, cell: Cell, cell_has: str) -> bool:
        if is_empty(cell.pawns):
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
        if is_empty(cell.buildings):
            self.game_manager.messenger.set_buffer("cell_has_no_building")
            return False
        else:
            nec_building = cell_has.replace("building:", "")
            if cell.buildings["type"] == nec_building:
                return True
            else:
                self.game_manager.messenger.set_buffer("no_necessary_building_there", {"nec_building": nec_building})
                return False

    def is_near(self, chosen: Pawn|Building|Cell|None, target: Pawn|Building|Cell|None, distance: int|str, **kwargs) -> bool:
        if not chosen or not target:
            logger.warning(f"target or chosen is not recognized", f"TriggerManager.target_is_near({chosen}, {target}, {distance})")
            self.game_manager.messenger.set_buffer("no_target_there")
            return False

        if isinstance(distance, str): distance = int(chosen.data.get("distance", 1))

        if (
            (abs(chosen.coord[0]-target.coord[0]) <= distance or abs(root.world_map_size[0]-chosen.coord[0]-target.coord[0]) <= distance) and
            (abs(chosen.coord[1]-target.coord[1]) <= distance or abs(root.world_map_size[1]-chosen.coord[1]-target.coord[1]) <= distance)
            ):
            return True
        logger.warning(f"target is too far. pawn stand on {chosen.coord}, target stand on {target.coord}. distance must be {distance} or less", f"TriggerManager.target_is_near({chosen}, {target}, {distance})")
        self.game_manager.messenger.set_buffer("target_is_too_far")
        return False

    def compare_scheme_inventory(self, target: Building|None, pay_inv: str, **kwargs) -> bool:
        if not target:
            logger.warning(f"target is not recognized", f"TriggerManager.compare_scheme_inventory({target})")
            self.game_manager.messenger.set_buffer("no_target_there")
            return False

        if target.is_scheme:
            total = {}
            for resource in target.scheme_inventory.get_inventory(pay_inv):
                if total.get(resource, False):
                    total[resource.name] += resource.amount
                else:
                    total[resource.name] = resource.amount
            for resource, amount in target.data["cost"].items():
                if total.get(resource, False):
                    if total[resource] < amount:
                        logger.warning(f"not enought of resource {resource}. required: {amount}, available: {total[resource]}", f"TriggerManager.compare_scheme_inventory({pay_inv})")
                        self.game_manager.messenger.set_buffer("not_en_res")
                        return False
                else:
                    logger.warning(f"scheme has no resource {resource}", f"TriggerManager.compare_scheme_inventory({pay_inv})")
                    self.game_manager.messenger.set_buffer("not_en_res")
                    return False
        return True