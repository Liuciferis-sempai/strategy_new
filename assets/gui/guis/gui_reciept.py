from ..buttons import *
from ..infoboxs import *
from ..contentbox import *
from ..statistikbox import *
from ..textfield import *
from ..iconbox import *
from ..listof import *
import assets.root as root
from assets.root import logger
from assets.auxiliary_stuff import timeit

class GUIReciept:
    def __init__(self):
        self.reciepts = None
        self.buttons: list[UseReciept] = []
        self.reciepts_list = []
        self.reciept_y_offset = 0

        self.item_width = root.interface_size//4
        self.item_height = root.interface_size//4
    
    def open(self):
        self.reciept_y_offset = 0
        chosen_cell = root.game_manager.get_chosen_cell()

        self.reciepts_list = []
        player_fraction = root.game_manager.fraction_manager.get_player_fraction()
        if not player_fraction:
            logger.error("Player fraction not found when opening GUIReciept", "GUIReciept.open()")
            #print("Player Fraction doesnt found")
            return False
        self.reciepts = root.game_manager.reciept_manager.get_reciepts_for_workbench(chosen_cell.buildings["type"], chosen_cell.buildings["level"]) #type: ignore
        self.reciepts = [reciept for reciept in self.reciepts if reciept["id"] in player_fraction.reciepts]
        building = root.game_manager.buildings_manager.get_building_by_coord(root.game_manager.get_chosen_cell_coord())
        for reciept in self.reciepts:
            is_allowed = root.game_manager.trigger_manager.target_has_resources(reciept["necessary"], building)
            is_allowed_img = "allowed.png" if is_allowed else "not_allowed.png"

            time = Icon(self.item_width, self.item_height, img="time.png")
            time_cost = TextField(self.item_width,  self.item_height, text=reciept["time"])
            necessary = [Icon(self.item_width, self.item_height, img=resource) for resource in reciept["necessary"]]
            necessary_count = [TextField(self.item_width, self.item_height, text=reciept["necessary"][resource]) for resource in reciept["necessary"]]
            production = [Icon(self.item_width, self.item_height, img=production) for production in reciept["production"]]
            production_count = [TextField(self.item_width, self.item_height, text=reciept["production"][resource]) for resource in reciept["production"]]
            use_reciept = UseReciept(width=self.item_width, height=self.item_height, img=is_allowed_img, is_allowed=is_allowed, value=f"{reciept["id"]}")
            allowed = use_reciept
            self.buttons.append(use_reciept)
            self.reciepts_list.append({"necessary": necessary, "necessary_count": necessary_count, "time": time, "time_cost": time_cost, "production": production, "production_count": production_count, "allowed": allowed})
    
    #@timeit
    def draw(self):
        root.screen.fill((0, 0, 0))

        y = 0
        for reciept in self.reciepts_list:
            x = 0
            for necessary, necessary_count in zip(reciept["necessary"], reciept["necessary_count"]):
                necessary.change_position((x+10, y*self.item_height+10+10*y+self.reciept_y_offset))
                x += self.item_width+10
                necessary_count.change_position((x+10, y*self.item_height+10+10*y+self.reciept_y_offset))
                x += self.item_width+10

            reciept["time"].change_position((x+20, y*self.item_height+10+10*y+self.reciept_y_offset))
            x += self.item_width+20
            reciept["time_cost"].change_position((x+10, y*self.item_height+10+10*y+self.reciept_y_offset))
            x += self.item_width+30

            for production, production_count in zip(reciept["production"], reciept["production_count"]):
                production.change_position((x+10, y*self.item_height+10+10*y+self.reciept_y_offset))
                x += self.item_width+10
                production_count.change_position((x+10, y*self.item_height+10+10*y+self.reciept_y_offset))
                x += self.item_width+10
            
            reciept["allowed"].change_position((root.window_size[0]-self.item_width-10, y*self.item_height+10+10*y+self.reciept_y_offset))
            y += 1
        root.need_update_gui = False
    
    def move_up(self):
        if self.reciept_y_offset < 0:
            self.reciept_y_offset += root.interface_size//8
            update_gui()

    def move_down(self):
        self.reciept_y_offset -= root.interface_size//8
        update_gui()

    def move_left(self):
        pass

    def move_right(self):
        pass