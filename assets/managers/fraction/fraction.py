import random
from ...root import logger
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ..pawns.pawn import Pawn
    from ..buildings.building import Building
    from ..towns.town import Town
    from ..policy.policycard import PolicyCard

class Fraction:
    def __init__(self, name:str="New Fraction", type_:str="bot", id: int=-1, data:dict={}, is_default: bool=True):
        self.is_default = is_default
        if self.is_default:
            logger.warning("created default fraction", f"Fraction.__init__(...)")
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
        self.production = data.get("production", {"buildings": []})
        self.technologies = data.get("technologies", []) #id only
        self.policies: list[PolicyCard] = data.get("policies", []) #full policy
        self.research_technology = data.get("research_technology", "none_technology")
        self.achievements = data.get("achievements", []) #id only
        self.reciepts = data.get("reciepts", ["reciept_0", "reciept_1"]) #id only
        self.allowed_buildings =  data.get("allowed_buildings", ["manufactory"]) #id (name) only
        self.allowed_pawns = data.get("allowed_pawns", []) #id (name) only

        self.pawns: list[Pawn] = []
        self.buildings: list[Building] = []
        self.towns: list[Town] = []

    def __repr__(self) -> str:
        if not self:
            return f"<Fraction is default>"
        else:
            return f"<Fraction {self.name} with id {self.id}>"
    
    def __bool__(self) -> bool:
        return not self.is_default

    def get_base_growth_modifier(self) -> float:
        return 1 #must be difined by policy
    
    def get_adulthood_age(self) -> int:
        return 16 #must be difined by policy
    
    def get_retirement_age(self) -> int:
        return 30 #must be difined by policy
    
    def get_mortality_modifier_aged(self) -> float:
        return 1 #must be difined by policy

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