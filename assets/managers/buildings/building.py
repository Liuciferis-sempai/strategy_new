from types import UnionType
from ... import root
from ...root import logger, language
from ...auxiliary_stuff import *
from typing import Any, TYPE_CHECKING
import math
import copy
from ...world.cell import Cell

if TYPE_CHECKING:
    from .towns.town import Town
    from .storages.storage import Storage
    from .producer.producer import Producer
    from .workbench.workbench import Workbench
    from ..resources.resource_type import ResourceType

class Building:
    def __init__(self, coord: tuple[int, int, int] = (0, 0, 0), cell: Cell = Cell(), data: dict = {"name": "unknow", "type": "unknow", "category": "unknow", "fraction_id": -1, "storage": [], "storage_size": 0, "default_storage": "main"}, is_default: bool = True):
        self.is_default = is_default
        if self.is_default:
            logger.warning("created default building", f"Building.__init__(...)")
        self.coord = coord
        self.name = language.get(data["name"])
        self.type = data["type"]
        self.category = data["category"]
        self.data = data.copy()
        self.cell = cell
        self.conected_with: Town|None
        if data.get("conected_with"):
            self.conected_with = root.game_manager.town_manager.get_town_by_id(data["conected_with"])

        self.fraction_id = data.get("fraction_id", -1)
        if self.fraction_id == -1:
            logger.error("Building created without fraction_id", f"Building.__init__(...)")
        self.level = data.get("level", 0)
        self.max_hp = data.get("max_hp", 100)
        self.max_hp_mod = data.get("max_hp_mod", {})
        self.hp = data.get("max_hp", 100)
        self.hp_mod = data.get("hp_mod", {})
        self.max_service = data.get("max_service", 50)
        self.max_service_mod = data.get("max_service_mod", {})
        self.service = data.get("max_service", 50)
        self.service_mod = data.get("service_mod", {})
        self.necessary_workers = data.get("necessary_workers", {})
        self.can_work: bool = data.get("can_work", False)

        self.set_type(self.data)
        
        if self.data.get("scheme", False):
            self.is_scheme = True
            scheme_inventory_size = 0
            for resource, amount in self.data["cost"].items():
                scheme_inventory_size += int(amount / root.game_manager.resource_manager.get_resource_data(resource)["max_amount"]) #type: ignore
                if amount % root.game_manager.resource_manager.get_resource_data(resource)["max_amount"] != 0:#type: ignore
                    scheme_inventory_size += 1
            scheme_inventory_size = {"cost": scheme_inventory_size, "inventory": scheme_inventory_size}
            self.scheme_inventory = Inventory(scheme_inventory_size, {"cost": [root.game_manager.resource_manager.create(name, amount) for name, amount in self.data["cost"].items()], "inventory": []})
        else:
            self.is_scheme = False

        self.set_inventory(self.data)
    
    def set_type(self, data: dict):
        self.is_workbench = False
        self.is_storage = False
        self.is_producer = False
        self.is_town = False

        if data.get("category", False) == "workbench":
            self.is_workbench = True
            self.workbench: "Workbench" = root.game_manager.workbench_manager.build_workbench(id=self.data.get("workbench_id", -1), workbench_type=None, building_data=self.data, coord=self.coord, fraction_id=self.fraction_id)

        elif data.get("category", False) == "storage":
            self.is_storage = True
            self.storage: "Storage" = root.game_manager.storage_manager.build_storage(id=self.data.get("storage_id", -1), storage_type=None, building_data=self.data, coord=self.coord, fraction_id=self.fraction_id)

        elif data.get("category", False) == "producer":
            self.is_producer = True
            self.producer = root.game_manager.producer_manager.build_producer(id=self.data.get("producer_id", -1), producer_type=None, building_data=self.data, coord=self.coord, fraction_id=self.fraction_id)

        elif data.get("category", False) == "town":
            self.is_town = True
            self.town: "Town" = root.game_manager.town_manager.build_town(id = self.data.get("town_id", -1), town_ = self.name, coord = self.coord, fraction_id = self.fraction_id, building_data = self.data)

    def set_inventory(self, data: dict):
       self.inventory = Inventory(data["storage_size"], data["storage"], data.get("default_storage", "any"))
    
    def __repr__(self) -> str:
        if not self:
            return f"<Building is default>"
        else:
            return f"<Building {self.name} on coord {self.coord}>"
    
    def __bool__(self) -> bool:
        return not self.is_default

    def add_resource(self, resource_name: str = "unknow", resource_amount: int = 0, resource: ResourceType|None = None, inv_type: str = "main") -> str:
        return self.inventory.add_resouce(resource_name, resource_amount, resource, inv_type)

    def remove_resource(self, resource_name: str = "unknow", resource_amount: int = 0, resource: ResourceType|None = None, inv_type: str = "main") -> str:
        return self.inventory.remove_resource(resource_name, resource_amount, resource, inv_type)

    def get_queue_lenght(self) -> int:
        if self.is_workbench:
            return len(self.workbench.queue)
        elif self.is_town:
            return len(self.town.queue)
        return 0
    
    def get_queue_max_lenght(self) -> int:
        if self.is_workbench:
            return self.workbench.max_queue
        elif self.is_town:
            return self.town.max_queue
        return 0

    def get_queue(self) -> list:
        if self.is_workbench:
            return self.workbench.queue
        elif self.is_town:
            return self.town.queue
        return []

    def get_max_hp(self) -> int:
        max_hp = self.max_hp
        for mod in self.max_hp_mod.values():
            max_hp += mod
        return max_hp
    
    def get_hp(self) -> int:
        hp = self.hp
        for mod in self.hp_mod.values():
            hp += mod
        return hp
    
    def get_max_service(self) -> int:
        max_service = self.max_service
        for mod in self.max_service_mod.values():
            max_service += mod
        return max_service

    def get_service(self) -> int:
        service = self.service
        for mod in self.service_mod.values():
            service += mod
        return service
    
    def take_damage(self, damage: int):
        self.hp -= damage
        if self.get_hp() <= 0:
            self.destroy()

    def conect(self, town: "Town"):
        self.conected_with = town
        if self.necessary_workers == {}:
            self.set_can_work(True)
            return

        for pop in self.conected_with.popgroups:
            if pop.has_enough_quality(self.necessary_workers.get("quality", {})):
                if pop.add_workers(self.necessary_workers["amount"]):
                    self.set_can_work(True)
                    return
        self.set_can_work(False)

    def deconect(self):
        self.conected_with = None
        self.set_can_work(False)

    def set_can_work(self, value: bool):
        if self.can_work == value: return
        
        self.can_work = value
        if self.is_workbench:
            self.workbench.can_work = value
        elif self.is_storage:
            self.storage.can_work = value
        elif self.is_producer:
            self.producer.can_work = value

    def get_food_value_in_storage(self) -> int:
        food_value = 0
        if isinstance(self.inventory, list):
            for resource in self.inventory:
                if resource.is_food:
                    food_value += resource.food_value
        elif isinstance(self.inventory, dict):
            for storage in self.inventory.values():
                for resorce in storage:
                    if resorce.is_food:
                        food_value += resorce.food_value
        return food_value
    
    def remove_food_for_value(self, remainder: int|float) -> int|float:
        if isinstance(self.inventory, list):
            for resource in self.inventory:
                if not resource.is_food:
                    continue

                needed_units = math.ceil(remainder / resource.food_value)
                to_remove = min(needed_units, resource.amount)
                self.remove_resource(resource.name, to_remove)

                remainder -= to_remove * resource.food_value

                if remainder <= 0:
                    return 0

        return remainder
    
    def attacked(self, attack: dict) -> str:
        self.take_damage(attack["damage"])
        return f"{self} taked {attack["damage"]} damage"

    def destroy(self):
        root.game_manager.buildings_manager.remove(self.coord)
        root.game_manager.buildings_manager.build({"name": f"ruin of_{self.name}", "type": f"ruin of_{self.type}", "category": "ruin", "desc": f"ruin_of_{self.data["desc"]}", "img": f"ruin_of_{self.data["img"]}", "level": self.level}, self.coord, self.fraction_id)

    def can_be_upgraded(self) -> bool:
        if self.data.get("upgrades", False):
            if self.data["upgrades"].get(str(self.level+1), False):
                return True
        return False

    def upgrade(self):
        if self.is_scheme:
            self.is_scheme = False
            for effect in self.data["upgrades"][str(self.level)]["effect"]:
                self.do_change(effect["type"], effect["args"])
            self.cell.buildings = extract_building_data_for_cell(self.data)

    def do_change(self, type: str, args: dict[str, Any]):
        match type:
            case "change_text":
                self.name = args.get("new_name", self.name)
                self.data["name"] = self.name
                self.data["desc"] = args.get("new_desc", self.data["desc"])
                self.data["img"] = args.get("new_img", self.data["img"])
            case "change_numbers":
                self.max_hp = args.get("max_hp", self.max_hp)
                self.max_service = args.get("max_service", self.max_service)
                if self.queue or args.get("queue", False):
                    self.queue = args.get("queue", self.queue)
            case "change_type":
                self.data["type"] = args.get("new_type", self.data["type"])
                self.set_type(self.data)
            case "change_storage_type":
                if args.get("new_type", False):
                    self.data["storage_type"] = args["new_type"]
                    temp_inv = copy.deepcopy(self.inventory)
                    if args["new_type"] == "list" and isinstance(temp_inv, dict):
                        self.data["storage"] = []
                        self.data["storage_size"] = args["new_size"]
                        self.set_inventory(self.data)
                        for inv in temp_inv.values():
                            for resource in inv:
                                self.inventory.append(resource) #type: ignore
                    elif args["new_type"] == "dict" and isinstance(temp_inv, list):
                        self.data["storage"] = {}
                        self.data["storage_size"] = args["new_size"]
                        self.set_inventory(self.data)
                        for resource in temp_inv:
                            self.add_resource(resource.name, resource.amount)
            case "change_storage_size":
                self.inventory_size = args.get("new_size", self.inventory_size)

    def set_upgrade_mod(self, mod: bool):
        if mod:
            if self.can_be_upgraded():
                self.is_scheme = True
                self.level += 1
                self.scheme_inventory = {"cost": [root.game_manager.resource_manager.create(name, amount) for name, amount in self.data["upgrades"][str(self.level)]["cost"].items()], "inventory": []}
                self.scheme_inventory_size = 0
                for resource, amount in self.data["cost"].items():
                    self.scheme_inventory_size += int(amount / root.game_manager.resource_manager.get_resource_data(resource)["max_amount"]) #type: ignore
                    if amount % root.game_manager.resource_manager.get_resource_data(resource)["max_amount"] != 0:#type: ignore
                        self.scheme_inventory_size += 1
                self.scheme_inventory_size = {"cost": self.scheme_inventory_size, "inventory": self.scheme_inventory_size}

                self.name = "scheme of_" + self.name
                self.data["name"] = self.name
                self.data["scheme"] = True
                self.cell.buildings = extract_building_data_for_cell(self.data)
                self.cell.resize()
            else:
                logger.error(f"Building can not be upgraded", f"Building.set_upgrade_mod({mod})")
        else:
            self.is_scheme = False

    def has_free_space(self) -> bool:
        return True

    def add_in_queue(self, reciept: dict|str):
        if self.is_workbench:
            self.workbench.add_in_queue(reciept)
        elif self.is_town:
            self.town.add_in_queue(reciept)

    def remove_from_queue(self, reciept:dict|str) -> str:
        if self.is_workbench:
            return self.workbench.remove_from_queue(reciept)
        elif self.is_town:
            return self.town.remove_from_queue(reciept)
        else:
            return "has no queue"
    
    def build(self):
        if self.is_scheme:
            self.name = self.name.replace("scheme of_", "")
            self.data["name"] = self.name
            self.data["img"].replace("_scheme.png", ".png")
            self.data["scheme"] = False
            self.set_inventory(self.data)
            self.cell.buildings = extract_building_data_for_cell(self.data)
            self.cell.resize()
            if self.level != 0:
                self.upgrade()
            self.is_scheme = False
            update_gui()

            fraction = root.game_manager.fraction_manager.get_fraction_by_id(self.fraction_id)
            for town in fraction.towns:
                town.check_conection()