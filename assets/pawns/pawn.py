import pygame as py
from assets import root
from assets.functions import logging

class Pawn:
    def __init__(self, id: int= -1, coord: tuple[int, int]=(0, 0), data: dict= {}, is_default: bool=True):
        self.is_default = is_default
        if is_default:
            logging("WARNING", "created default pawn", "Pawn.__init__", f"id: {id}, coord: {coord}, data: {data}")
        self.id = id
        self.coord = coord
        self.fraction_id = data.get("fraction_id", -1)
        self.type = data.get("type", "unknown")
        self.inventory_size = data.get("inventory_size", 1)
        self.inventory = []
        self.data = data
    
    def __repr__(self) -> str:
        return f"<Pawn {self.type} with id {self.id} on coord {self.coord}. Is {"not" if not self.is_default else ""} default>"
    
    def add_resource(self, resource:str, amout:int):
        if len(self.inventory) < self.inventory_size:
            remainder = amout
            if self.inventory != []:
                for item in self.inventory:
                    if item.name == resource:
                        remainder = item.add(amout)
            if remainder > 0:
                self.inventory.append(root.handler.resource_manager.create(resource, remainder))
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