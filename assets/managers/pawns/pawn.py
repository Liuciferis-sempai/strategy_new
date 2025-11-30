import pygame as py
from ... import root
from ...root import logger, language
from ...auxiliary_stuff import *

class Pawn:
    def __init__(self, id: int= -1, coord: tuple[int, int, int]=(0, 0, 0), data: dict= {}, is_default: bool=True):
        self.is_default = is_default
        if is_default:
            logger.warning("created default pawn", f"Pawn.__init__(...)")
        self.id = id
        self.coord = coord
        
        self.inventory = Inventory(data.get("inventory_size", 1), data.get("inventory", []), "main")
        self.data = data.copy()

        self.name = language.get(data.get("name", data.get("type", "unknow")))
        self.type = data.get("type", "unknow")
        self.fraction_id = data.get("fraction_id", -1)
        self.category = data.get("category", "unknown")
        self.hp = data.get("max_hp", 50)
        self.hp_mod = data.get("hp_mod", {})
        self.max_hp = data.get("max_hp", 50)
        self.max_hp_mod = data.get("hp_mod", {})
        self.attack = data.get("attack", {"type": "none", "distance": 0, "damage": 0, "mods": []})

        self.has_job_to_res_movment_points = data.get("has_job_to_res_movment_points", None)
    
    def __repr__(self) -> str:
        if not self:
            return f"<Pawn is default>"
        else:
            return f"<Pawn {self.type} with id {self.id} on coord {self.coord}>"
    
    def __bool__(self) -> bool:
        return not self.is_default
    
    def add_resource(self, resource:str, amount:int):
        return self.inventory.add_resouce(resource, amount)
    
    def remove_resource(self, resource:str, amount:int):
        return self.inventory.remove_resource(resource, amount)

    def has_free_space(self) -> bool:
        return True
    
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