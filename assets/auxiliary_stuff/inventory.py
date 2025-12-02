from .. import root
from ..managers.resources.resource_type import ResourceType

class Inventory:
    def __init__(self, inv_max_size: int|dict, inv_self: list|dict, default_inv_cat: str = "main"):
        self.inventory: dict[str, list[ResourceType]] = {}
        self.inv_max_size: dict[str, int] = {}
        self.default_inv_cat = default_inv_cat
        if isinstance(inv_self, dict) and isinstance(inv_max_size, dict):
            for key in inv_self.keys():
                self.inventory[key] = inv_self[key]
                self.inv_max_size[key] = inv_max_size[key]
        elif isinstance(inv_self, list) and isinstance(inv_max_size, int):
            self.inventory = {"main": inv_self}
            self.inv_max_size["main"] = inv_max_size
        else:
            self.inventory = {"main": []}
            self.inv_max_size["main"] = 1
            root.logger.error("false inventory type", f"Inventory.__init__({inv_max_size}, {inv_self}, {default_inv_cat})")
    
    def add_resouce(self, resource_name: str = "unknow", resource_amount: int = 0, resource: ResourceType|None = None, inv_type: str = "main") -> str:
        inv = self._get_inv_type(inv_type)
        
        if resource:
            for cat in inv:
                while len(self.inventory[cat]) < self.inv_max_size[cat]:
                    self.inventory[cat].append(resource)
                    self._optimize_inventory()
                    return f"added resource {resource.name} to inventory"
            return f"can not add resource {resource.name}"

        remainder = resource_amount
        for cat in inv:
            for item in self.inventory[cat]:
                if item.name == resource_name:
                    remainder = item.add(remainder)
                    if remainder <= 0: return f"added resource {resource_name} to inventory in amount {resource_amount}"
        
        for cat in inv:
            while len(self.inventory[cat]) < self.inv_max_size[cat]:
                self.inventory[cat].append(root.game_manager.resource_manager.create(resource_name, remainder))
                remainder -= self.inventory[cat][-1].get_max_amount()
                if remainder <= 0: return f"added resource {resource_name} to inventory in amount {resource_amount}"
        
        root.logger.warning("must add more resources as can", f"Inventory.add_resouce({resource_name}, {resource_amount}, {resource})")
        if remainder < resource_amount:
            return f"added resource {resource_name} to inventory in amount {remainder} and {resource_amount-remainder} lost"
        else:
            return f"can not add {resource_name} to invnentory"

    def remove_resource(self, resource_name: str = "unknow", resource_amount: int = 0, resource: ResourceType|None = None, inv_type: str = "main") -> str:
        inv = self._get_inv_type(inv_type)

        if resource:
            for cat in inv:
                if resource in self.inventory[cat]:
                    self.inventory[cat].remove(resource)
                    return f"removed resource {resource.name} to inventory"
            for cat in inv:
                for res in self.inventory[cat]:
                    if res.is_equal(resource):
                        self.inventory[cat].remove(res)
            return f"can not remove resource {resource.name}"

        remainder = resource_amount
        for cat in inv:
            for item in self.inventory[cat]:
                if item.name == resource_name:
                    remainder -= item.take(remainder)
                    if remainder <= 0:
                        self._optimize_inventory()
                        return f"removed {resource_amount} {resource_name}"
        
        root.logger.error("must remove more resources as own", f"Inventory.remove_resource({resource_name}, {resource_amount}, {resource})")
        if remainder == resource_amount:
            return f"removed {resource_amount-remainder} {resource_name}"
        else:
            return f"can not remove {resource_name}"

    def get_resource(self, resource_name: str, resource_amount: int|str = "all", category: str = "main", with_remove: bool = False) -> ResourceType|None:
        inv_type = self._get_inv_type(category)
        resource = None
        org_item = None
        resource_inv = "none"

        for inv in inv_type:
            for item in self.inventory[inv]:
                if item.name == resource_name:
                    org_item = item
                    resource = item.copy()
                    resource_inv = inv
                    break

        if with_remove and resource and org_item:
            if resource_amount == "all" or (isinstance(resource_amount, int) and org_item.amount <= resource_amount):
                self.inventory[resource_inv].remove(org_item)
            elif isinstance(resource_amount, int):
                org_item.take(resource_amount)
                resource.amount = resource_amount
            self._optimize_inventory()

        return resource

    def has_resource(self, resource_name: str = "unknow", resource_amount: int = 0, resource: ResourceType|None = None, inv_type: str = "main") -> bool:
        inv = self._get_inv_type(inv_type)

        remainder = resource_amount
        for cat in inv:
            for item in self.inventory[cat]:
                if item.name == resource_name:
                    remainder -= item.amount
                    if remainder <= 0: return True
        return False
    
    def content_to_dict(self) -> dict[str, list[ResourceType]]:
        content = {}
        for cat in self.inventory:
            content[cat] = self.inventory[cat]
        return content

    def content_to_list(self, inv_type: str = "main") -> list[ResourceType]:
        if inv_type in self.inventory.keys():
            return self.inventory[inv_type]
        return self.inventory[self.default_inv_cat]
    
    def size_to_dict(self) -> dict[str, int]:
        return self.inv_max_size

    def _get_inv_type(self, inv_type: str) -> list[str]:
        if inv_type in [key for key in self.inventory.keys()]:
            return [inv_type]
        elif self.default_inv_cat == "none":
            return []
        elif inv_type == "any":
            return [key for key in self.inventory.keys()]
        elif inv_type == "main" or inv_type not in [key for key in self.inventory.keys()]:
            return [self.default_inv_cat]
        else:
            return [inv_type]
        
    def _optimize_inventory(self):
        to_remove = []
        for inv in self.inventory:
            for i, item1 in enumerate(self.inventory[inv]):
                if item1.amount == item1.get_max_amount():
                    continue
                elif item1.amount == 0:
                    if item1 not in to_remove: to_remove.append((item1, inv))
                    continue
                elif (item1, inv) in to_remove:
                    continue

                for j, item2 in enumerate(self.inventory[inv]):
                    if (item2, inv) in to_remove: continue
                    if item1.name == item2.name and i != j and item2.amount != item2.get_max_amount():
                        if item2.amount > 0:
                            remainder = item1.add(item2.amount)
                            if remainder == 0:
                                to_remove.append((item2, inv))
                            else:
                                item2.take(remainder)
                        elif item2 not in to_remove:
                            to_remove.append((item2, inv))

        for item, inv in to_remove:
            self.inventory[inv].remove(item)
    
    def get_inventory(self, inventory_category: str) -> list[ResourceType]:
        if inventory_category in self.inventory.keys():
            return self.inventory[inventory_category]
        else:
            return []