import assets.root as root
from assets.root import logger
from .popgroup import PopGroup
import math
import matplotlib.pyplot as plt

class Town:
    def __init__(self, id: int = -1, name: str = "Unknow", coord: tuple[int, int, int] = (-1, -1, 0), fraction_id: int = -1, data: dict = {}, is_default: bool = True):
        self.id = id
        self.name = name
        self.coord: tuple[int, int, int] = coord
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
            self.population_history[popgroup.name] = [popgroup.get_sum_population()]

    def __repr__(self):
        if not self:
            return f"<Town is default>"
        else:
            return f"<Town {self.name} at {self.coord} | pop: {self.get_sum_population()}>"
    
    def __bool__(self) -> bool:
        return not self.is_default
    
    def destroy(self):
        for building in self.conection:
            building.deconect()

    def check_conection(self):
        for conection in self.conection:
            conection.deconect()
        self.conection = []
        for group in self.popgroups:
            group.set_workers(0)
        cells = root.game_manager.world_map.get_travel_region(self.coord, self.conection_lenght, root.player_id==self.fraction_id)
        for cell, _ in cells.values():
            if cell.buildings != {} and cell.coord != self.coord:
                if cell.buildings["fraction_id"] == self.fraction_id:
                    building = root.game_manager.buildings_manager.get_building_by_coord(cell.coord)
                    self.conection.append(building)
                    building.conect(self)

    def append_popgroup(self, new_popgroup: str|dict):
        if isinstance(new_popgroup, dict):
            for popgroup in self.popgroups:
                if popgroup.name == new_popgroup["name"]:
                    return
            self.popgroups.append(PopGroup(new_popgroup["name"], new_popgroup, new_popgroup.get("size", {"aged": [1], "adult": [2, 5, 3], "children": [2]})))
        else:
            for popgroup in self.popgroups:
                if popgroup.name == new_popgroup:
                    return
            self.popgroups.append(root.game_manager.town_manager.create_pop_group(new_popgroup))
        
    def add_population(self, new_popgroup: str, popsize: dict) -> str:
        for popgroup in self.popgroups:
            if popgroup.name == new_popgroup:
                popgroup.size["adult"] += popsize.get("adult", 0)
                popgroup.size["aged"] += popsize.get("aged", 0)
                if popsize.get("children"):
                    popgroup.new_generation(popsize["children"])
                return f"successfully added new population to {self}"
        self.append_popgroup({"name": new_popgroup, "size": popsize})
        return f"successfully added new population to {self}"
    
    def remove_population(self, new_popgroup: str, popsize: dict|str) -> str:
        if isinstance(popsize, dict):
            for popgroup in self.popgroups:
                if popgroup.name == new_popgroup:
                    popgroup.size["adult"] -= popsize.get("adult", 0)
                    popgroup.size["aged"] -= popsize.get("aged", 0)
                    popgroup.size["children"] -= popsize.get("children", 0)
                    if popgroup.size["adult"] < 0 or popgroup.size["aged"] < 0 or popgroup.size["children"]:
                        self.remove_popgroup(popgroup.name)
                    return f"successfully removed population from {self}"
        elif popsize == "all":
            self.remove_popgroup(new_popgroup)
            return f"successfully removed population from {self}"
        return f"can not remov population from {self}"

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
            popgroup.new_generation(sum(popgroup.size["adult"])/2 * growth_rate_per_turn)
            self.add_in_population_history(popgroup.name, popgroup.get_sum_population())

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
            if building.category == "storage":
                food_value += building.get_food_value_in_storage()
        necessary_food_value = self.get_necessaty_food_value()

        if necessary_food_value == 0: return 0

        food_ratio = food_value / necessary_food_value
        if food_ratio == 0: return root.food_sufficiency_factor_frame[0]
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
                if building.category == "storage":
                    necessary_food_value = building.remove_food_for_value(necessary_food_value)
                if necessary_food_value <= 0:
                    return
    
    def spawn(self, pawn_type: str):
        building = root.game_manager.buildings_manager.get_building_by_coord(self.coord)
        pawn_sample = root.game_manager.pawns_manager.get_pawn_sample_by_type(pawn_type)
        if len(building.queue) < building.max_queue:
            time = pawn_sample["cost"]["time"] // building.data["speed_of_work_mod"]
            if time < 0:
                time = 1
            building.add_in_queue(pawn_sample)
            root.game_manager.turn_manager.add_event_in_queue(time, {"do": "spawn", "event_data": {"type": pawn_type, "coord": self.coord, "fraction_id": self.fraction_id}})
            root.game_manager.turn_manager.add_event_in_queue(time, {"do": "clear_the_queue", "event_data": {"building": building, "reciept": pawn_sample}})

    def get_sum_population(self) -> int:
        population = 0
        for popgroup in self.popgroups:
            population += popgroup.get_sum_population()
        return population
    
    def get_population(self) -> dict:
        population = {}
        for popgroup in self.popgroups:
            population[popgroup.name] = popgroup.get_sum_population()
        return population
    
    def get_popgroup(self, popgroup_name: str) -> PopGroup|None:
        for popgroup in self.popgroups:
            if popgroup.name == popgroup_name:
                return popgroup
        return None
    
    def remove_popgroup(self, popgroup_name: str):
        for popgroup in self.popgroups:
            if popgroup.name == popgroup_name:
                self.popgroups.remove(popgroup)