from .... import root
from ....root import logger
from typing import Any, TYPE_CHECKING
import copy

if TYPE_CHECKING:
    from ..building import Building

class Scientific:
    def __init__(self, id: int = -1, name: str = "unknow", coord: tuple[int, int, int] = (-1, -1, 0), fraction_id: int = -1, data: dict | None = None, building_data: dict|None = None, is_default: bool = True):
        self.id = id
        self.name = name
        self.coord: tuple[int, int, int] = coord
        self.is_default = is_default
        if is_default:
            logger.error("created default scientific", f"Scientific.__init__({name}, {coord}, {fraction_id}, {data}, {is_default})")
        self.data = copy.deepcopy((data or {}))
        self.building_data = copy.deepcopy((building_data or {}))
        self.fraction_id = fraction_id
        self.can_work = self.data.get("can_work", False)

        self.speed_of_work = self.building_data.get("speed_of_work", 1)
        self.prodaction: dict[str, int] = self.building_data.get("prodaction", {})
        self.last_prodaction_at = self.building_data.get("last_prodaction_at", root.game_manager.turn_manager.turn)

    def __repr__(self):
        if not self:
            return f"<Scientific is default>"
        else:
            return f"<Scientific {self.name} at {self.coord}>"
    
    def __bool__(self) -> bool:
        return not self.is_default

    def destroy(self):
        pass
    
    def turn(self):
        if not self.can_work: return
        fraction = root.game_manager.fraction_manager.get_fraction_by_id(self.fraction_id)
        if fraction.research_technology == "none_tech": return

        turn = root.game_manager.turn_manager.turn
        if self.last_prodaction_at + self.speed_of_work <= turn:
            self.last_prodaction_at = turn
            for science, amount in self.prodaction.items():
                fraction.add_science(science, amount)