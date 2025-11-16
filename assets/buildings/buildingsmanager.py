import os
from assets.auxiliary_stuff import read_json_file
from .building import Building
from assets import root
from assets.world.cell import Cell
from assets.root import loading, logger

class BuildingsManager:
    def __init__(self):
        self._default_building: Building = Building()
         
        self.buildings: dict[str, Building] = {}
        self.types_of_buildings: list[dict] = []
        self.names: list[str] = []

        loading.draw("Loading building types...")
        self.load_types_of_buildings()

    def load_types_of_buildings(self):
        self.types_of_buildings = []
        for buildingsfile in os.listdir("data/buildings/data"):
            if buildingsfile.endswith(".json"):
                type = read_json_file(f"data/buildings/data/{buildingsfile}")
                self.types_of_buildings.append(type)
        self.names = []
        for building in self.types_of_buildings:
            self.names.append(building.get("name", "unknow"))

    def build(self, data: str|dict, coord: tuple[int, int, int], fraction_id: int) -> bool:
        '''
        use data str to build standart building
        use data dict to build building with specials characteristics
        '''
        #print(self.types_of_buildings)
        if not self.buildings.get(str(coord), False):
            for type in self.types_of_buildings:
                if isinstance(data, dict):
                    self._build(data, coord, fraction_id)
                    return True
                elif data == type["name"]:
                    self._build(type, coord, fraction_id)
                    return True
        elif "scheme" in self.buildings[str(coord)].name:
                    self.buildings[str(coord)].build()
                    return True
        return False
    
    def build_scheme(self, data: str|dict, coord: tuple[int, int, int], fraction_id: int) -> bool:
        '''
        use data str to build standart building
        use data dict to build building with specials characteristics
        '''
        if not self.buildings.get(str(coord), False):
            for type in self.types_of_buildings:
                if data == type["name"] or data == type:
                    if isinstance(data, str):
                        self._build_scheme(type, coord, fraction_id)
                    else:
                        self._build_scheme(data, coord, fraction_id)
                    return True
        return False
    
    def _build_scheme(self, data: dict, coord: tuple[int, int, int], fraction_id: int):
        data = data.copy()

        data["fraction_id"] = fraction_id
        data["name"] = "scheme" + ":of_" + data["name"]
        data["img"] = data["img"].replace(".png", "_scheme.png")
        data["scheme"] = True
        cell = root.game_manager.world_map.get_cell_by_coord(coord)
        building = Building(coord, cell, data.copy(), False)
        self.buildings[str(coord)] = building

        cell.add_building({"name": data["name"], "desc": data["desc"], "coord": coord, "img": data["img"], "fraction_id": data["fraction_id"], "type": data["type"], "level": data["level"]})
        self._add_to_fraction(building, fraction_id)

    def _build(self, data: dict, coord: tuple[int, int, int], fraction_id: int):
        data = data.copy()

        data["fraction_id"] = fraction_id
        cell = root.game_manager.world_map.get_cell_by_coord(coord)
        building = Building(coord, cell, data, False)
        self.buildings[str(coord)] = building

        cell.add_building({"name": data["name"], "desc": data["desc"], "coord": coord, "img": data["img"], "fraction_id": data["fraction_id"], "type": data["type"], "level": data["level"]})
        self._add_to_fraction(building, fraction_id)
        
        fraction = root.game_manager.fraction_manager.get_fraction_by_id(fraction_id)
        for town in fraction.towns:
            town.check_conection()

    def remove(self, coord: tuple[int, int, int]):
        building = self.buildings[str(coord)]

        self._remove_from_fraction(building, building.fraction_id)

        self.buildings.pop(str(coord))
        cell = root.game_manager.world_map.get_cell_by_coord(coord)
        cell.remove_building()

    def _add_to_fraction(self, building: Building, fraction_id: int):
        fraction = root.game_manager.fraction_manager.get_fraction_by_id(fraction_id)
        fraction.statistics["building_count"] += 1
        fraction.buildings.append(building)
        if building.category == "producer":
            fraction.production["buildings"].append(building)
    
    def _remove_from_fraction(self, building: Building, fraction_id: int):
        fraction = root.game_manager.fraction_manager.get_fraction_by_id(fraction_id)
        fraction.statistics["building_count"] -= 1 #type: ignore
        fraction.buildings.remove(building)
        if building.is_town:
            fraction.statistics["town_count"] -= 1
            fraction.towns.remove(building.town)
            building.town.destroy()
        if building.category == "producer":
            fraction.production["buildings"].remove(building)

    def get_building_by_coord(self, coord:tuple[int, int, int]) -> Building:
        #print(self.buildings)
        #print(self.buildings[str(coord)])
        try:
            return self.buildings[str(coord)]
        except:
            return self._default_building
        
    def get_building_in_area(self, start_coord: tuple[int, int], end_coord: tuple[int, int], center_coord: tuple[int, int] = (-1, -1)) -> list:
        buildings = []
        for nx in range(start_coord[0], end_coord[0]):
            for ny in range(start_coord[1], end_coord[1]):
                if (nx, ny) != (center_coord[0], center_coord[1]):
                    if self.buildings.get(str((nx, ny))):
                        buildings.append(self.buildings[str((nx, ny))])
        return buildings
    
    def get_all_possible_buildings_names(self) -> list[str]:
        return self.names
        
    def get_all_unique_buildings_sorted_by_types(self, only_allowed_for_players_fraction: bool=True) -> dict:
        buildings_by_types = {}
        uniqu_buildings = []
        if only_allowed_for_players_fraction:
            player_fraction = root.game_manager.fraction_manager.get_player_fraction()
            if not player_fraction:
                logger.error("No player fraction found in get_all_buildings_sorted_by_types", f"BuildingsManager.get_all_buildings_sorted_by_types({only_allowed_for_players_fraction})")
                return buildings_by_types

        for building in self.buildings.values():
            if only_allowed_for_players_fraction:
                if building.type not in player_fraction.allowed_buildings: #type: ignore
                    continue
            if not building.data.get("can_be_builded", True):
                continue

            if building.type not in uniqu_buildings:
                uniqu_buildings.append(building.type)
            else:
                continue
            building_type = building.data.get("type", "general")
            if buildings_by_types.get(building_type, False):
                buildings_by_types[building_type].append(building)
            else:
                buildings_by_types[building_type] = []
                buildings_by_types[building_type].append(building)

        return buildings_by_types
    
    def try_to_build_on_cell(self, cell: Cell):
        if self.buildings.get(str(cell.coord), None) == None:
            self.build_scheme(root.game_manager.gui.game.sticked_object.img.replace(".png", ""), cell.coord, root.player_id) #type: ignore
        
    def remove_resource(self, target: Cell|Building, resource: str, amout: int, inv_type: str = "input") -> str:
        if isinstance(target, Cell):
            building = self.buildings[str(target.coord)]
        else:
            building = target
        return building.remove_resource(resource, amout, inv_type)

    def add_resources(self, target: Cell|Building, resource: str, amout: int, inv_type: str = "output") -> str:
        if isinstance(target, Cell):
            building = self.buildings[str(target.coord)]
        else:
            building = target
        return building.add_resource(resource, amout, inv_type)