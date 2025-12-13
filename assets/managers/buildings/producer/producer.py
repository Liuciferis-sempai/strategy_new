from .... import root
from ....root import logger
from typing import Any, TYPE_CHECKING
import copy

if TYPE_CHECKING:
    from ...buildings.building import Building

class Producer:
    def __init__(self, id: int = -1, name: str = "unknow", coord: tuple[int, int, int] = (-1, -1, 0), fraction_id: int = -1, data: dict | None = None, building_data: dict|None = None, is_default: bool = True):
        self.id = id
        self.name = name
        self.coord: tuple[int, int, int] = coord
        self.is_default = is_default
        if is_default:
            logger.error("created default town", f"Town.__init__({name}, {coord}, {fraction_id}, {data}, {is_default})")
        self.data = copy.deepcopy((data or {}))
        self.building_data = copy.deepcopy((building_data or {}))
        self.fraction_id = fraction_id
        self.can_work = self.data.get("can_work", False)

        self.prodaction_time = self.building_data.get("prodaction_time", 1)
        self.last_prodaction_at = self.building_data.get("last_prodaction_at", root.game_manager.turn_manager.turn)
        self.prodaction: dict[str, int] = self.building_data.get("prodaction", {})

    def __repr__(self):
        if not self:
            return f"<Producer is default>"
        else:
            return f"<Producer {self.name} at {self.coord}>"
    
    def __bool__(self) -> bool:
        return not self.is_default

    def destroy(self):
        pass
    
    def turn(self):
        if not self.can_work: return

        turn = root.game_manager.turn_manager.turn
        if self.last_prodaction_at + self.prodaction_time <= turn:
            self.last_prodaction_at = turn
            self_building = root.game_manager.get_building(coord=self.coord)
            for resource, amout in self.prodaction.items():
                self_building.add_resource(resource_name=resource, resource_amount=amout, inv_type="output")