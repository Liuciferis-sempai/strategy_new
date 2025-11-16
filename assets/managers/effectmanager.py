from typing import Any, TYPE_CHECKING
import root
from root import logger

if TYPE_CHECKING:
    from world.cell import Cell
    from .pawns.pawn import Pawn
    from .buildings.building import Building
    from .policy.policytable import PolicyCard
    from .towns.town import Town

class EffectManager:
    def __init__(self):
        self.effects: dict[str, dict[str, Any]] = {
            "clear_the_queue": {"building": Building, "reciept": dict},
            "restore_movement_points": {"pawn": Pawn},
            "add_resource": {"pawn": Pawn, "building": Building, "resource": str, "amout": int}, #pawn and building are mutually exclusive
            "take_resource": {"pawn": Pawn, "building": Building, "resource": str, "anout": int}, #pawn and building are mutually exclusive
            "open_share_menu": {"target": str},
            "stand_here": {"pawn": Pawn, "target_cell": Cell},
            "build_scheme": {"target_building_str": str, "building_coord": tuple[int, int], "building_fraction": int},
            "spawn": {"coord": tuple[int, int], "type": str|dict, "fraction_id": int},
            "build": {"coord": tuple[int, int], "type": str|dict, "fraction_id": int},
            "change_cell": {"cell": Cell, "coord": tuple[int, int], "new_type": str}, #cell and coord are mutually exclusive
            "open_area": {"start_coord": tuple[int, int], "end_coord": tuple[int, int]},
            "show_statistic": {"coord": tuple[int, int]},
            "add_policy": {"fraction_id": int, "policy": str|dict|PolicyCard},
            "remove_policy": {"fraction_id": int, "policy": str|dict|PolicyCard},
            "add_popgroup": {"town": Town, "popgroup_name": str, "size": dict},
            "remove_popgroup": {"town": Town, "popgroup_name": str, "size": dict|str},
            "create_fraction": {"name": str, "type": str, "data": dict},
            "attack": {"target": Pawn|Building, "data": dict}
        }
        
    def do(self, effect_type: str, effect_data: dict) -> str:
        do_answer: str = ""
        match effect_type:
            case "clear_the_queue":
                do_answer = self.cleat_the_queue(effect_data["building"], effect_data["reciept"])
            case "restore_movement_points":
                do_answer = self.restore_movement_points(effect_data["pawn"])
            case "add_resource":
                if effect_data.get("pawn"): do_answer = self.add_resource_to_pawn(effect_data["pawn"], effect_data["resource"], effect_data["amout"])
                else: do_answer = self.add_resource_to_building(effect_data["building"], effect_data["resource"], effect_data["amout"])
            case "take_resource":
                if effect_data.get("pawn"): do_answer = self.remove_resource_from_pawn(effect_data["pawn"], effect_data["resource"], effect_data["amout"])
                else: do_answer = self.remove_resource_from_building(effect_data["building"], effect_data["resource"], effect_data["amout"])
            case "open_share_menu":
                do_answer = self.open_share_menu(effect_data["target_of_action"])
            case "stand_here":
                do_answer = self.stand_here(effect_data["pawn"], effect_data["target_cell"])
            case "build_scheme":
                do_answer = self.build_scheme(effect_data["target_building_str"], effect_data["building_coord"], effect_data["building_fraction"])
            case "spawn":
                do_answer = self.spawn(effect_data["type"], effect_data["coord"], effect_data["fraction_id"])
            case "build":
                do_answer = self.build(effect_data["type"], effect_data["coord"], effect_data["fraction_id"])
            case "change_cell":
                if effect_data.get("coord"): do_answer = self.change_cell_by_coord(effect_data["coord"], effect_data["new_type"])
                else: do_answer = self.change_cell_by_coord(effect_data["cell"].coord, effect_data["new_type"])
            case "open_area":
                do_answer = self.open_area(effect_data["start_coord"], effect_data["end_coord"])
            case "show_statistic":
                do_answer = self.show_statistic(effect_data["coord"])
            case "add_policy":
                do_answer = self.add_policy(effect_data["fraction_id"], effect_data["policy"])
            case "remove_policy":
                do_answer = self.remove_policy(effect_data["fraction_id"], effect_data["policy"])
            case "add_popgroup":
                do_answer = self.add_popgroup(effect_data["town"], effect_data["popgroup_name"], effect_data["size"])
            case "remove_popgroup":
                do_answer = self.remove_popgroup(effect_data["town"], effect_data["popgroup_name"], effect_data["size"])
            case "create_fraction":
                do_answer = self.create_fraction(effect_data["name"], effect_data["type"], effect_data.get("data", {}))
            case "attack":
                do_answer = self.attack(effect_data["target"], effect_data["data"])
            case _:
                do_answer = f"effect type {effect_type} does not exist"
                logger.error(f"effect {effect_type} does not exist", f"EffectManager.do(...)")
        logger.info(do_answer, f"EffectManager.do(...)")
        return do_answer

    def cleat_the_queue(self, building: Building, reciept: dict) -> str:
        return building.remove_from_queue(reciept)
    
    def restore_movement_points(self, pawn: Pawn) -> str:
        return root.game_manager.pawns_manager.restore_movement_points(pawn)
    
    def add_resource_to_pawn(self, pawn: Pawn, resource: str, amout: int) -> str:
        return root.game_manager.pawns_manager.add_resource(pawn, resource, amout)

    def add_resource_to_building(self, building: Building, resource: str, amout: int) -> str:
        return root.game_manager.buildings_manager.add_resources(building, resource, amout)

    def remove_resource_from_pawn(self, pawn: Pawn, resource: str, amout: int) -> str:
        return root.game_manager.pawns_manager.remove_resource(pawn, resource, amout)
    
    def remove_resource_from_building(self, building: Building, resource: str, amout: int) -> str:
        return root.game_manager.buildings_manager.remove_resource(building, resource, amout)
    
    def open_share_menu(self, target_of_action: str) -> str:
        root.change_window_state("share_menu")
        root.game_manager.gui.sharemenu.open(target_of_action)
        return f"opened share menu with {target_of_action}"
    
    def stand_here(self, pawn: Pawn, target_cell: Cell) -> str:
        return root.game_manager.pawns_manager.move_pawn(pawn, target_cell)
    
    def build_scheme(self, target_building_str: str, building_coord: tuple[int, int, int], building_fraction: int) -> str:
        if root.game_manager.buildings_manager.build(target_building_str, building_coord, building_fraction):
            return f"scheme of the building {target_building_str} was successfully constructed using {building_coord} coordinates"
        else:
            return f"scheme of the building {target_building_str} can not be constructed using {building_coord} coordinates"
    
    def spawn(self, type:str|dict, coord: tuple[int, int, int], fraction_id: int) -> str:
        if root.game_manager.pawns_manager.spawn(type, coord, fraction_id):
            return f"spawned pawn {type if isinstance(type, str) else type["name"]} on coord {coord} for fraction {fraction_id}"
        else:
            return f"can not spawn {type if isinstance(type, str) else type["name"]} on coord {coord} for fraction {fraction_id}"
    
    def build(self, type:str|dict, coord: tuple[int, int, int], fraction_id: int) -> str:
        if root.game_manager.buildings_manager.build(type, coord, fraction_id):
            return f"builded building {type if isinstance(type, str) else type["name"]} on coord {coord} for fraction {fraction_id}"
        else:
            return f"can not build building {type if isinstance(type, str) else type["name"]} on coord {coord} for fraction {fraction_id}"
    
    def change_cell_by_coord(self, coord: tuple[int, int, int], new_type: str) -> str:
        return root.game_manager.world_map.change_cell_by_coord(coord, new_type)

    def open_area(self, start_coord: tuple[int, int, int], end_coord: tuple[int, int, int]) -> str:
        root.game_manager.world_map.open_area((start_coord, end_coord))
        return f"successfully opened area from {start_coord} to {end_coord}"

    def show_statistic(self, coord: tuple[int, int, int]) -> str:
        building = root.game_manager.buildings_manager.get_building_by_coord(coord)
        if building.is_town:
            building.town.show_statistic()
            return f"successfully showed statistic for town {building.town.name}"
        return f"there are no town or any other structer that have statistic at coord {coord}"

    def add_policy(self, fraction_id: int, policy: str|dict|PolicyCard) -> str:
        return root.game_manager.fraction_manager.add_policy_to_fraction(fraction_id, policy)

    def remove_policy(self, fraction_id: int, policy: str|dict|PolicyCard) -> str:
        return root.game_manager.fraction_manager.remove_policy_to_fraction(fraction_id, policy)
    
    def add_popgroup(self, town: Town, popgroup_name: str, popgroup_size: dict) -> str:
        return town.add_population(popgroup_name, popgroup_size)
    
    def remove_popgroup(self, town: Town, popgroup_name: str, popgroup_size: dict|str) -> str:
        return town.remove_population(popgroup_name, popgroup_size)

    def create_fraction(self, name: str, type: str, data: dict) -> str:
        fraction = root.game_manager.fraction_manager.create_fraction(name, type)
        return f"created {fraction}"
    
    def attack(self, target: Pawn|Building, data: dict) -> str:
        return target.attacked(data)