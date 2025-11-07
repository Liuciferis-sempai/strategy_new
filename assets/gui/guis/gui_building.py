from ..buttons import *
from ..infoboxs import *
from ..contentbox import *
from ..statistikbox import *
from ..textfield import *
from ..iconbox import *
from ..listof import *
import assets.root as root
from assets.auxiliary_stuff.decorators import timeit
from assets.buildings.building import Building

class GUIBuildings:
    def __init__(self):
        self.building_ico = None
        self.building_name = None
        self.building_level = None
        self.building_info = None
        self.buildings_queue_name = None
        self.buildings_queue: list[TextField] = []
        self.buildings_town_population: list[TextField] = []
        self.building_reciept_button = WorkbenchButton()
        self.upgrade_building_button = UpgradeBuildingButton(root.interface_size, root.interface_size//3)
    
    def change_position_for_new_screen_sizes(self):
        self.building_reciept_button.change_position((root.window_size[0]-self.building_reciept_button.width-10, root.window_size[1]-self.building_reciept_button.height-10))

    def open(self):
        cell_size = root.cell_sizes[root.cell_size_scale][0]
        building = root.game_manager.buildings_manager.get_building_by_coord(root.game_manager.get_chosen_cell_coord())

        self.building_ico = Icon(cell_size, cell_size, position=(10, 10), img=f"data/buildings/img/{building.data["img"]}")
        self.building_name = TextField(root.interface_size*2, 60, position=(cell_size+20, 10), text=f"{building.name}") #type: ignore
        self.building_level = TextField(root.interface_size//2, root.interface_size//3, position=(10, self.building_ico.rect.height+20), text=f"lvl {building.level}") #type: ignore

        y_offset = self.building_ico.rect.height+self.building_level.rect.height
        self._set_upgrade_button(self.building_ico.rect.height)
        y_offset += self._set_building_queue(building, y_offset, cell_size)
        y_offset += self._set_population(building, y_offset, cell_size)

    def _set_upgrade_button(self, y_pos: int) -> int:
        if root.game_manager.buildings_manager.get_building_by_coord(root.game_manager.get_chosen_cell_coord()).can_be_upgraded():
            self.upgrade_building_button.change_position((root.interface_size//2+20, y_pos+20))
            return self.upgrade_building_button.rect.height
        return 0
    
    def _set_building_queue(self, building: Building, y_pos: int, cell_size: int) -> int:
        self.buildings_queue = []
        y_offset = 0

        if building.data.get("max_queue", False):
            self.buildings_queue_name = TextField(root.interface_size//2, root.interface_size//4, position=(10, y_pos+30), text="Queue") #type: ignore
            y_offset += 2
            for i in range(building.max_queue): #type: ignore
                position = (10+(cell_size+10)*i, y_pos+self.buildings_queue_name.rect.height+40)
                if i < len(building.queue): #type: ignore
                    self.buildings_queue.append(Icon(cell_size, cell_size, position=position, img=f"data/reciepts/img/{building.queue[i]["img"]}")) #type: ignore
                else:
                    self.buildings_queue.append(Icon(cell_size, cell_size, position=position, img="data/reciepts/img/empty.png")) #type: ignore
            return self.buildings_queue_name.rect.height+40

        self.buildings_queue_name = None
        return 0

    def _set_population(self, building: Building, y_pos: int, cell_size: int) -> int:
        self.buildings_town_population = []

        if building.is_town:
            self.building_town_population_name = TextField(root.interface_size, root.interface_size//4, text="population *:", position=(10, y_pos+30))
            y = y_pos+self.building_town_population_name.rect.height+40
            for group, size in building.town.get_population().items():
                if len(self.buildings_town_population) > 0:
                    y += self.buildings_town_population[0].rect.height+10
                self.buildings_town_population.append(
                    TextField(root.interface_size, cell_size, position=(root.interface_size//2, y), text=f"{group} *: *{size}")
                )
            return self.building_town_population_name.rect.height+y
        self.building_town_population_name = None
        return 0
    
    def open_name_edit(self):
        pass

    def close_name_edit(self):
        pass

    #@timeit
    def draw(self):
        root.screen.fill((0, 0, 0))

        self.building_ico.draw() #type: ignore
        self.building_name.draw() #type: ignore
        self.building_level.draw() #type: ignore
        if root.game_manager.buildings_manager.get_building_by_coord(root.game_manager.get_chosen_cell_coord()).can_be_upgraded():
            self.upgrade_building_button.draw()

        if self.buildings_queue_name:
            self.buildings_queue_name.draw()
        for reciept in self.buildings_queue:
            reciept.draw()
        if root.game_manager.get_chosen_cell().buildings.get("type", False) == "workbench": #type: ignore
            self.building_reciept_button.draw()
        if self.building_town_population_name:
            self.building_town_population_name.draw()
            for population in self.buildings_town_population:
                population.draw()
        
        root.need_update_gui = False