#from typing import Any
import pygame as py
import root
from .cell import Cell
from .river import River
from random import randint, seed, choice, uniform, random
import os
from auxiliary_stuff import read_json_file, timeit, update_gui
from root import loading, logger

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from gamemanager import GameManager

class WorldMap(py.sprite.Sprite):
    def __init__(self,):
        super().__init__()
        
        self.display_mode = "normal"
        self.display_layer = 0
         
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

        self.cells_on_screen: list[Cell] = []
        self.marked_region: dict[str, list[Cell]] = {}

        self.terrain: dict[str, list[list[Cell]]] = {}
        self.types_of_land = []
        self.types_of_flora = []
        self.types_of_fauna = []
        
        loading.draw("Loading world map types...")
        self.load_types_of_land()
        self.load_types_of_flora()
        self.load_types_of_fauna()
    
    #@timeit
    def click(self, mouse_pos: tuple[int, int], mouse_button: int):
        rel_mouse_pos = (mouse_pos[0] - self.rect.x - self.x_offset, mouse_pos[1] - self.rect.y - self.y_offset)
        for cell in self.cells_on_screen:
            if cell.rect.collidepoint(rel_mouse_pos):
                self._process_click(cell, mouse_button)
                return
    
    def _process_click(self, cell: Cell, mouse_button: int):
        if mouse_button == 1:
            if root.game_manager.gui.game.sticked_object != None:
                self._process_lmb_click_with_sticked_object(cell)
            else:
                self._process_lmb_click_usual(cell)
        elif mouse_button == 3:
            if root.game_manager.gui.game.sticked_object != None:
                root.game_manager.gui.game.sticked_object = None
                update_gui()
            else:
                self._process_rmb_click_usual(cell)

    def _process_lmb_click_with_sticked_object(self, cell: Cell):
        root.game_manager.buildings_manager.try_to_build_on_cell(cell)

    def _process_lmb_click_usual(self, cell: Cell):
        if not root.game_manager.is_chosen_cell_default():
            if not root.game_manager.is_opened_pawn_default():
                if root.game_manager.get_opened_pawn_coord() != cell.coord:
                    self.unchose_cell()
                    if root.game_manager.pawns_manager.try_to_move_pawn(root.game_manager.get_opened_pawn(), cell):
                        self._click_at_cell(cell)
                        return
                else:
                    self.unmark_region("all")
                    root.game_manager.reset_opened_pawn()
            elif root.game_manager.get_chosen_cell_coord() != cell.coord: self.unchose_cell()

        self._click_at_cell(cell)

    def _process_rmb_click_usual(self, cell: Cell):
        if not root.game_manager.is_opened_pawn_default():
            if root.game_manager.get_opened_pawn_coord() == cell.coord:
                self.unchose_cell()
            else:
                if root.game_manager.pawns_manager.try_to_move_pawn(root.game_manager.get_opened_pawn(), cell):
                    self.unchose_cell()
                    self._click_at_cell(cell)
                else:
                    if cell.pawns != [] or cell.buildings != {}:
                        root.game_manager.set_target_coord(cell.coord)
                        root.game_manager.gui.game.show_actions(cell.pawns, cell.buildings)

    def _click_at_cell(self, cell: Cell):
        cell.click()
        cell.mark((255, 0, 0, 250))
        self._draw_cell(cell)

    def unchose_cell(self):
        if not root.game_manager.is_chosen_cell_default():
            chosen_cell = root.game_manager.get_chosen_cell()
            chosen_cell.chosen_pawn_index = -1
            chosen_cell.unmark()
            self._draw_cell(chosen_cell)
            root.game_manager.reset_chosen_cell(False)
            root.game_manager.reset_opened_pawn()
            self.unmark_region("all")
            root.game_manager.gui.game.set_standard_footer()

    def move_map_up(self):
        self.y_offset += self.move_distance
        if self.y_offset > 0:
            self.y_offset = 0
            return
        self.draw()
        root.game_manager.messenger.draw()

    def move_map_down(self):
        self.y_offset -= self.move_distance
        if -self.y_offset > self.lower_limit:
            self.y_offset = -self.lower_limit
            return
        self.draw()
        root.game_manager.messenger.draw()

    def move_map_left(self):
        self.x_offset += self.move_distance
        if self.x_offset > 0:
            self.x_offset = 0
            return
        self.draw()
        root.game_manager.messenger.draw()

    def move_map_right(self):
        self.x_offset -= self.move_distance
        if -self.x_offset > self.right_limit:
            self.x_offset = -self.right_limit
            return
        self.draw()
        root.game_manager.messenger.draw()

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

    def change_display_mode(self, display_mode: str):
        self.display_mode = display_mode

    def redraw(self):
        for cell in self.cells_on_screen:
            self._draw_cell(cell)

    def open_area(self, area: tuple[tuple[int, int, int], tuple[int, int, int]]):
        start_coord = area[0]
        end_coord = area[1]

        coord = [start_coord[0], start_coord[1]]
        cell = self.get_cell_by_coord((coord[0], coord[1], 0))
        cell.is_opened = True

        for nx in range(start_coord[0]-1, end_coord[0]+2):
            for ny in range(start_coord[1]-1, end_coord[1]+2):
                for nz in range(start_coord[2]-1, end_coord[2]+2):
                    cell = self.get_cell_by_coord((nx, ny, nz))
                    cell.is_opened = True

    #@timeit
    def draw(self):
        self.cells_on_screen = []
        self.image.fill((200, 200, 200))

        layer = self.display_layer
        cell_size = list(root.cell_sizes[root.cell_size_scale])
        cell_size[0] += 5
        cell_size[1] += 5

        start_col = max(0, (0 - self.x_offset) // cell_size[0])
        end_col = min(len(self.terrain[f"{layer}"][0]), (self.rect.width - self.x_offset + cell_size[0] - 1) // cell_size[0])

        start_row = max(0, (0 - self.y_offset) // cell_size[1])
        end_row = min(len(self.terrain[f"{layer}"]), (self.rect.height - self.y_offset + cell_size[1] - 1) // cell_size[1])
        
        for row in range(start_row, end_row):
            for col in range(start_col, end_col):
                cell = self.terrain[f"{layer}"][row][col]
                self.cells_on_screen.append(cell)
                self._draw_cell(cell)

        root.screen.blit(self.image, self.rect)
        if root.game_manager.gui.game.main_info_window_content.text != "":
            root.game_manager.gui.game.main_info_window_content.draw()
        #logger.info(f"drawn {len(self.cells_on_screen)}", "WorldMap.draw()")
    
    def _draw_cell(self, cell: Cell):
        cell_position = cell.rect.topleft
        cell_position = (cell_position[0] + self.x_offset, cell_position[1] + self.y_offset)
        cell.draw(cell_position, self.image, self.display_mode)

    #def mark_region(self, coord: tuple[int, int, int], color: tuple[int, int, int, int]=(255, 0, 0, 100), radius:int=1, mark_type:str="for_move"):
    #    for y in range(coord[0]-radius, coord[0]+radius+1):
    #        for x in range(coord[1]-radius, coord[1]+radius+1):
    #            if 0 <= x < root.world_map_size[0] and 0 <= y < root.world_map_size[1]:
    #                cell = self.get_cell_by_coord((0, x, y))
    #                if cell:
    #                    cell.mark(color)
    #                    self._draw_cell(cell)
    #                    self._add_mark(cell, mark_type)

    def mark_movement_region(self, start_coord: tuple[int, int, int], movement_points: int=1, color: tuple[int, int, int, int]=(0, 0, 255, 150)):
        cells = self.get_travel_region(start_coord, movement_points, True)

        for cell, remaining in cells.values():
            cell.data["subdata"]["movement_points"] = remaining
            cell.mark(color)
            self._add_mark(cell, "for_move")
            if cell in self.cells_on_screen:
                self._draw_cell(cell)
    
    def get_travel_region(self, start_coord: tuple[int, int, int], movement_points: int=1, set_open: bool = False) -> dict[tuple[int, int, int], tuple[Cell, float]]:
        width, height = root.world_map_size

        visited: dict[tuple[int, int, int], tuple[Cell, float]] = {}
        queue = []
        
        for nx in range(start_coord[0]-1, start_coord[0]+2):
            for ny in range(start_coord[1]-1, start_coord[1]+2):
                if (nx, ny, start_coord[2]) != (start_coord[0], start_coord[1], start_coord[2]):
                    cell = self.get_cell_by_coord((nx, ny, start_coord[2]))
                    if set_open: cell.is_opened = True
                    queue.append(((nx, ny, start_coord[2]), movement_points))

        while queue:
            (x, y, z), points_left = queue.pop(0)

            if not (0 <= x < width and 0 <= y < height):
                continue

            cell = self.get_cell_by_coord((x, y, start_coord[2]))
            difficulty = cell.data["subdata"]["difficulty"]
            remaining = points_left - difficulty

            if remaining < 0:
                if set_open and cell.data["subdata"].get("translucent"):
                    cell.is_opened = True
                    for nx in range(x-1, x+2):
                        for ny in range(y-1, y+2):
                            if (nx, ny, start_coord[2]) != (x, y, start_coord[2]):
                                cell = self.get_cell_by_coord((nx, ny, start_coord[2]))
                                cell.is_opened = True
                continue

            if (x, y, z) in visited and visited[(x, y, z)][1] >= remaining:
                continue

            if set_open: cell.is_opened = True

            visited[(x, y, z)] = (cell, remaining)

            for nx in range(x-1, x+2):
                for ny in range(y-1, y+2):
                    if (nx, ny, start_coord[2]) != (x, y, z):
                        queue.append(((nx, ny, start_coord[2]), remaining))
            
        return visited
    
    def _add_mark(self, cell: Cell, type_:str):
        if type_ not in self.marked_region:
            self.marked_region[type_] = []
        if cell not in self.marked_region[type_]:
            self.marked_region[type_].append(cell)

    def unmark_region(self, type_:str):
        if type_ == "all":
            for type__ in self.marked_region.keys():
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
        for layer in self.terrain.values():
            for row in layer:
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

    def get_cell_by_coord(self, coord: tuple[int, int, int]) -> Cell:
        try:
            return self.terrain[f"{coord[2]}"][coord[1]][coord[0]]
        except:
            logger.warning(f"Cell coord {coord} is not founded", f"WorldMap.get_cell_by_coord({coord})")
            return Cell()

    def change_cell_by_coord(self, coord: tuple[int, int, int], new_type: str, change_cell_modifications: bool = True):
        cell = self.get_cell_by_coord(coord)
        old_type = cell.type
        data = {}

        for type in self.types_of_land:
            if new_type == type["name"]:
                data = {"type": type["name"], "desc": type["desc"], "img": type["img"]}
                data["temperature"] = cell.data["temperature"]
                data["height"] = cell.data["height"]
                data["humidity"] = cell.data["humidity"]
                data["soil_fertility"] = cell.data["soil_fertility"]
                data["subdata"] = type["subdata"]
                data["pawns"] = cell.pawns
                data["buildings"] = cell.buildings

                if change_cell_modifications:
                    if type.get("frame_modification", False):
                        for modification_type, modification in type["frame_modification"].items():
                            if modification[0] != modification[1]:
                                data[modification_type] = uniform(modification[0], modification[1])
                            else:
                                data[modification_type] = modification[0]
                break

        self.terrain[f"{coord[2]}"][coord[1]][coord[0]] = Cell(position=cell.position, coord=cell.coord, data=data, is_default=False)
        return f"changed cell by coord {cell.coord} from {old_type} to {new_type}"

    @timeit
    def map_generate(self, seed_:int=0):
        loading.draw("Map generation...")
        seed(seed_)
        self.terrain = {"0": []}

        #earth surface generation
        for y in range(root.world_map_size[0]):
            self.terrain["0"].append([])
            for x in range(root.world_map_size[1]):
                temperature = uniform(0.2, 0.8)
                humidity = uniform(0.5, 0.8)
                height = uniform(0.1, 0.75)
                soil_fertility = uniform(0.4, 0.7)

                land = self._define_land({"temperature": temperature, "humidity": humidity, "height": height, "soil_fertility": soil_fertility})
                land = self._define_flora(land)
                land = self._define_fauna(land)

                cell = Cell(position=(x*root.cell_sizes[root.cell_size_scale][0]+5*x, y*root.cell_sizes[root.cell_size_scale][1]+5*y), coord=(x, y, 0), data=land, is_default=False)
                self.terrain["0"][-1].append(cell)
        self.lower_limit = (root.world_map_size[1]-1)*root.cell_sizes[root.cell_size_scale][1]+(root.world_map_size[1]-1)*5
        self.right_limit = (root.world_map_size[0]-1)*root.cell_sizes[root.cell_size_scale][0]+(root.world_map_size[0]-1)*5

        #river generation
        for _ in range(root.river_count):
            if random() > 0.3:
                River((0, 0, randint(0, root.world_map_size[1])), self)
            else:
                River((0, randint(0, root.world_map_size[0]), randint(0, root.world_map_size[1])), self)
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