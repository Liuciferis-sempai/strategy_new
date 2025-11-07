from assets import root
from assets.root import logger
from assets.auxiliary_stuff.functions import update_gui
from assets.world.cell import Cell
from assets.towns.town import Town
from typing import Any
import math

class Building:
    def __init__(self, coord: tuple[int, int] = (0, 0), cell: Cell = Cell(), data: dict = {"name": "unknow", "type": "unknow"}, is_default: bool = True):
        self.is_default = is_default
        if self.is_default:
            logger.warning("created default building", f"Building.__init__(...)")
        self.coord = coord
        self.name = data["name"]
        self.type = data["type"]
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
        self.workers = data.get("workers", {})

        self.set_type(self.data)
        
        if self.data.get("scheme", False):
            self.is_scheme = True
            self.scheme_inventory = {"cost": [root.game_manager.resource_manager.create(name, amount) for name, amount in self.data["cost"].items()], "inventory": []}
            self.scheme_inventory_size = 0
            for resource, amount in self.data["cost"].items():
                self.scheme_inventory_size += int(amount / root.game_manager.resource_manager.get_resource_data(resource)["max_amount"]) #type: ignore
                if amount % root.game_manager.resource_manager.get_resource_data(resource)["max_amount"] != 0:#type: ignore
                    self.scheme_inventory_size += 1
            self.scheme_inventory_size = {"cost": self.scheme_inventory_size, "inventory": self.scheme_inventory_size}
        else:
            self.is_scheme = False

        self.set_inventory(self.data)
    
    def set_type(self, data: dict):
        self.is_workbench = False
        self.is_producer = False
        self.is_town = False
        if data.get("type", False) == "workbench":
            if self.is_workbench: return
            self.is_workbench = True
            self.max_queue = data.get("max_queue", 1)
            self.queue = data.get("queue", [])
            if self.queue != []:
                for item in self.queue:
                    self.add_in_queue(item)

        elif data.get("type", False) == "producer":
            if self.is_producer: return
            self.is_producer = True
            self.prodaction_time = data.get("prodaction_time", 1)
            self.last_prodaction_at = data.get("last_prodaction_at", root.game_manager.turn_manager.turn)
            self.prodaction = data.get("prodaction", {})
            def produce(self: Building):
                for resource, amount in self.prodaction.items():
                    self.add_resource(resource, amount, "output")
            self.produce = produce

        elif data.get("type", False) == "town":
            if self.is_town: return
            self.is_town = True
            self.town: Town = root.game_manager.town_manager.build_town(self.name, self.coord, self.fraction_id)

    def set_inventory(self, data: dict):
        if data.get("storage_type") == "dict":
            self.inventory = {}
            self.inventory_size = data.get("storage_size", {"input": 5, "output": 2})
            
            self.data["inventory_size"] = self.inventory_size
            def add_resource_(resource: str, amount: int, type_: str="none", *args) -> str:
                '''
                type: str -> type of storage
                For Example: type="input"
                '''
                type = self._determine_type(resource, type_)
                if type == "none":
                    return f"building {self.name} has no {type_} for {resource}"
                if self.is_scheme:
                    remainder = amount
                    while len(self.scheme_inventory[type]) < self.scheme_inventory_size[type] and remainder > 0: #type: ignore
                        if self.scheme_inventory[type] != []: #type: ignore
                            for item in self.scheme_inventory[type]: #type: ignore
                                if item.name == resource:
                                    remainder = item.add(amount)
                        if remainder > 0:
                            self.scheme_inventory[type].append(root.game_manager.resource_manager.create(resource, remainder)) #type: ignore
                            remainder -= self.scheme_inventory[type][-1].max_amount
                        self.optimize_inventory(type)
                        return f"building '{self.name}' received {resource} in quantity {amount} to storage {type}"
                else:
                    remainder = amount
                    while len(self.inventory[type]) < self.inventory_size[type] and remainder > 0: #type: ignore
                        if self.inventory[type] != []: #type: ignore
                            for item in self.inventory[type]: #type: ignore
                                if item.name == resource:
                                    remainder = item.add(remainder)
                        if remainder > 0:
                            self.inventory[type].append(root.game_manager.resource_manager.create(resource, remainder)) #type: ignore
                            remainder -= self.inventory[type][-1].max_amount
                        self.optimize_inventory(type)
                        return f"building '{self.name}' received {resource} in quantity {amount} to storage {type}"
                return f"building {self.name} can not receiv {resource} in {type} ({type_})"

            def remove_resource_(resource: str, amount: int, type_: str="none", *args) -> str:
                '''
                type: str -> type of storage
                For Example: type="input"
                '''
                type = self._determine_type(resource, type_)
                if type == "none":
                    return f"building {self.name} has no {type_} for {resource}"
                if self.is_scheme:
                    for item in self.scheme_inventory[type]: #type: ignore
                        if item.name == resource:
                            if item.take(amount):
                                if item.amount <= 0:
                                    self.scheme_inventory[type].remove(item) #type: ignore
                                self.optimize_inventory(type)
                                return f"building '{self.name}' gave {resource} in quantity {amount} from storage {type}"
                else:
                    for item in self.inventory[type]: #type: ignore
                        if item.name == resource:
                            if item.take(amount):
                                if item.amount <= 0:
                                    self.inventory[type].remove(item) #type: ignore
                                self.optimize_inventory(type)
                                return f"building '{self.name}' gave {resource} in quantity {amount} from storage {type}"
                return f"building {self.name} can not give {resource} from {type} ({type_})"

            def optimize_inventory_(type: str, *args):
                if self.is_scheme:
                    for j, item in enumerate(self.scheme_inventory[type]): #type: ignore
                        for i, item_ in enumerate(self.scheme_inventory[type]): #type: ignore
                            if item.name == item_.name and i != j:
                                remainder = item.add(item_.amount)
                                if remainder == 0:
                                    self.scheme_inventory[type].remove(item_) #type: ignore
                                else:
                                    item_.amount = remainder
                else:
                    for j, item in enumerate(self.inventory[type]): #type: ignore
                        for i, item_ in enumerate(self.inventory[type]): #type: ignore
                            if item.name == item_.name and i != j:
                                remainder = item.add(item_.amount)
                                if remainder == 0:
                                    self.inventory[type].remove(item_) #type: ignore
                                else:
                                    item_.amount = remainder

            self.add_resource = add_resource_
            self.remove_resource = remove_resource_
            self.optimize_inventory = optimize_inventory_

            if self.inventory == {}:
                for key in self.inventory_size.keys():
                    self.inventory[key] = []
            for type in data.get("storage", {}):
                for resource, amount in data["storage"][type]:
                    self.add_resource(resource, amount, type)

        else:
            self.inventory = data.get("storage", [])
            self.inventory_size = data.get("storage_size", 1)

            def add_resource(resource: str, amount: int, *args) -> str:
                remainder = amount
                while remainder > 0 and len(self.inventory) < self.inventory_size:
                    if self.inventory != []:
                        for item in self.inventory:
                            if item.name == resource:
                                remainder = item.add(remainder)
                    if remainder > 0:
                        self.inventory.append(root.game_manager.resource_manager.create(resource, remainder)) #type: ignore
                        remainder -= self.inventory[-1].max_amount
                    self.optimize_inventory()
                return f"building '{self.name}' received {resource} in quantity {amount} and left {remainder}"
            def remove_resource(resource: str, amount: int, *args) -> str:
                for item in self.inventory:
                    if item.name == resource:
                        if item.take(amount):
                            if item.amount <= 0:
                                self.inventory.remove(item) #type: ignore
                            self.optimize_inventory()
                            return f"building '{self.name}' gave {resource} in quantity {amount}"
                return  f"building {self.name} can not give {resource}"
            def optimize_inventory(*args):
                for j, item in enumerate(self.inventory):
                    for i, item_ in enumerate(self.inventory):
                        if item.name == item_.name and i != j:
                            remainder = item.add(item_.amount)
                            if remainder == 0:
                                self.inventory.remove(item_) #type: ignore
                            else:
                                item_.amount = remainder

            self.add_resource = add_resource
            self.remove_resource = remove_resource
            self.optimize_inventory = optimize_inventory
    
    def __repr__(self) -> str:
        if self.is_default:
            return f"<Building is default>"
        else:
            return f"<Building {self.name} on coord {self.coord}>"

    def add_resource(self, *args) -> str:
        return "add resource is not definded"

    def remove_resource(self, *args) -> str:
        return "add resource is not definded"

    def optimize_inventory(self, *args):
        pass

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
        if self.get_hp() < 0:
            self.destroy()

    def can_work(self) -> bool:
        for necessary_worker_type, necessary_amount in self.necessary_workers.items():
            if self.workers.get(necessary_worker_type):
                if self.workers[necessary_worker_type] < necessary_amount:
                    return False
            else:
                return False
        return True

    def conect(self, town: Town):
        self.conected_with = town

    def deconect(self):
        self.conected_with = None
        self.workers = {}

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

    def destroy(self):
        fraction = root.game_manager.fraction_manager.get_fraction_by_id(self.fraction_id)
        fraction.statistics["building_count"] -= 1

        if self.is_town:
            fraction.statistics["town_count"] -= 1
            fraction.towns.remove(self.town)

        fraction.buildings.remove(self)

        root.game_manager.buildings_manager.remove(self.coord)
        root.game_manager.buildings_manager.build({"name": f"ruin:of_{self.name}", "desc": f"ruin_of_{self.data["desc"]}", "img": f"ruin_of_{self.data["img"]}", "type": "ruin"}, self.coord, self.fraction_id)

    def can_be_upgraded(self) -> bool:
        if self.data.get("upgrades", False):
            if self.data["upgrades"].get(str(self.level+1), False):
                return True
        return False

    def upgrade(self):
        if self.is_scheme:
            self.is_scheme = False
            self.level += 1
            for effect in self.data["upgrades"][str(self.level)]["effect"]:
                self.do_change(effect["type"], effect["args"])
            self.cell.buildings = {"name": self.data["name"], "desc": self.data["desc"], "coord": self.coord, "img": self.data["img"], "fraction_id": self.data["fraction_id"], "type": self.data["type"], "level": self.data["level"]}

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
                    if args["new_type"] == "list" and isinstance(self.inventory, dict):
                        temp_inv = self.inventory.copy()
                        self.set_inventory(self.data)
                        for inv in temp_inv:
                            for resource in inv:
                                self.inventory.append(resource) #type: ignore
                    elif args["new_type"] == "dict" and isinstance(self.inventory, list):
                        temp_inv = self.inventory.copy()
                        self.set_inventory(self.data)
                        for resource in temp_inv:
                            self.add_resource(resource.name, resource.amount)
            case "change_storage_size":
                self.inventory_size = args.get("new_size", self.inventory_size)

    def set_upgrade_mod(self, mod: bool):
        if mod:
            if self.can_be_upgraded():
                self.is_scheme = True
                self.scheme_inventory = {"cost": [root.game_manager.resource_manager.create(name, amount) for name, amount in self.data["upgrades"][str(self.level+1)]["cost"].items()], "inventory": []}
                self.scheme_inventory_size = 0
                for resource, amount in self.data["cost"].items():
                    self.scheme_inventory_size += int(amount / root.game_manager.resource_manager.get_resource_data(resource)["max_amount"]) #type: ignore
                    if amount % root.game_manager.resource_manager.get_resource_data(resource)["max_amount"] != 0:#type: ignore
                        self.scheme_inventory_size += 1
                self.scheme_inventory_size = {"cost": self.scheme_inventory_size, "inventory": self.scheme_inventory_size}

                self.name = "scheme of_" + self.name
                self.data["name"] = self.name
                self.data["scheme"] = True
                self.cell.buildings = self.data
                self.cell.resize()
            else:
                logger.error(f"Building can not be upgraded", f"Building.set_upgrade_mod({mod})")
        else:
            self.is_scheme = False

    def has_free_space(self) -> bool:
        return True

    def _determine_type(self, resource: str, type: str) -> str:
        resource_data = root.game_manager.resource_manager.get_resource_data(resource)
        if type in self.inventory.keys() and not self.is_scheme:
            return type
        elif self.is_scheme:
            if type in self.scheme_inventory:
                return type
        if resource_data:
            if "food" in self.inventory.keys() and resource_data.get("is_food", False):
                return "food"
        if "input" in self.inventory.keys() and not self.is_scheme:
            return "input"
        elif self.is_scheme and "inventory" in self.scheme_inventory.keys():
            return "inventory"
        return "none"

    def add_in_queue(self, reciept: dict|str):
        if self.is_workbench:
            if len(self.queue) <= self.max_queue:
                if isinstance(reciept, dict):
                    self.queue.append(reciept)
                else:
                    self.queue.append(root.game_manager.reciept_manager.get_reciept_by_id(reciept))

    def remove_from_queue(self, reciept:dict|str) -> str:
        if self.is_workbench:
            if isinstance(reciept, dict):
                self.queue.remove(reciept)
            else:
                reciept = root.game_manager.reciept_manager.get_reciept_by_id(reciept)
                self.queue.remove(reciept)
            return f"recipe {reciept["id"]} has been successfully removed from the queue"
        else:
            return f"ERROR: {self.name} is not workbench"
    
    def build(self):
        if self.is_scheme:
            self.name = self.name.replace("scheme of_", "")
            self.data["name"] = self.name
            self.data["img"].replace("_scheme.png", ".png")
            self.data["scheme"] = False
            self.cell.buildings = self.data
            self.cell.resize()
            if self.level == 0:
                self.upgrade()
            self.is_scheme = False
            update_gui()