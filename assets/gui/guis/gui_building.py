from ..buttons import *
from ..infoboxs import *
from ..contentbox import *
from ..statistikbox import *
from ..textfield import *
from ..iconbox import *
from ..listof import *
import assets.root as root
from assets.decorators import timeit

class GUIBuildings:
    def __init__(self):
        self.building_ico = None
        self.building_name = None
        self.building_level = None
        self.building_info = None
        self.buildings_queue_name = None
        self.buildings_queue = []
        self.building_reciept_button = WorkbenchButton()
        self.upgrade_building_button = UpgradeBuildingButton(root.interface_size, root.interface_size//3)
    
    def change_position_for_new_screen_sizes(self):
        self.building_reciept_button.change_position((root.window_size[0]-self.building_reciept_button.width-10, root.window_size[1]-self.building_reciept_button.height-10))

    def open(self):
        chosen_cell = root.game_manager.get_chosen_cell()
        cell_size = root.cell_sizes[root.cell_size_scale][0]

        self.building_ico = Icon(cell_size, cell_size, position=(10, 10), img=f"data/buildings/img/{chosen_cell.buildings["img"]}")
        self.building_name = TextField(root.interface_size*2, 60, position=(cell_size+20, 10), text=f"{chosen_cell.buildings["name"]}") #type: ignore
        self.building_level = TextField(root.interface_size//2, root.interface_size//3, position=(10, self.building_ico.rect.height+20), text=f"lvl {chosen_cell.buildings["level"]}") #type: ignore
        
        building = root.game_manager.buildings_manager.get_building_by_coord(chosen_cell.coord)

        if root.game_manager.buildings_manager.get_building_by_coord(root.game_manager.get_chosen_cell_coord()).can_be_upgraded():
            self.upgrade_building_button.rect.height = root.interface_size//3
            self.upgrade_building_button.change_position((root.interface_size//2+20, self.building_ico.rect.height+20))
        else:
            self.upgrade_building_button.rect.height = 0

        self.buildings_queue = []
        y_offset = 0
        if building.data.get("max_queue", False):
            self.buildings_queue_name = TextField(root.interface_size//2, root.interface_size//4, position=(10, self.building_ico.rect.height+self.upgrade_building_button.rect.height+30), text="Queue") #type: ignore
            y_offset += 2
            for i in range(building.max_queue): #type: ignore
                position = (10+(cell_size+10)*i, self.building_ico.rect.height+self.upgrade_building_button.rect.height+self.buildings_queue_name.rect.height+40)
                if i < len(building.queue): #type: ignore
                    self.buildings_queue.append(Icon(cell_size, cell_size, position=position, img=f"data/reciepts/img/{building.queue[i]["img"]}")) #type: ignore
                else:
                    self.buildings_queue.append(Icon(cell_size, cell_size, position=position, img="data/reciepts/img/empty.png")) #type: ignore
        else:
            self.buildings_queue_name = None

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
        
        root.need_update_gui = False