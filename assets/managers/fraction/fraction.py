import random
from ... import root
from ...root import logger
from typing import Any, TYPE_CHECKING
from ...auxiliary_stuff import *
from ...gui.contentbox import ContentBox

if TYPE_CHECKING:
    from ..pawns.pawn import Pawn
    from ..buildings.building import Building
    from ..buildings.towns.town import Town
    from ..policy.policycard import PolicyCard
from ..technologies.techtree import Techtree

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
        self.production: list[Building] = data.get("production", [])
        self.policies: list[PolicyCard] = [] #full policy
        for policy_name in data.get("policies", []):
            self.policies.append(root.game_manager.policy_table.get_policy_by_id(policy_name))

        self.techs: Techtree = root.game_manager.technology_manager.create_techtree(data.get("tech_tree", []), self.id) if has(root, "game_manager") else Techtree([], self.id)
        self.research_technology = data.get("research_technology", "none_tech")
        self.researched_technology: list[str] = data.get("researched_technology", [])

        self.science: dict[str, int] = data.get("science", {})
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
    
    def use_science(self):
        if self.research_technology == "none_tech":
            for science in root.game_manager.gui.game.science_contentboxes:
                science.set_value(0)
            return

        tech = self.techs.get_tech(self.research_technology)
        for science, amount in self.science.items():
            if not has(tech.accumulated, science): continue
            tech.accumulated[science] += amount
            if self.id == root.player_id:
                if has(root.game_manager.gui.game, science):
                    getattr(root.game_manager.gui.game, science).set_value(amount)
                else:
                    science_content_box = ContentBox(position=(10, 10), value=amount, allowed_range=[0, 9999])
                    setattr(root.game_manager.gui.game, science, science_content_box)
                    root.game_manager.gui.game.header_info_content.insert(1, science_content_box)
                    update_gui()
        for science, amount in tech.cost.items():
            if tech.accumulated[science] < amount:
                return
        root.game_manager.technology_manager.reseach_technology(tech.id, self.id)

    def set_science(self, science_type: str, value: int):
        self.science[science_type] = value

    def add_science(self, science_type: str, science_amount: int):
        if not has(self.science, science_type):
            self.science[science_type] = 0
        self.science[science_type] += science_amount

    def set_research_technology(self, technology_id: str):
        self.research_technology = technology_id
        self.science = {}

    def reset_research_technology(self):
        self.research_technology = "none_tech"

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