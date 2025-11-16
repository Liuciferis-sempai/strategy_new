import assets.root as root
from random import random

class River:
    def __init__(self, start_pos: tuple[int, int, int], worldmap):
        self.start_pos = start_pos
        self._loop(worldmap)
    
    def _loop(self, worldmap):
        x = self.start_pos[0]
        y = self.start_pos[1]
        while x < root.world_map_size[0]-1:
            if y < 0:
                y = 0
            elif y > root.world_map_size[1]-1:
                y = root.world_map_size[1]-1
            worldmap.change_cell_by_coord((x, y, 0), "river")
            if random() > 0.8:
                if random() > 0.5:
                    y += 1
                    x -= 1
                else:
                    y -= 1
                    x -= 1
            elif random() > 0.99:
                River((x, y, 0), worldmap)
            x += 1