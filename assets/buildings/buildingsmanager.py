import os
from assets.work_with_files import read_json_file
from .building import *
from assets import root
from assets.world.cell import Cell
from assets.root import loading, logger

class BuildingsManager:
    def __init__(self):
         
        self.buildings = {}
        self.types_of_buildings = []

        loading.draw("Loading building types...")
        self.load_types_of_buildings()

    def load_types_of_buildings(self):
        self.types_of_buildings = []
        for buildingsfile in os.listdir("data/buildings/data"):
            if buildingsfile.endswith(".json"):
                type = read_json_file(f"data/buildings/data/{buildingsfile}")
                self.types_of_buildings.append(type)

    def build(self, data: str|dict, coord: tuple[int, int], fraction_id: int) -> bool:
        '''
        use data str to build standart building
        use data dict to build building with specials characteristics
        '''
        #print(self.types_of_buildings)
        root.handler.allFractions.get_fraction_by_id(fraction_id).statistics["building_count"] += 1 #type: ignore
        for type in self.types_of_buildings:
            if data == type["name"] or data == type:
                if not self.buildings.get(str(coord), False):
                    if isinstance(data, str):
                        self._build(type, coord, fraction_id)
                    else:
                        self._build(data, coord, fraction_id)
                    return True
                elif "scheme" in self.buildings[str(coord)].name:
                    self.buildings[str(coord)].build()
                else:
                    return False
        return False
    
    def build_scheme(self, data: str|dict, coord: tuple[int, int], fraction_id: int) -> bool:
        '''
        use data str to build standart building
        use data dict to build building with specials characteristics
        '''
        for type in self.types_of_buildings:
            if data == type["name"] or data == type:
                if not self.buildings.get(str(coord), False):
                    if isinstance(data, str):
                        self._build_scheme(type, coord, fraction_id)
                    else:
                        self._build_scheme(data, coord, fraction_id)
                    return True
                else:
                    return False
        return False
    
    def _build_scheme(self, data: dict, coord: tuple[int, int], fraction_id: int):
        data = data.copy()
        data["fraction_id"] = fraction_id
        data["name"] = "scheme" + ":of_" + data["name"]
        data["img"] = data["img"].replace(".png", "_scheme.png")
        data["scheme"] = True
        cell = root.handler.world_map.get_cell_by_coord(coord)
        self.buildings[str(coord)] = Building(coord, cell, data.copy(), False)
        cell.add_building({"name": data["name"], "desc": data["desc"], "coord": coord, "img": data["img"], "fraction_id": data["fraction_id"], "type": data["type"], "level": data["level"]})

    def _build(self, data: dict, coord: tuple[int, int], fraction_id: int):
        data = data.copy()
        data["fraction_id"] = fraction_id
        cell = root.handler.world_map.get_cell_by_coord(coord)
        self.buildings[str(coord)] = Building(coord, cell, data.copy(), False)
        cell.add_building({"name": data["name"], "desc": data["desc"], "coord": coord, "img": data["img"], "fraction_id": data["fraction_id"], "type": data["type"], "level": data["level"]})
    
    def remove(self, coord: tuple[int, int]):
        building = self.buildings[str(coord)]
        root.handler.allFractions.get_fraction_by_id(building.fraction_id).statistics["building_count"] -= 1 #type: ignore
        self.buildings.pop(str(coord))
        cell = root.handler.world_map.get_cell_by_coord(coord)
        cell.remove_building()

    def get_building_by_coord(self, coord:tuple[int, int]) -> Building:
        try:
            return self.buildings[str(coord)]
        except:
            return Building()
        
    def get_all_unique_buildings_sorted_by_types(self, only_allowed_for_players_fraction: bool=True) -> dict:
        buildings_by_types = {}
        uniqu_buildings = []
        if only_allowed_for_players_fraction:
            player_fraction = root.handler.allFractions.get_player_fraction()
            if not player_fraction:
                logger.error("No player fraction found in get_all_buildings_sorted_by_types", f"BuildingsManager.get_all_buildings_sorted_by_types({only_allowed_for_players_fraction})")
                return buildings_by_types

        for building in self.buildings.values():
            if only_allowed_for_players_fraction:
                if building.name not in player_fraction.allowed_buildings: #type: ignore
                    continue
            if building.name not in uniqu_buildings:
                uniqu_buildings.append(building.name)
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
            self.build_scheme(root.handler.gui.game.sticked_object.img.replace(".png", ""), cell.coord, root.player_id) #type: ignore
        
    def remove_resource(self, cell: Cell, resources: dict|list):
        building = self.buildings[str(cell.coord)]
        if isinstance(resources, list):
            for resource, amout in resources:
                building.remove_resource(resource, amout)
        elif isinstance(resources, dict):
            for resource in resources:
                building.remove_resource(resource, resources[resource])

    def add_resources(self, cell: Cell, resources: dict|list):
        building = self.buildings[str(cell.coord)]
        if isinstance(resources, list):
            for resource, amout in resources:
                building.add_resource(resource, amout, "output")
        elif isinstance(resources, dict):
            for resource in resources:
                building.add_resource(resource, resources[resource], "output")