from .... import root
from ....root import logger
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ...buildings.building import Building

class Storage:
    def __init__(self, id: int = -1, coord: tuple[int, int, int] = (-1, -1, 0), fraction_id: int = -1, data: dict | None = None, is_default: bool = True):
        self.id = id
        self.coord: tuple[int, int, int] = coord
        self.is_default = is_default
        if is_default:
            logger.error("created default town", f"Town.__init__({id}, {coord}, {fraction_id}, {data}, {is_default})")
        self.data = (data or {}).copy()
        self.fraction_id = fraction_id
        self.can_work = self.data.get("can_work", False)
        
        self.bandwidth = 5
        self.conection_lenght = 1
        self.conection: list[Building] = []

    def __repr__(self):
        if not self:
            return f"<Storage is default>"
        else:
            return f"<Storage at {self.coord}>"
    
    def __bool__(self) -> bool:
        return not self.is_default

    def destroy(self):
        pass
    
    def check_conection(self):
        self.conection = []
        cells = root.game_manager.world_map.get_travel_region(self.coord, self.conection_lenght, root.player_id==self.fraction_id)
        for cell, _ in cells.values():
            if cell.buildings != {} and cell.coord != self.coord:
                if cell.buildings["fraction_id"] == self.fraction_id:
                    building = root.game_manager.buildings_manager.get_building_by_coord(cell.coord)
                    self.conection.append(building)
    
    def turn(self):
        if not self.can_work: return

        self_building = root.game_manager.buildings_manager.get_building_by_coord(self.coord)
        remainder_bandwidth = self.bandwidth
        for building in self.conection:
            if building.is_producer:
                for production in building.producer.prodaction.keys():
                    while building.inventory.has_resource(production, inv_type="output") and remainder_bandwidth > 0:
                        resource = building.inventory.get_resource(resource_name=production, resource_amount=remainder_bandwidth, category="output")
                        if resource:
                            remainder_bandwidth -= resource.amount
                            self_building.add_resource(resource=resource)
                            building.inventory.remove_resource(resource=resource, inv_type="output")