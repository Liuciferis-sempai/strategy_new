import pygame as py
import assets.root as root
from assets.root import logger

class Cell(py.sprite.Sprite):
    def __init__(self, position: tuple[int, int]=(-1, -1), coord: tuple[int, int, int]=(-1, -1, 0), data: dict={"type": "field", "desc": "field_desc", "temperature": 0.5, "height": 0.5, "humidity": 0.5, "soil_fertility": 0.5}, is_default: bool=True):
        super().__init__()
        self.data = data.copy()
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

        self.mark_image = py.Surface((root.cell_sizes[root.cell_size_scale][0]+10, root.cell_sizes[root.cell_size_scale][1]+10), py.SRCALPHA)
        self.mark_image.fill((0, 0, 0, 0))
        self.mark_image.set_alpha(0)
        self.surface = py.Surface((root.cell_sizes[root.cell_size_scale][0], root.cell_sizes[root.cell_size_scale][1]), py.SRCALPHA)
        self.surface.fill((180, 180, 180))
        self._set_graph()
    
    def __repr__(self) -> str:
        if not self:
            return f"<Cell is default>"
        else:
            return f"<Cell {self.type} on coord {self.coord} has {len(self.pawns)} pawns and {0 if self.buildings == {} else 1} buildings>"
    
    def __bool__(self) -> bool:
        return not self.is_default

    def click(self, mouse_pos: tuple[int, int]):
        root.game_manager.set_chosen_cell(self)
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
        pawn = root.game_manager.pawns_manager.get_pawn_by_id(self.pawns[self.chosen_pawn_index]["id"])
        root.game_manager.gui.game.open_main_info_window(pawn.name)
        if root.player_id == self.pawns[self.chosen_pawn_index].get("fraction_id"):
            root.game_manager.set_opened_pawn(self.pawns[self.chosen_pawn_index])
            root.game_manager.gui.game.open_pawn()
            root.game_manager.world_map.mark_movement_region(self.pawns[self.chosen_pawn_index].get("coord"), self.pawns[self.chosen_pawn_index].get("movement_points", 1))

    def _open_building(self):
        if self.buildings.get("fraction_id") == root.player_id:
            root.game_manager.gui.game.open_building(self.buildings)
        root.game_manager.gui.game.open_main_info_window(self.buildings.get("name", "unknow"))

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
        self.position = (self.coord[0]*root.cell_sizes[root.cell_size_scale][0]+5*self.coord[0], self.coord[1]*root.cell_sizes[root.cell_size_scale][1]+5*self.coord[1])
        self.surface = py.Surface((root.cell_sizes[root.cell_size_scale][0], root.cell_sizes[root.cell_size_scale][1]), py.SRCALPHA)
        self.change_display_mode(self.display_mode)
        self.mark_image = py.Surface((root.cell_sizes[root.cell_size_scale][0]+10, root.cell_sizes[root.cell_size_scale][1]+10), py.SRCALPHA)
        self._set_graph()

    def mark(self, color: tuple[int, int, int, int]=(255, 0, 0, 100)):
        self.mark_image.fill(color)
        self.mark_image.set_alpha(color[3])
    
    def unmark(self):
        self.mark_image.fill((0, 0, 0, 0))
        self.mark_image.set_alpha(0)

    def draw(self, position: tuple[int, int], image: py.surface.Surface, display_mode: str = "norlam"):
        image.blit(self.mark_image, (position[0]-5, position[1]-5))
        if self.is_opened and display_mode == "normal":
            image.blit(self.bg_image, position)
        else:
            if self.display_mode != display_mode:
                self.change_display_mode(display_mode)
            image.blit(self.surface, position)
    
    def change_display_mode(self, display_mode: str):
        self.display_mode = display_mode
        if display_mode == "temperature":
            self.surface.fill((255*self.data["temperature"], 0, 0))
        elif display_mode == "humidity":
            self.surface.fill((0, 0, 255*self.data["humidity"]))
        elif display_mode == "height":
            self.surface.fill((255*self.data["height"], 255*self.data["height"], 255*self.data["height"]))
        elif display_mode == "soil_fertility":
            self.surface.fill((255*self.data["soil_fertility"], 255*self.data["soil_fertility"]/2, 0))
        elif display_mode == "difficulty":
            diff = self.data["subdata"]["difficulty"] / 10
            self.surface.fill((255*diff, 0, 255*diff))
        else:
            self.surface.fill((180, 180, 180))

    def _set_graph(self):
        self.bg_image = root.image_manager.get_worldcell_image(f"land/{self.land}", "land")
        #self.bg_image = py.transform.scale(self.bg_image, root.cell_sizes[root.cell_size_scale])

        if self.fauna != {}:
            self.fauna_image = root.image_manager.get_worldcell_image(f"fauna/{self.fauna.get("img")}", "fauna")
            #self.fauna_image = py.transform.scale(self.fauna_image, root.cell_sizes[root.cell_size_scale])
            self.bg_image.blit(self.fauna_image, (0, 0))

        if self.flora != {}:
            self.flora_image = root.image_manager.get_worldcell_image(f"flora/{self.flora.get("img")}", "flora")
            #self.flora_image = py.transform.scale(self.flora_image, root.cell_sizes[root.cell_size_scale])
            self.bg_image.blit(self.flora_image, (0, 0))
        
        if self.buildings != {}:
            self.buildings_image = root.image_manager.get_image(f"data/buildings/img/{self.buildings.get("img")}", "data/buildings/img/none.png")
            self.buildings_image = py.transform.scale(self.buildings_image, root.cell_sizes[root.cell_size_scale])
            self.bg_image.blit(self.buildings_image, (0, 0))
        
        if self.pawns != []:
            self.pawns_image_list = []
            for pawn in self.pawns:
                self.pawns_image_list.append(root.image_manager.get_image(f"data/pawns/img/{pawn.get("img")}", "data/pawns/img/none.png"))

            for pawn_image in self.pawns_image_list:
                pawn_image = py.transform.scale(pawn_image, root.cell_sizes[root.cell_size_scale])
                self.bg_image.blit(pawn_image, (0, 0))

        self.rect = self.bg_image.get_rect(topleft=self.position)