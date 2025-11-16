from .. import root
from random import random
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from .cell import Cell
    from .worldmap import WorldMap

class River:
    def __init__(self, start_pos: tuple[int, int, int], worldmap: "WorldMap"):
        self.start_pos = start_pos
        self.cells: list["Cell"] = []
        self._loop(worldmap)
    
    def _loop(self, worldmap: "WorldMap"):
        x = self.start_pos[0]
        y = self.start_pos[1]
        while x < root.world_map_size[0]-1:
            if y < 0:
                y = 0
            elif y > root.world_map_size[1]-1:
                y = root.world_map_size[1]-1
            self.cells.append(worldmap.get_cell_by_coord((x, y, 0)))
            worldmap.change_cell_by_coord((x, y, 0), "river")
            if random() > 0.8:
                if random() > 0.5:
                    y += 1
                    x -= 1
                else:
                    y -= 1
                    x -= 1
            elif random() > 0.99:
                worldmap.rivers.append(River((x, y, 0), worldmap))
            x += 1