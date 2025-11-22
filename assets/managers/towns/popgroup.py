from ... import root
from random import random
import copy


class PopGroup:
    @staticmethod
    def normalize_size(size: dict) -> dict:
        """Return a dict with keys 'aged','adult','children' where values are lists of Pop objects.

        Accepts input where lists may contain ints (interpreted as ages), dicts (Pop data) or Pop instances.
        """
        result = {"aged": [], "adult": [], "children": []}
        if not isinstance(size, dict):
            return result
        for key in ("aged", "adult", "children"):
            vals = size.get(key, [])
            if isinstance(vals, int):
                # treat as count of newborns/unknown-age -> create that many default pops
                vals = [0] * vals
            if not isinstance(vals, (list, tuple)):
                continue
            for v in vals:
                if isinstance(v, Pop):
                    result[key].append(v)
                elif isinstance(v, dict):
                    result[key].append(Pop(v))
                elif isinstance(v, int):
                    result[key].append(Pop({"age": v, "gender": "male" if random() < 0.5 else "female"}))
                else:
                    # fallback: create default pop
                    result[key].append(Pop({}))
        return result

    def __init__(self, name: str, data: dict, size: dict | None = None):
        self.name = name
        normalized = PopGroup.normalize_size(size or {})
        # always store lists of Pop objects
        self.size: dict[str, list['Pop']] = {
            "aged": normalized.get("aged", []),
            "adult": normalized.get("adult", []),
            "children": normalized.get("children", [])
        }
        #print(self.size)
        self.workers = 0
        self.data = data.copy()

        self.quality: dict[str, float] = self.data.get("quality", {})
        self.base_growth = self.data.get("base_growth", 0.1)
        self.food_valued_consumption_per_person = data.get("food_valued_consumption_per_person", 0.05)

    def get_sum_population(self) -> int:
        summe = 0
        for group in self.size.values():
            summe += len(group)
        return int(summe)
    
    def get_population(self) -> dict:
        return self.size
    
    def get_necassary_food_value(self) -> float:
        return self.get_sum_population() * (self.food_valued_consumption_per_person * root.food_valued_consumption_per_person_factor)

    def get_female_count(self, group_name: str) -> int:
        if self.get_sum_population() == 0:
            return 0
        female_count = 0
        for pop in self.size.get(group_name, []):
            if pop.gender == "female":
                female_count += 1
        return female_count
    
    def new_generation(self, value: float|int):
        self.aged_get_old()
        self.adults_get_old()
        self.children_growing_up()
        for _ in range(int(value)):
            self.size["children"].append(Pop({"age": 0, "gender": "male" if random() < 0.5 else "female"}))
    
    def has_enough_quality(self, necessary_quality: dict[str, float]) -> bool:
        for n_key, n_value in necessary_quality.items():
            if self.quality.get(n_key, 0) < n_value:
                return False
        return True

    def children_growing_up(self):
        fraction = root.game_manager.fraction_manager.get_player_fraction()
        adulthood_age = fraction.get_adulthood_age() * root.year_length
        for child in self.size["children"]:
            child.age += 1
        grown = [c for c in self.size["children"] if c.age >= adulthood_age]
        if grown:
            self.size["adult"].extend(grown)
            self.size["children"] = [c for c in self.size["children"] if c.age < adulthood_age]
    
    def adults_get_old(self):
        fraction = root.game_manager.fraction_manager.get_player_fraction()
        retirement_age = fraction.get_retirement_age() * root.year_length
        for adult in self.size["adult"]:
            adult.age += 1
        to_aged = [a for a in self.size["adult"] if a.age >= retirement_age]
        if to_aged:
            self.size["aged"].extend(to_aged)
            self.size["adult"] = [a for a in self.size["adult"] if a.age < retirement_age]

    def aged_get_old(self):
        fraction = root.game_manager.fraction_manager.get_player_fraction()
        mortality_modifier_aged = fraction.get_mortality_modifier_aged()
        mortality_rate = root.base_mortality_rate_aged * mortality_modifier_aged
        survivors = []
        for aged in self.size["aged"]:
            aged.age += 1
            if random() >= mortality_rate:
                survivors.append(aged)
        self.size["aged"] = survivors
    
    def set_workers(self, value: int):
        self.workers = value
    
    def add_workers(self, value: int) -> bool:
        if self.workers + value > len(self.size["adult"]):
            return False
        else:
            self.workers += value
        return True

class Pop:
    def __init__(self, data: dict):
        self.data = copy.deepcopy(data)

        self.gender: str = self.data.get("gender", "male")
        self.age: int = self.data.get("age", 0)
    
    def __repr__(self) -> str:
        return f"<Pop {self.gender} {self.age} yo>"