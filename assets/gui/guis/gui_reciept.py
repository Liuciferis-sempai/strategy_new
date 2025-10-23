from ..buttons import *
from ..infoboxs import *
from ..contentbox import *
from ..statistikbox import *
from ..textfield import *
from ..iconbox import *
from ..listof import *
import assets.root as root
from assets.functions import logging
from assets.decorators import timeit

class GUIReciept:
    def __init__(self):
        self.reciepts = None
        self.reciepts_list = []
        self.reciept_y_offset = 0
    
    def open(self):
        chosen_cell = root.handler.get_chosen_cell()

        self.reciepts_list = []
        player_fraction = root.handler.allFractions.get_player_fraction()
        if player_fraction == None:
            logging("ERROR", "Player fraction not found when opening GUIReciept", "GUIReciept.open")
            #print("Player Fraction doesnt found")
            return False
        self.reciepts = root.handler.reciept_manager.get_reciepts_for_workbench(chosen_cell.buildings["name"], chosen_cell.buildings["level"]) #type: ignore
        for reciept in self.reciepts:
            is_allowed = ["allowed.png", (0, 0, 0)] if reciept["id"] in player_fraction.reciepts else ["not_allowed.png", (255, 255, 255)]

            time = ContentBox(root.interface_size//4, root.interface_size//4, value=reciept["time"], img="time.png")
            necessary = [Icon(root.interface_size//4, root.interface_size//4, img=resource) for resource in reciept["necessary"]]
            necessary_count = [TextField(root.interface_size//4, root.interface_size//4, text=reciept["necessary"][resource]) for resource in reciept["necessary"]]
            production = [Icon(root.interface_size//4, root.interface_size//4, img=production) for production in reciept["production"]]
            production_count = [TextField(root.interface_size//4, root.interface_size//4, text=reciept["production"][resource]) for resource in reciept["production"]]
            allowed = Icon(root.interface_size//4, root.interface_size//4, img=is_allowed[0], color=is_allowed[1])
            self.reciepts_list.append({"necessary": necessary, "necessary_count": necessary_count, "time": time, "production": production, "production_count": production_count, "allowed": allowed})
    
    #@timeit
    def draw(self):
        root.screen.fill((0, 0, 0))

        y = 0
        for reciept in self.reciepts_list:
            x = 0
            for necessary, necessary_count in zip(reciept["necessary"], reciept["necessary_count"]):
                necessary.change_position((x*root.interface_size//4+10, y*root.interface_size//4+10+10*y+self.reciept_y_offset))
                x += 1
                necessary_count.change_position((x*root.interface_size//4+10, y*root.interface_size//4+10+10*y+self.reciept_y_offset))
                x += 1

            reciept["time"].change_position((x*root.interface_size//4+20, y*root.interface_size//4+10+10*y+self.reciept_y_offset))
            x += 1

            for production, production_count in zip(reciept["production"], reciept["production_count"]):
                production.change_position((x*root.interface_size//4+30, y*root.interface_size//4+10+10*y+self.reciept_y_offset))
                x += 1
                production_count.change_position((x*root.interface_size//4+30, y*root.interface_size//4+10+10*y+self.reciept_y_offset))
                x += 1
            
            reciept["allowed"].change_position((root.window_size[0]-root.interface_size//4-10, y*root.interface_size//4+10+10*y+self.reciept_y_offset))
            y += 1
        root.need_update_gui = False