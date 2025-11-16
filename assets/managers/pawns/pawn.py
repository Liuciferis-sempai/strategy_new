import pygame as py
import root
from root import logger

class Pawn:
    def __init__(self, id: int= -1, coord: tuple[int, int, int]=(0, 0, 0), data: dict= {}, is_default: bool=True):
        self.is_default = is_default
        if is_default:
            logger.warning("created default pawn", f"Pawn.__init__(...)")
        self.id = id
        self.coord = coord
        
        self.inventory_size = data.get("inventory_size", 1)
        self.inventory = []
        self.data = data.copy()

        self.name = data.get("name", data.get("type", "unknow"))
        self.type = data.get("type", "unknow")
        self.fraction_id = data.get("fraction_id", -1)
        self.category = data.get("category", "unknown")
        self.hp = data.get("max_hp", 50)
        self.hp_mod = data.get("hp_mod", {})
        self.max_hp = data.get("max_hp", 50)
        self.max_hp_mod = data.get("hp_mod", {})
        self.attack = data.get("attack", {"type": "none", "distance": 0, "damage": 0, "mods": []})
    
    def __repr__(self) -> str:
        if not self:
            return f"<Pawn is default>"
        else:
            return f"<Pawn {self.type} with id {self.id} on coord {self.coord}>"
    
    def __bool__(self) -> bool:
        return not self.is_default
    
    def add_resource(self, resource:str, amout:int):
        if len(self.inventory) < self.inventory_size:
            remainder = amout
            if self.inventory != []:
                for item in self.inventory:
                    if item.name == resource:
                        remainder = item.add(amout)
            if remainder > 0:
                self.inventory.append(root.game_manager.resource_manager.create(resource, remainder))
            self.optimize_inventory()
    
    def remove_resource(self, resource:str, amout:int) -> bool:
        for item in self.inventory:
            if item.name == resource:
                if item.take(amout):
                    if item.amout <= 0:
                        self.inventory.remove(item)
                    self.optimize_inventory()
                    return True
        return False
    
    def optimize_inventory(self):
        for j, item in enumerate(self.inventory):
            for i, item_ in enumerate(self.inventory):
                if item.name == item_.name and i != j:
                    remainder = item.add(item_.amout)
                    if remainder == 0:
                        self.inventory.remove(item_)
                    else:
                        item_.amout = remainder

    def has_free_space(self) -> bool:
        return len(self.inventory) < self.inventory_size
    
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
    
    def take_damage(self, damage: int):
        self.hp -= damage
        if self.get_hp() < 0:
            self.destroy()
    
    def destroy(self):
        root.game_manager.pawns_manager.despawn(self.id)

    def attacked(self, attack: dict) -> str:
        self.take_damage(attack["damage"])
        return f"{self} taked {attack["damage"]} damage"