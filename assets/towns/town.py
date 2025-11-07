import assets.root as root
from assets.root import logger
from .popgroup import PopGroup
import math
import matplotlib.pyplot as plt

class Town:
    def __init__(self, id: int = -1, name: str = "Unknow", coord: tuple[int, int] = (-1, -1), fraction_id: int = -1, data: dict = {}, is_default: bool = True):
        self.id = id
        self.name = name
        self.coord: tuple[int, int] = coord
        self.is_default = is_default
        if is_default:
            logger.error("created default town", f"Town.__init__({name}, {coord}, {fraction_id}, {data}, {is_default})")
        self.data = data.copy()

        self.fraction_id = fraction_id
        
        self.popgroups: list[PopGroup] = []
        for popgroup in data.get("popgroups", ["peasants", "workers", "educated"]):
            self.append_popgroup(popgroup)
        self.conection_lenght = 2
        from assets.buildings.building import Building
        self.conection: list[Building] = []
        self.check_conection()

        self.population_history: dict[str, list[float]] = {}
        for popgroup in self.popgroups:
            self.population_history[popgroup.name] = [popgroup.get_population()]

    def __repr__(self):
        if self.is_default:
            return f"<Town is default>"
        else:
            return f"<Town {self.name} at {self.coord} | pop: {self.get_sum_population()}>"

    def check_conection(self):
        self.conection = []
        cells = root.game_manager.world_map.get_travel_region(self.coord, self.conection_lenght, True)
        for cell, _ in cells.values():
            if cell.buildings != {}:
                if cell.buildings["fraction_id"] == root.player_id:
                    self.conection.append(root.game_manager.buildings_manager.get_building_by_coord(cell.coord))

    def append_popgroup(self, new_popgroup: str|dict):
        if isinstance(new_popgroup, dict):
            for popgroup in self.popgroups:
                if popgroup.name == new_popgroup["name"]:
                    return
            self.popgroups.append(PopGroup(new_popgroup["name"], new_popgroup, new_popgroup.get("size", 10)))
        else:
            for popgroup in self.popgroups:
                if popgroup.name == new_popgroup:
                    return
            self.popgroups.append(root.game_manager.town_manager.create_pop_group(new_popgroup))

    def simulation(self):
        fraction = root.game_manager.fraction_manager.get_fraction_by_id(self.fraction_id)
        #logger.info(f"{self} need {necessary_food_value} food and have has access to {food_value}", "Town.simulation()")

        food_sufficiency_factor = self.get_food_sufficiency_factor()
        self.consume_food()

        base_policy_growth_modifier = fraction.get_base_growth_modifier()

        time_factor = 1 / root.year_length
        for popgroup in self.popgroups:
            growth_factor = popgroup.base_growth * base_policy_growth_modifier * food_sufficiency_factor
            #print(popgroup.base_growth * base_policy_growth_modifier * food_sufficiency_factor, popgroup.base_growth, base_policy_growth_modifier, food_sufficiency_factor)
            growth_rate_per_turn = (1 + growth_factor) ** time_factor - 1
            #print(growth_rate_per_turn)
            #logger.info(f"{popgroup.name} in {self} growth up on {growth_rate_per_turn} rate ({popgroup.size * growth_rate_per_turn})", "Town.simulation()")
            popgroup.add_new_children(popgroup.size["adult"]/2 * growth_rate_per_turn)
            self.add_in_population_history(popgroup.name, popgroup.get_population())
            if popgroup.get_population() < 1:
                self.remove_popgroup(popgroup.name)

    def add_in_population_history(self, popgroup_name: str, popgroup_population: float):
        self.population_history[popgroup_name].append(popgroup_population)

    def show_statistic(self):
        for popgroup in self.population_history:
            plt.plot([i for i in range(len(self.population_history[popgroup]))], self.population_history[popgroup], "-o", label=f"{popgroup}")
        plt.legend()
        plt.grid()
        plt.show()

    def get_food_sufficiency_factor(self) -> float:
        self_building = root.game_manager.buildings_manager.get_building_by_coord(self.coord)
        
        food_value = self_building.get_food_value_in_storage()
        for building in self.conection:
            if building.type == "storage":
                food_value += building.get_food_value_in_storage()
        necessary_food_value = self.get_necessaty_food_value()

        food_ratio = food_value / necessary_food_value
        sigmoid = 1 / (1 + math.exp(-3 * (food_ratio - root.food_sufficiency_factor_center)))
        #print("r", food_ratio, food_value, round(necessary_food_value, 4))
        #print("s", sigmoid)
        #if food_ratio < 0.6:
        #    return 0
        return root.food_sufficiency_factor_frame[0] + (root.food_sufficiency_factor_frame[1] - root.food_sufficiency_factor_frame[0]) * sigmoid

    def get_necessaty_food_value(self) -> float:
        time_factor = 1 / root.year_length
        necessary_food_value = 0
        for popgroup in self.popgroups:
            necessary_food_value += popgroup.get_necassary_food_value()
        return (1 + necessary_food_value) ** time_factor - 1

    def consume_food(self, necessary_food_value: float = 0):
        if necessary_food_value == 0:
            necessary_food_value = self.get_necessaty_food_value()
        self_building = root.game_manager.buildings_manager.get_building_by_coord(self.coord)
        necessary_food_value = self_building.remove_food_for_value(necessary_food_value)
        if necessary_food_value > 0:
            for building in self.conection:
                if building.type == "storage":
                    necessary_food_value = building.remove_food_for_value(necessary_food_value)

    def get_sum_population(self) -> int:
        population = 0
        for popgroup in self.popgroups:
            population += popgroup.get_population()
        return population
    
    def get_population(self) -> dict:
        population = {}
        for popgroup in self.popgroups:
            population[popgroup.name] = popgroup.get_population()
        return population
    
    def remove_popgroup(self, popgroup_name: str):
        for popgroup in self.popgroups:
            if popgroup.name == popgroup_name:
                self.popgroups.remove(popgroup)