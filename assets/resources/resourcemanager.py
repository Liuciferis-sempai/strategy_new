import os
from assets.work_with_files import read_json_file
from .resource_type import ResourceType
from assets import root
from assets.functions import logging
from assets.root import loading

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
        logging("WARNING", f"Resource type '{name}' not found. Creating default resource.", "ResourceManager.create")
        return ResourceType({"name": name}, amout)

    def get_resource_data(self, resource_name: str) -> dict|None:
        for type in self.types_of_resources:
            if type["name"] == resource_name:
                return type
        return None