import pygame as py
from ..buttons import *
from ..infoboxs import *
from ..contentbox import *
from ..statistikbox import *
from ..textfield import *
from ..iconbox import *
from ..listof import *
from ..inputfield import *
from ... import root
from ...root import logger
from ...auxiliary_stuff import *
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ...gamemanager import GameManager

from ...managers.buildings.building import Building

class GUIBuildings:
    def __init__(self, game_manager: "GameManager"):
        self.game_manager = game_manager

        cell_size = get_cell_side_size()
        self._default_building = self.game_manager.get_default_building()
        self.building = self._default_building

        self.building_ico = Icon(cell_size, cell_size, img=f"data/buildings/img/none")
        self.building_name = InputField(root.interface_size*2, 60, place_holder=f"unknow", bg_color=(255, 255, 255, 255), font_size=40, hidden=True)
        game_manager.add_inputfield(self.building_name)
        self.building_level = TextField(root.interface_size//2, root.interface_size//3, text=f"lvl unknow")
        self.buildings_queue_name = TextField(root.interface_size//2, root.interface_size//4, text="Queue")
        self.building_town_population_name = TextField(int(root.interface_size*1.2), root.interface_size//4, text="population *:")
        self.buildings_queue: list[TextField] = []
        self.buildings_town_population: list[TextField] = []
        self.building_reciept_button = WorkbenchButton()
        self.upgrade_building_button = UpgradeBuildingButton(root.interface_size, root.interface_size//3)

        self.y_global_offset = 0
    
    def change_position_for_new_screen_sizes(self):
        cell_size = get_cell_side_size()

        self.building_ico.change_position((10, 10+self.y_global_offset))
        self.building_name.change_position((cell_size+20, 10+self.y_global_offset))
        self.building_level.change_position((10, self.building_ico.rect.height+20+self.y_global_offset))

        y_offset = self.building_ico.rect.height+self.building_level.rect.height+self.y_global_offset+20
        if self.building.can_be_upgraded():
            self.upgrade_building_button.change_position((root.interface_size//2+20, self.building_ico.rect.height+self.y_global_offset+20))
            y_offset += self.upgrade_building_button.rect.height+10

        if self.building.is_workbench or self.building.is_town:
            if self.building.is_workbench:
                self.building_reciept_button.change_position((root.window_size[0]-self.building_reciept_button.width-10, root.window_size[1]-self.building_reciept_button.height-10))
            self.buildings_queue_name.change_position((10, y_offset+10))
            y_offset += self.buildings_queue_name.rect.height + 10
            for i, qeue_ico in enumerate(self.buildings_queue):
                position = (10+(cell_size+10)*i, y_offset+10)
                qeue_ico.change_position(position)
            y_offset += self.buildings_queue[-1].rect.height+10
        
        if self.building.is_town:
            self.building_town_population_name.change_position((10, y_offset+10))
            y_offset += self.building_town_population_name.rect.height + 10
            x = [root.interface_size//2, root.interface_size, root.interface_size, root.interface_size]
            xi = 0
            for i, pop in enumerate(self.buildings_town_population):
                pop.change_position((x[xi], y_offset+10))
                xi += 1
                if xi > len(x)-1: xi = 0
                y_offset += pop.rect.height+10

    def open(self):
        self.y_global_offset = 0
        building = self.game_manager.get_chosen_building()
        self.building = building

        self.building_ico.update_image(f"data/buildings/img/{building.data["img"]}")
        self.building_ico.change_position((10, 10+self.y_global_offset))
        
        self.building_name.place_holder = f"{building.type}"
        self.building_name.hidden = False
        self.building_name.update_text_surface()

        self.building_level.text = f"lvl {building.level}"
        self.building_level.update_text_surface()

        self._set_building_queue()
        self._set_population()
        self.change_position_for_new_screen_sizes()

    def close(self):
        self.building_name.hidden = True
        if self.building_name.value != "":
            self.building.name = self.building_name.value
            self.building_name.value = ""
    
    def _set_building_queue(self):
        cell_size = get_cell_side_size()

        self.buildings_queue = []
        y_offset = 0

        if self.building.data.get("max_queue", False):
            y_offset += 2
            for i in range(self.building.max_queue): #type: ignore
                if i < len(self.building.queue): #type: ignore
                    self.buildings_queue.append(Icon(cell_size, cell_size, img=f"{self.building.queue[i]["img"]}", spec_path="data/reciepts/img")) #type: ignore
                else:
                    self.buildings_queue.append(Icon(cell_size, cell_size, img="empty.png", spec_path="data/reciepts/img")) #type: ignore

    def _set_population(self) :
        cell_size = get_cell_side_size()
        self.buildings_town_population = []

        if self.building.is_town:
            self.building_town_population_name.set_text(f"population *: *{self.building.town.get_sum_population()}")
            self.building_town_population_name.update_text_surface()
            for group, size in self.building.town.get_population().items():
                self.buildings_town_population.append(
                    TextField(root.interface_size, cell_size, text=f"{group} *: *{size}")
                )
                popgroup = self.building.town.get_popgroup(group)
                if popgroup == None: continue
                for subgroup, subsize in popgroup.get_population().items():
                    self.buildings_town_population.append(
                        TextField(root.interface_size, cell_size, text=f"{subgroup} *: *{sum(subsize)}")
                    )

    #@timeit
    def draw(self):
        root.screen.fill((0, 0, 0))

        self.building_ico.draw() #type: ignore
        self.building_name.draw() #type: ignore
        self.building_level.draw() #type: ignore
        if self.game_manager.get_chosen_building().can_be_upgraded():
            self.upgrade_building_button.draw()

        if self.building.is_workbench or self.building.is_town:
            self.buildings_queue_name.draw()
            if self.building.is_workbench:
                self.building_reciept_button.draw()
        for reciept in self.buildings_queue:
            reciept.draw()
        if self.building.is_town:
            self.building_town_population_name.draw()
            for population in self.buildings_town_population:
                population.draw()
        
        root.need_update_gui = False

    def move_up(self):
        if self.y_global_offset < 0:
            self.y_global_offset += 10
            self.change_position_for_new_screen_sizes()
            update_gui()

    def move_down(self):
        self.y_global_offset -= 10
        self.change_position_for_new_screen_sizes()
        update_gui()

    def move_left(self):
        pass

    def move_right(self):
        pass