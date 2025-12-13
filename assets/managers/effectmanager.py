from typing import Any, TYPE_CHECKING
from .. import root
from ..root import logger

if TYPE_CHECKING:
    from ..gamemanager import GameManager

from ..world.cell import Cell
from .pawns.pawn import Pawn
from .buildings.building import Building
from .policy.policytable import PolicyCard
from .buildings.towns.town import Town

class EffectManager:
    def __init__(self, game_manager: "GameManager"):
        self.game_manager = game_manager

        self.effects: dict[str, dict[str, Any]] = {
            "clear_the_queue": {"building": Building},
            "restore_movement_points": {"pawn": Pawn},
            "add_resource": {"pawn": Pawn, "building": Building, "resource": str, "amount": int}, #pawn and building are mutually exclusive
            "take_resource": {"pawn": Pawn, "building": Building, "resource": str, "anout": int}, #pawn and building are mutually exclusive
            "take_loot": {"pawn": Pawn, "loot": dict["resource": str, "amount": int]},
            "open_share_menu": {"target": str},
            "stand_here": {"pawn": Pawn, "target_cell": Cell},
            "build_scheme": {"building": Building},
            "spawn": {"coord": tuple[int, int], "type": str|dict, "fraction_id": int},
            "build": {"coord": tuple[int, int], "type": str|dict, "fraction_id": int},
            "change_cell": {"cell": "Cell", "coord": tuple[int, int], "new_type": str}, #cell and coord are mutually exclusive
            "open_area": {"start_coord": tuple[int, int], "end_coord": tuple[int, int]},
            "show_statistic": {"coord": tuple[int, int]},
            "add_policy": {"fraction_id": int, "policy": str|dict|PolicyCard},
            "remove_policy": {"fraction_id": int, "policy": str|dict|PolicyCard},
            "add_popgroup": {"town": Town, "popgroup_name": str, "size": dict},
            "remove_popgroup": {"town": Town, "popgroup_name": str, "size": dict|str},
            "create_fraction": {"name": str, "type": str, "data": dict},
            "attack": {"target": Pawn|Building, "data": dict},
            "call_event": {"event_id": str},
            "reseach_building": {"building_type": str, "fraction_id": int},
            "reseach_pawn": {"pawn_type": str, "fraction_id": int},
            "reseach_policy": {"policy_id": str, "fraction_id": int},
            "add_eventListener": {"trigger": dict|list, "effect": dict|list},
            "give_achievment": {"name": str}
        }
        self.effects_names = self.effects.keys()
        
    def do(self, effect_type: str, effect_data: dict) -> str:
        self.game_manager.listener.happend(effect_type, **effect_data)
        do_answer: str = ""
        match effect_type:
            case "clear_the_queue":
                do_answer = self.cleat_the_queue(effect_data["building"])
            case "restore_movement_points":
                do_answer = self.restore_movement_points(effect_data["pawn"])
            case "add_resource":
                if effect_data.get("pawn"): do_answer = self.add_resource_to_pawn(effect_data["pawn"], effect_data["resource"], effect_data["amount"])
                else: do_answer = self.add_resource_to_building(effect_data["building"], effect_data["resource"], effect_data["amount"])
            case "take_resource":
                if effect_data.get("pawn"): do_answer = self.remove_resource_from_pawn(effect_data["pawn"], effect_data["resource"], effect_data["amount"])
                else: do_answer = self.remove_resource_from_building(effect_data["building"], effect_data["resource"], effect_data["amount"])
            case "take_loot":
                do_answer = self.take_loot(effect_data["pawn"], effect_data["loot"])
            case "open_share_menu":
                do_answer = self.open_share_menu(effect_data["target"])
            case "stand_here":
                do_answer = self.stand_here(effect_data["pawn"], effect_data["target"])
            case "build_scheme":
                do_answer = self.build_scheme(effect_data["building"])
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
            case "call_event":
                do_answer = self.call_event(effect_data["event_id"])
            case "add_eventListener":
                do_answer = self.add_eventListener(effect_data["trigger"], effect_data["effect"])
            case "give_achievment":
                do_answer = self.give_achievment(effect_data["name"])
            case _:
                do_answer = f"effect type {effect_type} does not exist"
                logger.error(f"effect {effect_type} does not exist", f"EffectManager.do(...)")
        logger.info(do_answer, f"EffectManager.do(...)")
        return do_answer

    def cleat_the_queue(self, building: "Building") -> str:
        self.game_manager.messenger.print("cleared_queue_by_building", {"building_name": building.name}, building.coord)
        building.clear_the_queue()
        return f"cleared queue by {building.name}"
    
    def restore_movement_points(self, pawn: "Pawn") -> str:
        self.game_manager.messenger.print("restored_movement_points", {"pawn_name": pawn.name}, pawn.coord)
        return self.game_manager.pawns_manager.restore_movement_points(pawn)
    
    def add_resource_to_pawn(self, pawn: "Pawn", resource: str, amount: int) -> str:
        self.game_manager.messenger.print("pawn_get_res", {"pawn_name": pawn.name, "resource": root.language.get(resource)}, pawn.coord)
        return self.game_manager.pawns_manager.add_resource(pawn, resource, amount)

    def add_resource_to_building(self, building: "Building", resource: str, amount: int) -> str:
        self.game_manager.messenger.print("building_get_res", {"building_name": building.name, "resource": root.language.get(resource)}, building.coord)
        remainder = self.game_manager.buildings_manager.add_resources(building, resource, amount)
        if remainder == 0:        return f"{building.name} get {amount} {resource}"
        elif remainder != amount: return f"{building.name} get {amount-remainder} {resource} and {remainder} left"
        else:                     return f"{building.name} can not get {amount} {resource}"

    def remove_resource_from_pawn(self, pawn: "Pawn", resource: str, amount: int) -> str:
        self.game_manager.messenger.print("pawn_lost_res", {"pawn_name": pawn.name, "resource": root.language.get(resource)}, pawn.coord)
        return self.game_manager.pawns_manager.remove_resource(pawn, resource, amount)
    
    def remove_resource_from_building(self, building: "Building", resource: str, amount: int) -> str:
        self.game_manager.messenger.print("buildig_lost_res", {"building_name": building.name, "resouce": root.language.get(resource)}, building.coord)
        remainder = self.game_manager.buildings_manager.remove_resource(building, resource, amount)
        if remainder == 0:        return f"{building.name} take {amount} {resource}"
        elif remainder != amount: return f"{building.name} take {amount-remainder} {resource} and {remainder} left"
        else:                     return f"{building.name} can not take {amount} {resource}"

    def take_loot(self, pawn: Pawn, loot: dict[str, int]) -> str:
        answer = ""
        for resource, amount in loot.items():
            self.game_manager.messenger.print("pawn_get_loot", {"pawn": pawn.name, "resource": root.language.get(resource)}, pawn.coord)
            answer += self.game_manager.pawns_manager.add_resource(pawn, resource, amount) + "\n"
        return answer
    
    def open_share_menu(self, target_of_action: str) -> str:
        root.change_window_state("share_menu")
        self.game_manager.gui.sharemenu.open(target_of_action)
        return f"opened share menu with {target_of_action}"
    
    def stand_here(self, pawn: "Pawn", target_cell: "Cell") -> str:
        return self.game_manager.pawns_manager.move_pawn(pawn, target_cell)
    
    def build_scheme(self, building: Building) -> str:
        if building.build():
            self.game_manager.messenger.print("builded_scheme", {"coord": building.coord})
            return f"builded scheme {building.name}"
        else:
            if building.is_scheme:
                return f"can not build scheme on coord {building.coord}"
            else:
                self.game_manager.messenger.print("building_is_not_the_scheme")
                return f"building is not the scheme"
    
    def spawn(self, pawn_type:str|dict, coord: tuple[int, int, int], fraction_id: int) -> str:
        if self.game_manager.pawns_manager.spawn(pawn_type, coord, fraction_id):
            self.game_manager.messenger.print("spawned_pawn_on_coord", {"pawn": pawn_type if isinstance(pawn_type, str) else pawn_type["name"], "coord_x": coord[0], "coord_y": coord[1]}, coord)
            return f"spawned pawn {pawn_type if isinstance(pawn_type, str) else pawn_type["name"]} on coord {coord} for fraction {fraction_id}"
        else:
            self.game_manager.messenger.print("can_not_spawn_pawn_on_coord", {"coord_x": coord[0], "coord_y": coord[1]})
            return f"can not spawn {pawn_type if isinstance(pawn_type, str) else pawn_type["name"]} on coord {coord} for fraction {fraction_id}"
    
    def build(self, building_type:str|dict, coord: tuple[int, int, int], fraction_id: int) -> str:
        if self.game_manager.buildings_manager.build(building_type, coord, fraction_id):
            self.game_manager.messenger.print("builded_building_on_coord", {"building": building_type if isinstance(building_type, str) else building_type["name"], "coord_x": coord[0], "coord_y": coord[1]}, coord)
            return f"builded building {building_type if isinstance(building_type, str) else building_type["name"]} on coord {coord} for fraction {fraction_id}"
        else:
            self.game_manager.messenger.print("can_not_build_building_on_coord", {"coord_x": coord[0], "coord_y": coord[1]})
            return f"can not build building {building_type if isinstance(building_type, str) else building_type["name"]} on coord {coord} for fraction {fraction_id}"
    
    def change_cell_by_coord(self, coord: tuple[int, int, int], new_type: str) -> str:
        return self.game_manager.world_map.change_cell_by_coord(coord, new_type)

    def open_area(self, start_coord: tuple[int, int, int], end_coord: tuple[int, int, int]) -> str:
        self.game_manager.world_map.open_area((start_coord, end_coord))
        return f"successfully opened area from {start_coord} to {end_coord}"

    def show_statistic(self, coord: tuple[int, int, int]) -> str:
        building = self.game_manager.get_building(coord=coord)
        if building.is_town:
            building.town.show_statistic()
            return f"successfully showed statistic for town {building.town.name}"
        return f"there are no town or any other structer that have statistic at coord {coord}"

    def add_policy(self, fraction_id: int, policy: str|dict|PolicyCard) -> str:
        self.game_manager.messenger.print("fraction_get_new_policy", {"fraction": self.game_manager.fraction_manager.get_fraction_by_id(fraction_id).name})
        return self.game_manager.fraction_manager.add_policy_to_fraction(fraction_id, policy)

    def remove_policy(self, fraction_id: int, policy: str|dict|PolicyCard) -> str:
        self.game_manager.messenger.print("fraction_lost_policy", {"fraction": self.game_manager.fraction_manager.get_fraction_by_id(fraction_id).name})
        return self.game_manager.fraction_manager.remove_policy_to_fraction(fraction_id, policy)
    
    def add_popgroup(self, town: Town, popgroup_name: str, popgroup_size: dict) -> str:
        self.game_manager.messenger.print("town_has_new_popgroup", {"town": town.name, "popgroup": popgroup_name})
        return town.add_population(popgroup_name, popgroup_size)
    
    def remove_popgroup(self, town: Town, popgroup_name: str, popgroup_size: dict|str) -> str:
        self.game_manager.messenger.print("town_lost_new_popgroup", {"town": town.name, "popgroup": popgroup_name})
        return town.remove_population(popgroup_name, popgroup_size)

    def create_fraction(self, name: str, type: str, data: dict) -> str:
        self.game_manager.messenger.print("created_new_fraction", {"fraction": name})
        fraction = self.game_manager.fraction_manager.create_fraction(name, type)
        return f"created {fraction}"
    
    def attack(self, target: Pawn|Building, data: dict) -> str:
        self.game_manager.messenger.print("target_under_attack", {"target": target.name})
        return target.attacked(data)

    def call_event(self, event_id: str) -> str:
        return self.game_manager.event_manager.event_call(event_id)
    
    def add_eventListener(self, trigger: dict|list, effect: dict|list) -> str:
        answer = self.game_manager.addListener(trigger, effect)
        return f"added {answer[0]} Listener"
    
    def give_achievment(self, name: str) -> str:
        answer = self.game_manager.achievments_manager.do_achievment(name)
        if answer:
            return f"gave achievment {name} to player"
        else:
            return f"can not give achievment {name} to player"