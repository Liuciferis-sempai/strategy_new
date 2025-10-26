import random
from assets.root import logger

class Fraction:
    def __init__(self, name:str="New Fraction", type_:str="bot", id: int=-1, data:dict={}, is_default: bool=True):
        self.is_default = is_default
        if self.is_default:
            logger.warning("created default fraction", f"Fraction.__init__({name}, {type_}, {id}, {data}, {is_default})")
        self.name = name
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.symbol = name[0].upper()
        self.type = type_
        self.id = id
        if data.get("statistics", False):
            self.statistics = data["statistics"]
        else:
            self.statistics = {
                "score": 0,
                "town_count": 0,
                "pawn_count": 0,
                "building_count": 0
            }
        self.production = data.get("production", {})
        self.technologies = data.get("technologies", []) #id only
        self.policies = data.get("policies", []) #full dict data
        self.research_technology = data.get("research_technology", "none_technology")
        self.achievements = data.get("achievements", []) #id only
        self.reciepts = data.get("reciepts", ["reciept_0", "reciept_1"]) #id only
        self.allowed_buildings =  data.get("allowed_buildings", ["manufactory"]) #id (name) only
        self.allowed_pawns = data.get("allowed_pawns", []) #id (name) only

    def __repr__(self) -> str:
        return f"<Fraction {self.name} with id {self.id}. Is {"not" if self.is_default else ""} default>"

    def edit(self, data:dict={}):
        if data.get("set", False):
            data.pop("set")
            for key, value in data.items():
                setattr(self, key, value)
        elif data.get("add", False):
            data.pop("add")
            for key, value in data.items():
                if hasattr(self, key):
                    if isinstance(getattr(self, key), list):
                        getattr(self, key).append(value)
                    else:
                        setattr(self, key, value)
        elif data.get("remove", False):
            data.pop("remove")
            for key, value in data.items():
                if hasattr(self, key):
                    if isinstance(getattr(self, key), list):
                        getattr(self, key).remove(value)
                    else:
                        setattr(self, key, None)