from assets.root import player_id
from assets.pawns.pawn import Pawn
from assets import root
from assets.buildings.building import Building
from assets.functions import logging

class TriggerManager:
    def __init__(self):
        pass

    def has_tech(self, tech_id: str, fraction_id: int=-1) -> bool:
        if fraction_id == -1:
            fraction_id = player_id
        
        fraction = root.handler.allFractions.get_fraction_by_id(fraction_id)
        if fraction != None:
            if tech_id in fraction.technologies:
                return True
        return False
    
    def has_no_tech(self, tech_id: str, fraction_id: int=-1) -> bool:
        return not self.has_tech(tech_id, fraction_id)

    def building_has_resources(self, resources: dict, building: Building) -> bool:
        if building:
            sum_of = {}
            for resource in resources:
                sum_of[resource] = 0

            if isinstance(building.inventory, list):
                for item in building.inventory:
                    for resource in resources:
                        if resource == item.name:
                            if sum_of.get(resource, False):
                                sum_of[resource] = item.amout
                            else:
                                sum_of[resource] += item.amout
            elif isinstance(building.inventory, dict):
                for category in building.inventory:
                    for item in building.inventory[category]:
                        for resource in resources:
                            if resource == item.name:
                                if sum_of.get(resource, False):
                                    sum_of[resource] = item.amout
                                else:
                                    sum_of[resource] += item.amout
            for resource in sum_of:
                if sum_of[resource] < resources[resource]:
                    return False
        return True


    def _check_for_resourse_in_storage(self, resource: str, resources: dict, building: dict) -> bool:
        for r in building["storage"]:
            if resource == r:
                if resources[resource] <= building["storage"][r]:
                    return True
        return False
    
    def true(self, *args, **kwargs) -> bool:
        return True
    
    def stand_on_cell(self, pawn: Pawn, args: dict) -> bool:
        cell = root.handler.world_map.get_cell_by_coord(pawn.coord)
        result = False
        if args.get("cell_type", False):
            if cell.data.get("type", "") == args["cell_type"]:
                result = True
            else:
                return False
        elif args.get("cell_has", False):
            if args["cell_has"] == "scheme":
                if cell.buildings != {}:
                    if "scheme" in cell.buildings["name"]:
                        result = True
                    else:
                        return False
        return result
    
    def target_is_near(self, pawn: Pawn, args: dict) -> bool:
        target = root.handler.buildings_manager.get_building_by_coord(args["coord"])
        if not target:
            target = root.handler.pawns_manager.get_pawn_by_name(args["target_of_action"], args["coord"])

        if target:
            if abs(pawn.coord[0]-target.coord[0]) <= args["distance"] and abs(pawn.coord[1]-target.coord[1]) <= args["distance"]:
                return True
            logging("DEBUG", f"target is too far. pawn stand on {pawn.coord}, target stand on {target.coord}. distance must be {args["distance"]} or less", "TriggerManager.compare_inventory")
        else:
            logging("DEBUG", f"target is not recognized. target coord {args['coord']}", "TriggerManager.compare_inventory")
        return False

    def compare_inventory(self, pawn: Pawn, args: dict) -> bool:
        building = root.handler.buildings_manager.get_building_by_coord(root.handler.get_chosen_cell_coord())
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
                        logging("DEBUG", f"not enought of resource {resource}. required: {amout}, available: {total[resource]}", "TriggerManager.compare_inventory")
                        return False
                else:
                    logging("DEBUG", f"scheme has no resource {resource}", "TriggerManager.compare_inventory")
                    return False
        return True