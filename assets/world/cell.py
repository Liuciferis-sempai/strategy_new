import pygame as py
from .. import root
from ..root import logger
from ..auxiliary_stuff import *
from copy import deepcopy

class Cell(py.sprite.Sprite):
    def __init__(self, position: tuple[int, int]=(-1, -1), coord: tuple[int, int, int]=(-1, -1, 0), data: dict={"type": "field", "desc": "field_desc", "temperature": 0.5, "height": 0.5, "humidity": 0.5, "soil_fertility": 0.5}, is_default: bool=True):
        super().__init__()
        self.data = deepcopy(data)
        self.position = position
        self.coord: tuple[int, int, int] = coord
        self.is_opened = False
        self.display_mode = "normal"

        self.is_default = is_default
        if is_default:
            logger.warning("created default cell", f"Cell.__init__(...)")

        self.type = data.get("type", "field")
        self.land = data.get("img", "field.png")
        self.flora = data.get("flora", {})
        self.fauna = data.get("fauna", {})
        self.buildings = data.get("buildings", {})
        self.pawns = data.get("pawns", [])
        self.chosen_pawn_index = -1

        cell_side_size = get_cell_side_size()

        self.mark_image = py.Surface((cell_side_size+10, cell_side_size+10), py.SRCALPHA)
        self.mark_image.fill((0, 0, 0, 0))
        self.mark_image.set_alpha(0)

        self.icon = data.get("icon", "none")

        self.surface = py.Surface((cell_side_size, cell_side_size), py.SRCALPHA)
        self.surface.fill((180, 180, 180))
        self._set_graph()
    
    def __repr__(self) -> str:
        if not self:
            return f"<Cell is default>"
        else:
            return f"<Cell {self.type} on coord {self.coord} has {len(self.pawns)} pawns and {0 if is_empty(self.buildings) else 1} buildings>"
    
    def __bool__(self) -> bool:
        return not self.is_default

    def click(self):
        root.game_manager.set_chosen_cell(self)
        if not self.is_opened: return
        if self.pawns != []:
            self.chosen_pawn_index += 1
            if self.chosen_pawn_index > len(self.pawns)-1:
                self.chosen_pawn_index = -1
                if self.buildings != {}:
                    self._open_building()
                else:
                    self._open_land()
            else:
                self._open_pawn()
        elif self.buildings != {}:
            self.chosen_pawn_index += 1
            if self.chosen_pawn_index == 0:
                self._open_building()
            else:
                self.chosen_pawn_index = -1
                self._open_land()
        else:
            self._open_land()

    def _open_land(self):
        title = self.type if self.is_opened else "not_researched"
        #if self.flora != {}:
        #    title += f":with_{self.flora.get("name")}"
        #if self.fauna != {}:
        #    if self.flora != {}:
        #        title += ":and"
        #    title += f":with_{self.fauna.get("name")}"
        root.game_manager.gui.game.open_main_info_window(title)
    
    def _open_pawn(self):
        pawn = root.game_manager.get_pawn(pawn_id=self.pawns[self.chosen_pawn_index]["id"])
        root.game_manager.gui.game.open_main_info_window(f"*{pawn.name}")
        if root.player_id == self.pawns[self.chosen_pawn_index].get("fraction_id"):
            root.game_manager.set_chosen_pawn(self.pawns[self.chosen_pawn_index])
            root.game_manager.gui.game.open_pawn()
            root.game_manager.world_map.mark_movement_region(self.pawns[self.chosen_pawn_index].get("coord"), pawn.data["movement_points"])

    def _open_building(self):
        if self.buildings.get("fraction_id") == root.player_id:
            root.game_manager.set_chosen_building(self.buildings)
            root.game_manager.gui.game.open_building()
        root.game_manager.gui.game.open_main_info_window(f"*{self.buildings.get("name", "unknow")}")

    def change_type(self, new_type: str):
        self.type = new_type
        self.flora = {}
        self.fauna = {}
        self._set_graph()

    def remove_building(self):
        self.buildings = {}
        self._set_graph()

    def remove_pawn(self, pawn_id: int):
        for pawn in self.pawns:
            if pawn["id"] == pawn_id:
                self.pawns.remove(pawn)
                self._set_graph()

    def add_building(self, data: dict):
        self.buildings = data
        self._set_graph()

    def add_pawn(self, data: dict):
        self.pawns.append(data)
        self._set_graph()

    def resize(self):
        cell_side_size = get_cell_side_size()

        self.position = (self.coord[0]*cell_side_size+5*self.coord[0], self.coord[1]*cell_side_size+5*self.coord[1])
        self.surface = py.Surface((cell_side_size, cell_side_size), py.SRCALPHA)
        self.change_display_mode(self.display_mode)
        self.mark_image = py.Surface((cell_side_size+10, cell_side_size+10), py.SRCALPHA)
        self._set_graph()

    def mark(self, color: tuple[int, int, int, int]=(255, 0, 0, 100)):
        self.mark_image.fill(color)
        self.mark_image.set_alpha(color[3])
    
    def unmark(self):
        self.mark_image.fill((0, 0, 0, 0))
        self.mark_image.set_alpha(0)

    def draw(self, display_mode: str = "normal"):
        root.game_manager.world_map.blit(self.mark_image, (self.rect.left-5, self.rect.top-5))
        if self.is_opened and display_mode == "normal":
            root.game_manager.world_map.blit(self.bg_image, self.rect.topleft)
        else:
            if self.display_mode != display_mode:
                self.change_display_mode(display_mode)
            if display_mode == "fraction":
                self._set_fraction_color()
                if self.is_opened:
                    root.game_manager.world_map.blit(self.bg_image, self.rect.topleft)
            root.game_manager.world_map.blit(self.surface, self.rect.topleft)
    
    def change_display_mode(self, display_mode: str):
        self.display_mode = display_mode
        self.surface.set_alpha(255)

        if display_mode == "temperature":
            self.surface.fill((255*self.data["temperature"], 0, 0))
        elif display_mode == "humidity":
            self.surface.fill((0, 0, 255*self.data["humidity"]))
        elif display_mode == "height":
            self.surface.fill((255*self.data["height"], 255*self.data["height"], 255*self.data["height"]))
        elif display_mode == "soil_fertility":
            self.surface.fill((255*self.data["soil_fertility"], 255*self.data["soil_fertility"]/2, 0))
        elif display_mode == "difficulty":
            diff = 255 * (self.data["subdata"]["difficulty"] / 5)
            self.surface.fill((255-diff, 255-diff, 255-diff))
        elif display_mode == "fraction":
            self._set_fraction_color()
        else:
            self.surface.fill((180, 180, 180))

    def _set_fraction_color(self):
        if self.buildings != {}: fraction = root.game_manager.fraction_manager.get_fraction_by_id(self.buildings["fraction_id"])
        elif self.pawns != []: fraction = root.game_manager.fraction_manager.get_fraction_by_id(self.pawns[0]["fraction_id"])
        else: fraction = None
            
        if fraction:
            self.surface.fill(fraction.color)
            self.surface.set_alpha(130)
        else:
            self.surface.set_alpha(0)
    
    def set_icon(self, new_icon: str|None = None):
        if new_icon == self.icon: return
        if new_icon: self.icon = new_icon
        
        if self.icon != "none":
            self.icon_image = root.image_manager.get_image(f"data/icons/{self.icon}.png")
            self.bg_image.blit(self.icon_image, (0, 0))
    
    def remove_icon(self):
        self.icon = "none"
        self._set_graph()

    def _set_graph(self):
        self.bg_image = root.image_manager.get_worldcell_image(f"land/{self.land}", "land")
        #self.bg_image = py.transform.scale(self.bg_image, get_cell_size())

        if self.fauna != {}:
            self.fauna_image = root.image_manager.get_worldcell_image(f"fauna/{self.fauna.get("img")}", "fauna")
            #self.fauna_image = py.transform.scale(self.fauna_image, get_cell_size())
            self.bg_image.blit(self.fauna_image, (0, 0))

        if self.flora != {}:
            self.flora_image = root.image_manager.get_worldcell_image(f"flora/{self.flora.get("img")}", "flora")
            #self.flora_image = py.transform.scale(self.flora_image, get_cell_size())
            self.bg_image.blit(self.flora_image, (0, 0))

        if self.buildings != {}:
            self.buildings_image = root.image_manager.get_image(f"data/buildings/img/{self.buildings.get("img")}", "data/buildings/img/none.png")
            self.buildings_image = py.transform.scale(self.buildings_image, get_cell_size())
            if self.buildings["is_scheme"]:
                self.buildings_image.set_alpha(150)
            self.bg_image.blit(self.buildings_image, (0, 0))
        
        if self.pawns != []:
            self.pawns_image_list = []
            for pawn in self.pawns:
                self.pawns_image_list.append(root.image_manager.get_image(f"data/pawns/img/{pawn.get("img")}", "data/pawns/img/none.png"))

            for pawn_image in self.pawns_image_list:
                pawn_image = py.transform.scale(pawn_image, get_cell_size())
                self.bg_image.blit(pawn_image, (0, 0))
        
        self.set_icon()
        self.rect = self.bg_image.get_rect(topleft=self.position)

    def change_position(self, new_position: tuple[int, int]):
        self.position = new_position
        self.rect.topleft = new_position
    
    def get(self, att: str) -> str|int|float|None:
        match att:
            case "temperature":
                return round(self.data["temperature"], 2)
            case "height":
                return round(self.data["height"], 2)
            case "humidity":
                return round(self.data["humidity"], 2)
            case "soil_fertility":
                return round(self.data["soil_fertility"], 2)
            case "difficulty":
                return self.data["subdata"]["difficulty"]
            case "fraction":
                if self.buildings != {}: return root.game_manager.fraction_manager.get_fraction_by_id(self.buildings["fraction_id"]).name
                elif self.pawns != []: return root.game_manager.fraction_manager.get_fraction_by_id(self.pawns[0]["fraction_id"]).name
                else: return None