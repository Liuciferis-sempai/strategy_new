import root
from random import random

class PopGroup:
    def __init__(self, name: str, data: dict, size: dict = {}):
        self.name = name
        self.size: dict[str, list[float|int]] = {
            "aged": size.get("aged", [0]),
            "adult": size.get("adult", [0]),
            "children": size.get("children", [0])
        }
        self.workers = 0
        self.data = data.copy()

        self.quality: dict[str, float] = self.data.get("quality", {})
        self.base_growth = self.data.get("base_growth", 0.1)
        self.food_valued_consumption_per_person = data.get("food_valued_consumption_per_person", 0.05)

    def get_sum_population(self) -> int:
        summe = 0
        for group in self.size.values():
            summe += sum(group)
        return int(summe)
    
    def get_population(self) -> dict:
        return self.size
    
    def get_necassary_food_value(self) -> float:
        return self.get_sum_population() * (self.food_valued_consumption_per_person * root.food_valued_consumption_per_person_factor)
    
    def new_generation(self, value: float|int):
        self.size["children"].append(value)
        self.children_growing_up()
        self.adults_get_old()
        self.aged_get_old()
    
    def has_enough_quality(self, necessary_quality: dict[str, float]) -> bool:
        for n_key, n_value in necessary_quality.items():
            if self.quality.get(n_key, 0) < n_value:
                return False
        return True

    def children_growing_up(self):
        fraction = root.game_manager.fraction_manager.get_player_fraction()
        while len(self.size["children"]) >= fraction.get_adulthood_age() * root.year_length:
            children = self.size["children"].pop(0)
            self.size["adult"].append(children)
    
    def adults_get_old(self):
        fraction = root.game_manager.fraction_manager.get_player_fraction()
        while len(self.size["adult"]) >= fraction.get_retirement_age() * root.year_length:
            adult = self.size["adult"].pop(0)
            self.size["aged"].append(adult)

    def aged_get_old(self):
        fraction = root.game_manager.fraction_manager.get_player_fraction()
        for i, _ in enumerate(self.size["aged"]):
            death_chance = root.base_mortality_rate_aged * fraction.get_mortality_modifier_aged()
            if death_chance < random():
                self.size["aged"].pop(i)
    
    def set_workers(self, value: int):
        self.workers = value
    
    def add_workers(self, value: int) -> bool:
        if self.workers + value > sum(self.size["adult"]):
            return False
        else:
            self.workers += value
        return True