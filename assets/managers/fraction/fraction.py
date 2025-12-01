import random
from ... import root
from ...root import logger
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ..pawns.pawn import Pawn
    from ..buildings.building import Building
    from ..buildings.towns.town import Town
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
        self.production: dict[str, list[Any]] = data.get("production", {"buildings": []})
        self.technologies: list[str] = data.get("technologies", []) #id only
        self.policies: list[PolicyCard] = [] #full policy
        for policy_name in data.get("policies", []):
            self.policies.append(root.game_manager.policy_table.get_policy_by_id(policy_name))
        self.research_technology: str = data.get("research_technology", "none_technology")
        self.achievements: list[str] = data.get("achievements", []) #id only
        self.reciepts: list[str] = data.get("reciepts", ["reciept_0", "reciept_1"]) #id only
        self.allowed_buildings: list[str] =  data.get("allowed_buildings", ["manufactory", "storage", "lumberjack"]) #id (name) only
        self.allowed_pawns: list[str] = data.get("allowed_pawns", []) #id (name) only

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
        mod = 1
        for policy in self.policies:
            if "pop_growth" in policy.get_influence_categories():
                mod *= policy.get_influence_values().get("pop_growth_factor", 1)*policy.get_influence_weight()
        return mod
    
    def get_adulthood_age(self) -> int:
        adulthood_ages = []
        for policy in self.policies:
            if "adulthood_age" in policy.get_influence_categories():
                new_age = policy.get_influence_values().get("adulthood_age")
                if new_age:
                    adulthood_ages.append(new_age*policy.get_influence_weight())
        if adulthood_ages:
            return sum(adulthood_ages) // len(adulthood_ages)
        else:
            return 18
    
    def get_retirement_age(self) -> int:
        retirement_ages = []
        for policy in self.policies:
            if "retirement_age" in policy.get_influence_categories():
                new_age = policy.get_influence_values().get("retirement_age")
                if new_age:
                    retirement_ages.append(new_age*policy.get_influence_weight())
        if retirement_ages:
            return sum(retirement_ages) // len(retirement_ages)
        else:
            return 65
    
    def get_mortality_modifier_aged(self) -> float:
        mod = 1
        for policy in self.policies:
            if "aged_mortality" in policy.get_influence_categories():
                mod *= policy.get_influence_values().get("aged_mortality_factor", 1)*policy.get_influence_weight()
        return mod

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