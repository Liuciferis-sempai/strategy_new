#from typing import Any
import pygame as py
import assets.root as root
from .cell import Cell
from .river import River
from random import randint, seed, choice, uniform, random
import os
from assets.work_with_files import read_json_file
from assets.decorators import timeit
from assets.functions import update_gui
from assets.root import loading, logger

class WorldMap(py.sprite.Sprite):
    def __init__(self):
        super().__init__()
         
        self.width = root.window_size[0]
        self.height = root.window_size[1]-root.button_standard_size[1]-50

        self.image = py.Surface((self.width, self.height))
        self.image.fill((200, 200, 200))
        self.rect = py.Rect(0, root.button_standard_size[1] +10, self.width, self.height)

        self.x_offset = 0
        self.y_offset = 0
        self.move_distance = root.cell_sizes[root.cell_size_scale][1]//4
        self.lower_limit = 0
        self.right_limit = 0

        self.cells_on_screen = []
        self.marked_region = {}

        self.terrain = []
        self.types_of_land = []
        self.types_of_flora = []
        self.types_of_fauna = []
        
        loading.draw("Loading world map types...")
        self.load_types_of_land()
        self.load_types_of_flora()
        self.load_types_of_fauna()
    
    #@timeit
    def click(self, mouse_pos: tuple[int, int], mouse_button: int):
        #print("World map clicked")
        rel_mouse_pos = (mouse_pos[0] - self.rect.x - self.x_offset, mouse_pos[1] - self.rect.y - self.y_offset)
        for cell in self.cells_on_screen:
            if cell.rect.collidepoint(rel_mouse_pos):
                if root.handler.gui.game.sticked_object != None:
                    root.handler.buildings_manager.try_to_build_on_cell(cell)
                else:
                    #if (cell.pawns != [] or cell.buildings != {}) and mouse_button == 1:
                    #    root.handler.reset_opened_pawn()
                    #print(cell)
                    self._normal_click(cell, rel_mouse_pos, mouse_button)
                return
    
    def _normal_click(self, cell: Cell, rel_mouse_pos: tuple[int, int], mouse_button: int):
        if not root.handler.is_opened_pawn_default():
            if root.handler.get_opened_pawn_coord() == cell.coord:
                root.handler.reset_opened_pawn()
            else:
                root.handler.pawns_manager.try_to_move_pawn(root.handler.get_opened_pawn(), cell)
                return
        if root.handler.get_chosen_cell() != cell:
            self.unchose_cell()
        cell.click(rel_mouse_pos)
        cell.mark((255, 0, 0, 100))
        self._draw_cell(cell)

    def unchose_cell(self):
        if not root.handler.is_chosen_cell_default():
            chosen_cell = root.handler.get_chosen_cell()
            chosen_cell.chosen_pawn_index = -1
            chosen_cell.unmark()
            self._draw_cell(chosen_cell)
            root.handler.reset_chosen_cell()
            self.unmark_region("all")

    def move_map_up(self):
        self.y_offset += self.move_distance
        if self.y_offset > 0:
            self.y_offset = 0
            return
        #for row in self.terrain:
        #    for cell in row:
        #        cell.rect.top += self.move_distance
        #update_gui()
        self.draw()

    def move_map_down(self):
        self.y_offset -= self.move_distance
        if -self.y_offset > self.lower_limit:
            self.y_offset = -self.lower_limit
            return
        #for row in self.terrain:
        #    for cell in row:
        #        cell.rect.top -= self.move_distance
        #update_gui()
        self.draw()

    def move_map_left(self):
        self.x_offset += self.move_distance
        if self.x_offset > 0:
            self.x_offset = 0
            return
        #for row in self.terrain:
        #    for cell in row:
        #        cell.rect.left += self.move_distance
        #update_gui()
        self.draw()

    def move_map_right(self):
        self.x_offset -= self.move_distance
        if -self.x_offset > self.right_limit:
            self.x_offset = -self.right_limit
            return
        #for row in self.terrain:
        #    for cell in row:
        #        cell.rect.right -= self.move_distance
        #update_gui()
        self.draw()

    def load_types_of_land(self):
        self.types_of_land = []
        for cellfile in os.listdir("data/map/cell_data/land"):
            if cellfile.endswith(".json"):
                type = read_json_file(f"data/map/cell_data/land/{cellfile}")
                self.types_of_land.append(type)
    
    def load_types_of_flora(self):
        self.types_of_flora = []
        for cellfile in os.listdir("data/map/cell_data/flora"):
            if cellfile.endswith(".json"):
                type = read_json_file(f"data/map/cell_data/flora/{cellfile}")
                self.types_of_flora.append(type)
    
    def load_types_of_fauna(self):
        self.types_of_fauna = []
        for cellfile in os.listdir("data/map/cell_data/fauna"):
            if cellfile.endswith(".json"):
                type = read_json_file(f"data/map/cell_data/fauna/{cellfile}")
                self.types_of_fauna.append(type)

    def redraw(self):
        for cell in self.cells_on_screen:
            self._draw_cell(cell)

    #@timeit
    def draw(self):
        self.cells_on_screen = []
        self.image.fill((200, 200, 200))

        cell_size = list(root.cell_sizes[root.cell_size_scale])
        cell_size[0] += 5
        cell_size[1] += 5

        start_col = max(0, (0 - self.x_offset) // cell_size[0])
        end_col = min(len(self.terrain[0]), (self.rect.width - self.x_offset + cell_size[0] - 1) // cell_size[0])

        start_row = max(0, (0 - self.y_offset) // cell_size[1])
        end_row = min(len(self.terrain), (self.rect.height - self.y_offset + cell_size[1] - 1) // cell_size[1])
        
        for row in range(start_row, end_row):
            for col in range(start_col, end_col):
                cell = self.terrain[row][col]
                self.cells_on_screen.append(cell)
                self._draw_cell(cell)

        root.screen.blit(self.image, self.rect)
        #root.handler.gui.game.main_info_window_content.draw()
        #logger.info(f"drawn {len(self.cells_on_screen)}", "WorldMap.draw()")
    
    def _draw_cell(self, cell: Cell):
        cell_position = cell.rect.topleft
        cell_position = (cell_position[0] + self.x_offset, cell_position[1] + self.y_offset)
        self.image.blit(cell.mark_image, (cell_position[0]-5, cell_position[1]-5))
        self.image.blit(cell.bg_image, cell_position)

    def mark_region(self, coord: tuple[int, int], color: tuple[int, int, int, int]=(255, 0, 0, 100), radius:int=1, mark_type:str="for_move"):
        for y in range(coord[0]-radius, coord[0]+radius+1):
            for x in range(coord[1]-radius, coord[1]+radius+1):
                if 0 <= x < root.world_map_size[0] and 0 <= y < root.world_map_size[1]:
                    cell = self.get_cell_by_coord((x, y))
                    if cell:
                        cell.mark(color)
                        self._draw_cell(cell)
                        self._add_mark(cell, mark_type)
    
    def mark_movement_region(self, coord: tuple[int, int], movement_points: int=1, color: tuple[int, int, int, int]=(0, 0, 255, 100)):
        for x in range(coord[0]-1, coord[0]+2):
            for y in range(coord[1]-1, coord[1]+2):
                if 0 <= x < root.world_map_size[0] and 0 <= y < root.world_map_size[1]:
                    cell = self.get_cell_by_coord((x, y))
                    if cell:
                        if movement_points >= cell.data["subdata"]["difficulty"] and movement_points > 0:
                            self._mark_movement_region((x, y), movement_points-cell.data["subdata"]["difficulty"], color)
                            cell.mark(color)
                            cell.data["subdata"]["movement_points"] = movement_points - cell.data["subdata"]["difficulty"]
                            self._draw_cell(cell)
                            self._add_mark(cell, "for_move")

    def _mark_movement_region(self, coord: tuple[int, int], movement_points: int=1, color: tuple[int, int, int, int]=(0, 0, 255, 100)):
        for y in range(coord[1]-1, coord[1]+2):
            for x in range(coord[0]-1, coord[0]+2):
                if 0 <= x < root.world_map_size[0] and 0 <= y < root.world_map_size[1]:
                    cell = self.get_cell_by_coord((x, y))
                    if cell:
                        if movement_points >= cell.data["subdata"]["difficulty"] and movement_points > 0:
                            self._mark_movement_region((x, y), movement_points-cell.data["subdata"]["difficulty"], color)
                            cell.data["subdata"]["movement_points"] = movement_points - cell.data["subdata"]["difficulty"]
                            cell.mark(color)
                            self._draw_cell(cell)
                            self._add_mark(cell, "for_move")
    
    def _add_mark(self, cell: Cell, type_:str):
        if type_ not in self.marked_region:
            self.marked_region[type_] = []
        if cell not in self.marked_region[type_]:
            self.marked_region[type_].append(cell)

    def unmark_region(self, type_:str):
        if type_ == "all":
            for type__ in self.marked_region:
                for cell in self.marked_region[type__]:
                    cell.data["subdata"].pop("movement_points", None)
                    cell.unmark()
                    self._draw_cell(cell)
                self.marked_region[type__].clear()
        else:
            for cell in self.marked_region[type_]:
                cell.data["subdata"].pop("movement_points", None)
                cell.unmark()
                self._draw_cell(cell)
            self.marked_region[type_].clear()

    def resize(self):
        loading.draw("Resizing world map...")
        logger.info("Resizing world map", f"WorldMap.resize()")
        for row in self.terrain:
            for cell in row:
                cell.resize()

    def change_position(self, header_tab:int=0, footer_tab:int=0, header_info_tab:int=0):
        top_offset = (root.button_standard_size[1]+20)*(header_tab+1)+20+root.info_box_size[1]*header_info_tab
        bottom_offset = (root.button_standard_size[1]+20)*(footer_tab+1)+10
        if top_offset < 0:
            #print("top offset is negative", top_offset)
            top_offset = 0
        if bottom_offset < 0:
            #print("bottom offset is negative", bottom_offset)
            bottom_offset = 0

        y = top_offset

        self.width = root.window_size[0]
        self.height = root.window_size[1]-top_offset-bottom_offset
        if self.height < 0:
            logger.warning("Calculated world map height is negative. Adjusting to minimum size.", f"WorldMap.change_position({header_tab}, {footer_tab}, {header_info_tab})")
            #print("Screen is too low", self.height)
            self.height = root.cell_sizes[root.cell_size_scale][1]*2
            #y = root.cell_sizes[root.cell_size_scale][1]//2+20
        
        self.image = py.Surface((self.width, self.height))
        self.image.fill((200, 200, 200))
        self.rect = py.Rect(0, y, self.width, self.height)

        self.rect.topleft = (0, y)

    def get_cell_by_coord(self, coord: tuple[int, int]) -> Cell:
        try:
            return self.terrain[coord[1]][coord[0]]
        except:
            logger.warning(f"Cell coord {coord} is not founded", f"WorldMap.get_cell_by_coord({coord})")
            return Cell()

    def change_cell_by_coord(self, coord: tuple[int, int], new_type: str):
        cell = self.terrain[coord[0]][coord[1]]
        #print(coord, cell.coord)

        data = {}

        for type in self.types_of_land:
            if new_type == type["name"]:
                data = {"type": type["name"], "desc": type["desc"], "img": type["img"]}
                data["temperature"] = cell.data["temperature"]
                data["height"] = cell.data["height"]
                data["humidity"] = cell.data["humidity"]
                data["soil_fertility"] = cell.data["soil_fertility"]
                data["subdata"] = type["subdata"]

                if type.get("frame_modification", False):
                    for modification_type, modification in type["frame_modification"].items():
                        if modification[0] != modification[1]:
                            data[modification_type] = uniform(modification[0], modification[1])
                        else:
                            data[modification_type] = modification[0]
                break

        self.terrain[coord[0]][coord[1]] = Cell(position=cell.position, coord=cell.coord, data=data, is_default=False)

    @timeit
    def map_generate(self, seed_:int=0):
        loading.draw("Map generation...")
        seed(seed_)
        self.terrain = []
        for y in range(root.world_map_size[0]):
            self.terrain.append([])
            for x in range(root.world_map_size[1]):
                temperature = uniform(0.2, 0.8)
                humidity = uniform(0.5, 0.8)
                height = uniform(0.1, 0.75)
                soil_fertility = uniform(0.4, 0.7)

                land = self._define_land({"temperature": temperature, "humidity": humidity, "height": height, "soil_fertility": soil_fertility})
                land = self._define_flora(land)
                land = self._define_fauna(land)

                cell = Cell(position=(x*root.cell_sizes[root.cell_size_scale][0]+5*x, y*root.cell_sizes[root.cell_size_scale][1]+5*y), coord=(x, y), data=land, is_default=False)
                self.terrain[-1].append(cell)
        self.lower_limit = (root.world_map_size[1]-1)*root.cell_sizes[root.cell_size_scale][1]+(root.world_map_size[1]-1)*5
        self.right_limit = (root.world_map_size[0]-1)*root.cell_sizes[root.cell_size_scale][0]+(root.world_map_size[0]-1)*5
        for _ in range(root.river_count):
            if random() > 0.3:
                River((0, randint(0, root.world_map_size[1])), self)
            else:
                River((randint(0, root.world_map_size[0]), randint(0, root.world_map_size[1])), self)
        seed(None)
        update_gui()

    def _check_for_frame_conditions(self, frame: list[dict], data: dict) -> list:
        possible_types = []
        for type in frame:
            is_impossible = False

            if type["frame"]["temperature"][0] != 0.0 or type["frame"]["temperature"][1] != 1.0:
                if not (type["frame"]["temperature"][0] <= data["temperature"] <= type["frame"]["temperature"][1]):
                    is_impossible = True

            if type["frame"]["height"][0] != 0.0 or type["frame"]["height"][1] != 1.0:
                if not (type["frame"]["height"][0] <= data["height"] <= type["frame"]["height"][1]):
                    is_impossible = True

            if type["frame"]["humidity"][0] != 0.0 or type["frame"]["humidity"][1] != 1.0:
                if not (type["frame"]["humidity"][0] <= data["humidity"] <= type["frame"]["humidity"][1]):
                    is_impossible = True

            if type["frame"]["soil_fertility"][0] != 0.0 or type["frame"]["soil_fertility"][1] != 1.0:
                if not (type["frame"]["soil_fertility"][0] <= data["soil_fertility"] <= type["frame"]["soil_fertility"][1]):
                    is_impossible = True

            if not is_impossible:
                possible_types.append(type)

        return possible_types

    def _define_land(self, data: dict) -> dict:
        possible_types = self._check_for_frame_conditions(self.types_of_land, data)

        if len(possible_types) > 1:
            for type in possible_types:
                if type["priority"] == 0:
                    possible_types.remove(type)
        elif len(possible_types) == 0:
            logger.warning("No possible land types found for cell with given conditions. Choosing random land type.", f"WorldMap._define_land({data})")
            #print("impossible cell conditions")
            possible_types.append(choice(self.types_of_land))

        cell_type = choice(possible_types)
        if cell_type.get("frame_modification", False):
            for modification_type, modification in cell_type["frame_modification"].items():
                if modification[0] != modification[1]:
                    data[modification_type] = uniform(modification[0], modification[1])
                else:
                    data[modification_type] = modification[0]

        return {"type": cell_type["name"], "desc": cell_type["desc"], "img": cell_type["img"], "temperature": data["temperature"], "height": data["height"], "humidity": data["humidity"], "soil_fertility": data["soil_fertility"], "subdata": cell_type["subdata"]}

    def _define_flora(self, land: dict) -> dict:
        possible_types = self._check_for_frame_conditions(self.types_of_flora, land)

        if len(possible_types) > 1:
            for type in possible_types:
                if type["priority"] == 0:
                    possible_types.remove(type)
        elif len(possible_types) == 0:
            return land

        flora_type = choice(possible_types)
        if flora_type.get("frame_modification", False):
            for modification_type, modification in flora_type["frame_modification"].items():
                if modification[0] != modification[1]:
                    land[modification_type] = uniform(modification[0], modification[1])
                else:
                    land[modification_type] = modification[0]
        
        land["flora"] = flora_type

        return land
    
    def _define_fauna(self, land: dict) -> dict:
        possible_types = self._check_for_frame_conditions(self.types_of_fauna, land)

        if len(possible_types) > 1:
            for type in possible_types:
                if type["priority"] == 0:
                    possible_types.remove(type)
        elif len(possible_types) == 0:
            return land

        fauna_type = choice(possible_types)
        if fauna_type.get("frame_modification", False):
            for modification_type, modification in fauna_type["frame_modification"].items():
                if modification[0] != modification[1]:
                    land[modification_type] = uniform(modification[0], modification[1])
                else:
                    land[modification_type] = modification[0]
        
        land["fauna"] = fauna_type

        return land