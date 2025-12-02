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
        self.building_level = TextField(root.interface_size//2, root.interface_size//3, text="lvl", text_kwargs={"lvl": "unknow"})
        self.buildings_queue_name = TextField(root.interface_size//2, root.interface_size//4, text="Queue")
        self.building_town_population_name = TextField(int(root.interface_size*1.2), root.interface_size//4, text="population")
        self.workbench_queue: list[Icon] = []
        self.town_queue: list[Icon] = []
        self.buildings_town_population: list[TextField] = []
        self.building_reciept_button = WorkbenchButton()
        self.upgrade_building_button = UpgradeBuildingButton(root.interface_size, root.interface_size//3)
    
    def change_position_for_new_screen_sizes(self):
        cell_size = get_cell_side_size()
        y_offset = self.game_manager.get_y_offset()

        self.building_ico.change_position((10, 10+y_offset))
        self.building_name.change_position((cell_size+20, 10+y_offset))
        self.building_level.change_position((10, self.building_ico.rect.height+20+y_offset))

        y_offset = self.building_ico.rect.height+self.building_level.rect.height+y_offset+20
        if self.building.can_be_upgraded():
            self.upgrade_building_button.change_position((root.interface_size//2+20, y_offset-self.building_level.rect.height))

        if self.building.is_workbench:
            if self.building.is_workbench:
                self.building_reciept_button.change_position((root.window_size[0]-self.building_reciept_button.width-10, root.window_size[1]-self.building_reciept_button.height-10))
            self.buildings_queue_name.change_position((10, y_offset+10))
            y_offset += self.buildings_queue_name.rect.height + 10
            for i, qeue_ico in enumerate(self.workbench_queue):
                position = (10+(cell_size+10)*i, y_offset+10)
                qeue_ico.change_position(position)
            y_offset += self.workbench_queue[-1].rect.height+10

        if self.building.is_town:
            if self.building.is_workbench:
                self.building_reciept_button.change_position((root.window_size[0]-self.building_reciept_button.width-10, root.window_size[1]-self.building_reciept_button.height-10))
            self.buildings_queue_name.change_position((10, y_offset+10))
            y_offset += self.buildings_queue_name.rect.height + 10
            for i, qeue_ico in enumerate(self.town_queue):
                position = (10+(cell_size+10)*i, y_offset+10)
                qeue_ico.change_position(position)
            y_offset += self.town_queue[-1].rect.height+10

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
        y_offset = self.game_manager.get_y_offset()

        building = self.game_manager.get_chosen_building()
        self.building = building

        self.building_ico.update_image(f"data/buildings/img/{building.data["img"]}")
        self.building_ico.change_position((10, 10+y_offset))
        
        self.building_name.place_holder = f"{building.type}"
        self.building_name.hidden = False
        self.building_name.update_text_surface()

        self.building_level.set_text("lvl", {"lvl": building.level})

        self._set_workbench_queue()
        self._set_town_queue()
        self._set_population()
        self.change_position_for_new_screen_sizes()

    def close(self):
        self.building_name.hidden = True
        if self.building_name.value != "":
            self.building.name = self.building_name.value
            self.building_name.value = ""
    
    def _set_workbench_queue(self):
        cell_size = get_cell_side_size()

        self.workbench_queue = []
        y_offset = 0

        if self.building.is_workbench:
            building_queue = self.building.get_queue()
            y_offset += 2
            for i in range(self.building.get_queue_max_lenght()):
                if i < self.building.get_queue_lenght():
                    self.workbench_queue.append(Icon(cell_size, cell_size, img=f"{building_queue[i]["img"]}", spec_path="data/reciepts/img"))
                else:
                    self.workbench_queue.append(Icon(cell_size, cell_size, img="empty.png", spec_path="data/reciepts/img"))
    
    def _set_town_queue(self):
        cell_size = get_cell_side_size()

        self.town_queue = []
        y_offset = 0

        if self.building.is_town:
            building_queue = self.building.get_queue()
            y_offset += 2
            for i in range(self.building.get_queue_max_lenght()):
                if i < self.building.get_queue_lenght():
                    self.town_queue.append(Icon(cell_size, cell_size, img=f"{building_queue[i]["img"]}", spec_path="data/pawn/img"))
                else:
                    self.town_queue.append(Icon(cell_size, cell_size, img="empty.png", spec_path="data/reciepts/img"))

    def _set_population(self) :
        cell_size = get_cell_side_size()
        self.buildings_town_population = []

        if self.building.is_town:
            self.building_town_population_name.set_text("population_titel", text_kwargs={"population": self.building.town.get_sum_population()})
            self.building_town_population_name.render_text()
            for group, size in self.building.town.get_population().items():
                self.buildings_town_population.append(
                    TextField(root.interface_size, cell_size, text="population_group_size", text_kwargs={"group": group, "size": size})
                )
                popgroup = self.building.town.get_popgroup(group)
                if popgroup == None: continue
                for subgroup, subsize in popgroup.get_population().items():
                    self.buildings_town_population.append(
                        TextField(root.interface_size, cell_size, text="population_subgroup_size", text_kwargs={"subgroup": subgroup, "size": len(subsize)})
                    )

    #@timeit
    def draw(self):
        root.screen.fill((100, 100, 100))

        self.building_ico.draw()
        self.building_name.draw()
        self.building_level.draw()
        if self.game_manager.get_chosen_building().can_be_upgraded():
            self.upgrade_building_button.draw()

        if self.building.is_workbench or self.building.is_town:
            self.buildings_queue_name.draw()
            if self.building.is_workbench:
                self.building_reciept_button.draw()
        for reciept in self.workbench_queue:
            reciept.draw()
        for pawn in self.town_queue:
            pawn.draw()
        if self.building.is_town:
            self.building_town_population_name.draw()
            for population in self.buildings_town_population:
                population.draw()
        
        root.need_update_gui = False

    def move_up(self):
        if self.game_manager.get_y_offset() < 0:
            self.game_manager.add_y_offset(10)
            self.change_position_for_new_screen_sizes()
            update_gui()

    def move_down(self):
        self.game_manager.set_y_offset(-10)
        self.change_position_for_new_screen_sizes()
        update_gui()

    def move_left(self):
        pass

    def move_right(self):
        pass