import os
from ...auxiliary_stuff import read_json_file
from .resource_type import ResourceType
from ... import root
from ...root import loading, logger

class ResourceManager:
    def __init__(self):
        self.types_of_resources = []

        loading.draw("Loading resources...")
        self.load_resources()

    def load_resources(self):
        self.types_of_resources = []
        for resourcefile in os.listdir("data/resources/data"):
            if resourcefile.endswith(".json"):
                type = read_json_file(f"data/resources/data/{resourcefile}")
                self.types_of_resources.append(type)

    def create(self, name:str, amout:int=0) -> ResourceType:
        for type in self.types_of_resources:
            if type["name"] == name:
                return ResourceType(type, amout)
        logger.warning(f"Resource type '{name}' not found. Creating default resource.", f"ResourceManager.create({name}, {amout})")
        return ResourceType({"name": name}, amout)

    def get_resource_data(self, resource_name: str) -> dict|None:
        for type in self.types_of_resources:
            if type["name"] == resource_name:
                return type
        return None