import pygame as py
import assets.root as root
from assets.functions import logging

class Cell(py.sprite.Sprite):
    def __init__(self, position: tuple[int, int]=(0, 0), coord: tuple[int, int]=(0, 0), data: dict={"type": "field", "desc": "field_desc", "temperature": 0.5, "height": 0.5, "humidity": 0.5, "soil_fertility": 0.5}, is_default: bool=True):
        super().__init__()
        self.data = data
        self.position = position
        self.coord = coord

        self.is_default = is_default
        if is_default:
            logging("WARNING", "created default cell", "Cell.__init__", f"position: {position}, coord: {coord}, data: {data}")

        self.type = data.get("type", "field")
        self.land = data.get("img", "field.png")
        self.flora = data.get("flora", {})
        self.fauna = data.get("fauna", {})
        self.buildings = {}
        self.pawns = []
        self.chosen_pawn_index = -1

        self.mark_image = py.Surface((root.cell_sizes[root.cell_size_scale][0]+10, root.cell_sizes[root.cell_size_scale][1]+10), py.SRCALPHA)
        self.mark_image.fill((0, 0, 0, 0))
        self._set_graph()
    
    def __repr__(self) -> str:
        return f"<Cell on coord {self.coord} with args: {self.type} | {self.flora.get("name", "none")} | {self.fauna.get("name", "none")}. Is {"not" if not self.is_default else ""} default>"

    def click(self, mouse_pos: tuple[int, int]):
        root.handler.set_chosen_cell(self)
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
        title = self.type
        if self.flora != {}:
            title += f":with_{self.flora.get("name")}"
        if self.fauna != {}:
            if self.flora != {}:
                title += ":and:"
            title += f":with_{self.fauna.get("name")}"
        root.handler.gui.game.open_main_info_window({"title": title, "text": self.data["desc"]})
    
    def _open_pawn(self):
        title = self.pawns[self.chosen_pawn_index].get("name")
        desc = self.pawns[self.chosen_pawn_index].get("desc")
        root.handler.gui.game.open_main_info_window({"title": title, "text": desc})
        root.handler.gui.game.open_pawn()
        root.handler.world_map.mark_movement_region(self.pawns[self.chosen_pawn_index].get("coord"), self.pawns[self.chosen_pawn_index].get("movement_points", 1), (0, 0, 255, 100))
        if root.player_id == self.pawns[self.chosen_pawn_index].get("fraction_id"):
            root.handler.set_opened_pawn(self.pawns[self.chosen_pawn_index])

    def _open_building(self):
        if self.buildings.get("fraction_id") == root.player_id:
            root.handler.gui.game.open_building()
        root.handler.gui.game.open_main_info_window({"title": self.buildings.get("name"), "text": self.buildings.get("desc")})

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
        self._set_graph()

    def mark(self, color: tuple[int, int, int, int]=(255, 0, 0, 100)):
        self.mark_image.fill(color)
    
    def unmark(self):
        self.mark_image.fill((0, 0, 0, 0))

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