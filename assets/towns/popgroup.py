import assets.root as root

class PopGroup:
    def __init__(self, name: str, data: dict, size: dict = {}):
        self.name = name
        self.size = {
            "aged": size.get("aged", 1),
            "adult": size.get("adult", 10),
            "children": size.get("children", 2)
        }
        self.children_groups = []
        self.data = data.copy()

        self.education = self.data.get("education", 0.2)
        self.base_growth = self.data.get("base_growth", 0.1)
        self.food_valued_consumption_per_person = data.get("food_valued_consumption_per_person", 0.05)

    def get_population(self) -> int:
        return int(sum(self.size.values()))
    
    def get_necassary_food_value(self) -> float:
        return self.get_population() * (self.food_valued_consumption_per_person * root.food_valued_consumption_per_person_factor)
    
    def add_new_children(self, value: float|int):
        self.size["children"] += value
        self.children_groups.append(value)
        
        self.children_growing_up()

    def children_growing_up(self):
        fraction = root.game_manager.fraction_manager.get_player_fraction()
        while len(self.children_groups) >= fraction.get_adulthood_age() * root.year_length:
            children_group = self.children_groups.pop(0)
            self.size["children"] -= children_group
            self.size["adult"] += children_group