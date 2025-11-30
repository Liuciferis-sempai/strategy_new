from .... import root
from ....root import logger
from typing import Any, TYPE_CHECKING
import copy

if TYPE_CHECKING:
    from ...buildings.building import Building

class Workbench:
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
        
        self.conection_lenght = 1
        self.conection: list[Building] = []

        self.max_queue = self.building_data.get("max_queue", 1)
        self.queue = self.building_data.get("queue", [])

    def __repr__(self):
        if not self:
            return f"<Workbench is default>"
        else:
            return f"<Workbench {self.name} at {self.coord}>"
    
    def __bool__(self) -> bool:
        return not self.is_default

    def destroy(self):
        pass
    
    def turn(self):
        if not self.can_work: return
        pass

    def add_in_queue(self, reciept: dict|str):
        if len(self.queue) <= self.max_queue:
            if isinstance(reciept, dict):
                self.queue.append(reciept)
            else:
                self.queue.append(root.game_manager.reciept_manager.get_reciept_by_id(reciept))

    def remove_from_queue(self, reciept:dict|str) -> str:
        if isinstance(reciept, dict):
            self.queue.remove(reciept)
        else:
            reciept = root.game_manager.reciept_manager.get_reciept_by_id(reciept)
            self.queue.remove(reciept)
        return f"recipe {reciept.get("id", reciept.get("type", "ERROR"))} has been successfully removed from the queue"