import pygame as py
import os
from .. import root
from ..root import logger, read_json_file
import copy
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..gamemanager import GameManager

from .buildings.producer.producer import Producer

class ProducerManager:
    def __init__(self, game_manager: "GameManager"):
        self.game_manager = game_manager

        self.producers = []
        self.bloocked_producer_ids: list[int] = []

    def build_producer(self, id: int, producer_type: Producer|None, coord: tuple[int, int, int], fraction_id: int, building_data: dict = {}) -> Producer:
        if id not in self.bloocked_producer_ids and id >= 0: self.bloocked_producer_ids.append(id)
        else: return self.build_producer(id+1,producer_type, coord, fraction_id, building_data)
    
        if not producer_type:
            producer = Producer(id=id, coord=coord, fraction_id=fraction_id, data=None, building_data=building_data, is_default=False)
        else:
            producer = producer_type
        
        self.producers.append(producer)
        return producer
    
    def remove_producer(self, producer: Producer) -> bool:
        if producer in self.producers:
            self.producers.remove(producer)
            producer.destroy()
            return True
        return False