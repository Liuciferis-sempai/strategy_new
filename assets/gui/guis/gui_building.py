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
        self.building_desc = None
        self.building_level = None
        self.building_info = None
        self.buildings_queue_name = TextField(root.interface_size//2, root.interface_size//4, position=(10, root.cell_sizes[root.cell_size_scale][1]+80+60), text="Queue") #type: ignore
        self.buildings_queue = []
        self.building_reciept_button = WorkbenchButton()
        self.upgrade_building_button = UpgradeBuildingButton()
    
    def change_position_for_new_screen_sizes(self):
        self.building_reciept_button.change_position((root.window_size[0]-self.building_reciept_button.width-10, root.window_size[1]-self.building_reciept_button.height-10))

    def open(self):
        chosen_cell = root.game.get_chosen_cell()

        self.building_ico = Icon(root.cell_sizes[root.cell_size_scale][0], root.cell_sizes[root.cell_size_scale][1], position=(10, 10), img=f"data/buildings/img/{chosen_cell.buildings["img"]}")
        self.building_name = TextField(root.interface_size*2, 60, position=(root.cell_sizes[root.cell_size_scale][0]+20, 10), text=f"{chosen_cell.buildings["name"]}") #type: ignore
        self.building_desc = TextField(root.interface_size*2, 60, position=(10, 80), text=f"{chosen_cell.buildings["desc"]}") #type: ignore
        self.building_level = TextField(60, 60, position=(root.cell_sizes[root.cell_size_scale][0]+self.building_name.rect.width+30, 10), text=f"lvl {chosen_cell.buildings["level"]}") #type: ignore
        building = root.game.buildings_manager.get_building_by_coord(chosen_cell.coord)
        self.buildings_queue = []
        i = 0
        if building.data.get("max_queue", False):
            for i in range(building.max_queue): #type: ignore
                if i < len(building.queue): #type: ignore
                    self.buildings_queue.append(Icon(root.cell_sizes[root.cell_size_scale][0], root.cell_sizes[root.cell_size_scale][1], position=(10+root.cell_sizes[root.cell_size_scale][0]*i, root.cell_sizes[root.cell_size_scale][1]+80+self.building_desc.height+70), img=f"data/reciepts/img/{building.queue[i]["img"]}")) #type: ignore
                else:
                    self.buildings_queue.append(Icon(root.cell_sizes[root.cell_size_scale][0], root.cell_sizes[root.cell_size_scale][1], position=(10+root.cell_sizes[root.cell_size_scale][0]*i, root.cell_sizes[root.cell_size_scale][1]+80+self.building_desc.height+70), img="data/reciepts/img/empty.png")) #type: ignore
        self.upgrade_building_button.change_position((10+root.cell_sizes[root.cell_size_scale][0]*i, root.cell_sizes[root.cell_size_scale][1]+80+self.building_desc.height+70))

        #self.building_info = Statistikbox()
    
    #@timeit
    def draw(self):
        root.screen.fill((0, 0, 0))

        self.building_ico.draw() #type: ignore
        self.building_name.draw() #type: ignore
        self.building_desc.draw() #type: ignore
        self.building_level.draw() #type: ignore
        #self.building_info.draw() #type: ignore
        self.buildings_queue_name.draw()
        for reciept in self.buildings_queue:
            reciept.draw()
        if root.game.get_chosen_cell().buildings.get("type", False) == "workbench": #type: ignore
            self.building_reciept_button.draw()
        if root.game.buildings_manager.get_building_by_coord(root.game.get_chosen_cell_coord()).can_be_upgraded():
            self.upgrade_building_button.draw()
        
        root.need_update_gui = False