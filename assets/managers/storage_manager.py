import pygame as py
import os
from .. import root
from ..root import logger, read_json_file
import copy
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..gamemanager import GameManager

from .buildings.storages.storage import Storage

class StorageManager:
    def __init__(self, game_manager: "GameManager"):
        self.game_manager = game_manager

        self.storages: list[Storage] = []
        self.bloocked_storage_ids: list[int] = []

    def build_storage(self, id: int, storage_type: Storage|None, coord: tuple[int, int, int], fraction_id: int, building_data: dict = {}) -> Storage:
        if id not in self.bloocked_storage_ids and id >= 0: self.bloocked_storage_ids.append(id)
        else: return self.build_storage(id+1, storage_type, coord, fraction_id)
    
        if not storage_type:
            storage = Storage(id, coord, fraction_id, building_data, is_default=False)
        else:
            storage = storage_type
        
        self.storages.append(storage)
        return storage
    
    def remove_storage(self, storage: Storage) -> bool:
        if storage in self.storages:
            self.storages.remove(storage)
            storage.destroy()
            return True
        return False
    
    def check_conection(self, fraction_id: int):
        for storage in self.storages:
            if storage.fraction_id == fraction_id:
                storage.check_conection()

    def turn(self):
        for storage in self.storages:
            storage.turn()