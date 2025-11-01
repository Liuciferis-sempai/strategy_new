from typing import Any
from assets.world.cell import Cell
from assets.pawns.pawn import Pawn
from assets.buildings.building import Building
from assets import root
from assets.root import logger

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
            "spawn": {"coord": tuple[int, int], "type": str, "fraction_id": int},
            "build": {"coord": tuple[int, int], "type": str, "fraction_id": int},
            "change_cell": {"cell": Cell, "coord": tuple[int, int], "new_type": str} #cell and coord are mutually exclusive
        }

    def translate(self, entry: str) -> str:
        if entry == "move":
            return "stand_here"
        elif entry == "add":
            return "add_resource"
        elif entry == "take":
            return "take_resource"
        elif entry == "free":
            return "clear_the_queue"
        elif entry == "cell":
            return "change_cell"

        return entry
        
    def do(self, effect_type: str, effect_data: dict) -> str:
        do_answer = f"execution the effect {effect_type} with data: {[f"{key}: {value}" for key, value in effect_data.items()]}"
        logger.info(do_answer, f"EffectManager.do({effect_type}, {effect_data})")
        match effect_type:
            case "clear_the_queue":
                do_answer = self.cleat_the_queue(effect_data["building"], effect_data["reciept"])
            case "restore_movement_points":
                do_answer = self.restore_movement_points(effect_data["pawn"])
            case "add_resource":
                if effect_data.get("pawn"):
                    do_answer = self.add_resource_to_pawn(effect_data["pawn"], effect_data["resource"], effect_data["amout"])
                else:
                    do_answer = self.add_resource_to_building(effect_data["building"], effect_data["resource"], effect_data["amout"])
            case "take_resource":
                if effect_data.get("pawn"):
                    do_answer = self.remove_resource_from_pawn(effect_data["pawn"], effect_data["resource"], effect_data["amout"])
                else:
                    do_answer = self.remove_resource_from_building(effect_data["building"], effect_data["resource"], effect_data["amout"])
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
                if effect_data.get("coord"):
                    do_answer = self.change_cell_by_coord(effect_data["coord"], effect_data["new_type"])
                else:
                    do_answer = self.change_cell_by_coord(effect_data["cell"].coord, effect_data["new_type"])
            case _:
                do_answer = f"can not do {effect_type}"
                logger.error(f"effect {effect_type} not found", f"EffectManager.do({effect_type}, {effect_data})")
        logger.info(do_answer, f"EffectManager.do({effect_type}, {effect_data})")
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
    
    def build_scheme(self, target_building_str: str, building_coord: tuple[int, int], building_fraction: int) -> str:
        if root.game_manager.buildings_manager.build(target_building_str, building_coord, building_fraction):
            return f"scheme of the building {target_building_str} was successfully constructed using {building_coord} coordinates"
        else:
            return f"scheme of the building {target_building_str} can not be constructed using {building_coord} coordinates"
    
    def spawn(self, type:str|dict, coord: tuple[int, int], fraction_id: int) -> str:
        if root.game_manager.pawns_manager.spawn(type, coord, fraction_id):
            return f"spawned pawn {type if isinstance(type, str) else type["name"]} on coord {coord} for fraction {fraction_id}"
        else:
            return f"can not spawn {type if isinstance(type, str) else type["name"]} on coord {coord} for fraction {fraction_id}"
    
    def build(self, type:str|dict, coord: tuple[int, int], fraction_id: int) -> str:
        if root.game_manager.buildings_manager.build(type, coord, fraction_id):
            return f"builded building {type if isinstance(type, str) else type["name"]} on coord {coord} for fraction {fraction_id}"
        else:
            return f"can not build building {type if isinstance(type, str) else type["name"]} on coord {coord} for fraction {fraction_id}"
    
    def change_cell_by_coord(self, coord: tuple[int, int], new_type: str) -> str:
        return root.game_manager.world_map.change_cell_by_coord(coord, new_type)