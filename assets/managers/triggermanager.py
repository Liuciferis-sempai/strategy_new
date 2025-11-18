from .. import root
from ..root import logger
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..gamemanager import GameManager

from .buildings.building import Building
from .pawns.pawn import Pawn
from .towns.town import Town

class TriggerManager:
    def __init__(self, game_manager: "GameManager"):
        self.game_manager = game_manager

    def has_tech(self, tech_id: str, fraction_id: int=-1) -> tuple[bool, str]:
        if fraction_id == -1:
            fraction_id = root.player_id
        
        fraction = self.game_manager.fraction_manager.get_fraction_by_id(fraction_id)
        if fraction != None:
            if tech_id in fraction.technologies:
                return (True, "")
        return (False, f"no_tech {tech_id}")
    
    def has_no_tech(self, tech_id: str, fraction_id: int=-1) -> tuple[bool, str]:
        is_, comment = self.has_tech(tech_id, fraction_id)
        return (not is_, comment)

    def target_has_resources(self, resources: dict, target: Building|Town|Pawn) -> tuple[bool, str]:
        if target:
            if isinstance(target, Town): target = self.game_manager.buildings_manager.get_building_by_coord(target.coord)

            sum_of = {}
            for resource in resources:
                sum_of[resource] = 0

            if isinstance(target.inventory, list):
                for item in target.inventory:
                    for resource in resources:
                        if resource == item.name:
                            if sum_of.get(resource, False):
                                sum_of[resource] = item.amout
                            else:
                                sum_of[resource] += item.amout
            elif isinstance(target.inventory, dict):
                for category in target.inventory:
                    for item in target.inventory[category]:
                        for resource in resources:
                            if resource == item.name:
                                if sum_of.get(resource, False):
                                    sum_of[resource] = item.amout
                                else:
                                    sum_of[resource] += item.amout
            for resource in sum_of:
                if sum_of[resource] < resources[resource]:
                    return (False, f"{target.name} has_not_en_res")
        return (True, "")

    #def _check_for_resourse_in_storage(self, resource: str, resources: dict, building: dict) -> tuple[bool, str]:
    #    for r in building["storage"]:
    #        if resource == r:
    #            if resources[resource] <= building["storage"][r]:
    #                return (True, "")
    #    return (False, "")
    
    def true(self, *args, **kwargs) -> tuple[bool, str]:
        return (True, "")
    
    def stand_on_cell(self, pawn: "Pawn", args: dict) -> tuple[bool, str]:
        cell = self.game_manager.world_map.get_cell_by_coord(pawn.coord)
        if args.get("cell_type", False):
            if cell.data.get("type", "") == args["cell_type"]:
                return (True, "")
            else:
                return (False, f"pawn_must_be_on_cell_type {args["cell_type"]}")
        elif args.get("cell_has", False):
            if args["cell_has"] == "scheme":
                if cell.buildings != {}:
                    if "scheme" in cell.buildings["name"]:
                        return (True, "")
                    else:
                        return (False, "there_are_no_scheme")
                else:
                    return (False, "no_building_there")
            elif "fauna" in args["cell_has"]:
                fauna = args["cell_has"].replace("fauna:", "")
                if cell.fauna["name"] == fauna or fauna == "any":
                    return (True, "")
                else:
                    return (False, f"no_fauna_there {fauna}")
        return (False, "ERROR_no_needed_cell_checking_args")
    
    def target_is_near(self, pawn: "Pawn", args: dict) -> tuple[bool, str]:
        target = self.game_manager.world_map.get_cell_by_coord(args["coord"])
        distance = args["distance"]

        if isinstance(distance, str):
            distance = int(pawn.data.get("distance", 1))

        if target:
            if abs(pawn.coord[0]-target.coord[0]) <= distance and abs(pawn.coord[1]-target.coord[1]) <= distance:
                return (True, "")
            logger.warning(f"target is too far. pawn stand on {pawn.coord}, target stand on {target.coord}. distance must be {args["distance"]} or less", f"TriggerManager.target_is_near({pawn}, {args})")
            return (False, "target_is_too_far")
        else:
            logger.warning(f"target is not recognized. target coord {args['coord']}", f"TriggerManager.target_is_near({pawn}, {args})")
            return (False, "no_target_there")

    def compare_inventory(self, pawn: "Pawn", args: dict) -> tuple[bool, str]:
        building = self.game_manager.buildings_manager.get_building_by_coord(self.game_manager.get_chosen_cell_coord())
        if building.is_scheme:
            total = {}
            for resource in building.scheme_inventory[args["pay_inv"]]:
                if total.get(resource, False):
                    total[resource.name] += resource.amout
                else:
                    total[resource.name] = resource.amout
            for resource, amout in building.data["cost"].items():
                if total.get(resource, False):
                    if total[resource] < amout:
                        logger.warning(f"not enought of resource {resource}. required: {amout}, available: {total[resource]}", f"TriggerManager.compare_inventory({pawn}, {args})")
                        return (False, "not_en_res")
                else:
                    logger.warning(f"scheme has no resource {resource}", f"TriggerManager.compare_inventory({pawn}, {args})")
                    return (False, "not_en_res")
        return (True, "")