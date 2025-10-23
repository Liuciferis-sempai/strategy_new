import assets.root as root
import os
from assets.work_with_files import read_json_file
from assets.root import loading
from assets.functions import logging

class RecieptsManager:
    def __init__(self):
        self.reciepts = []

        loading.draw("Loading reciepts...")
        self.load_reciepts()

    def load_reciepts(self):
        self.reciepts = []
        for file in os.listdir("data/reciepts/data/"):
            if file.endswith(".json"):
                reciept = read_json_file(f"data/reciepts/data/{file}")
                self.reciepts.append(reciept)
    
    def get_reciept_by_id(self, reciept_id: str) -> dict:
        for reciept in self.reciepts:
            if reciept["id"] == reciept_id:
                return reciept.copy()
        logging("ERROR", f"reciept id {reciept_id} not found", "RecieptsManager.get_reciept_by_id")
        return {}
    
    def get_reciepts_for_workbench(self, workbench_type: str, workbench_level: int) -> list:
        allowed_reciepts = []
        for reciept in self.reciepts:
            for workbench_type_ in reciept["workbench_types"]:
                for allowed_type, allowed_level in workbench_type_.items():
                    if allowed_type == workbench_type and allowed_level <= workbench_level:
                        allowed_reciepts.append(reciept.copy())
        return allowed_reciepts

    def use_recipe(self, mouse_pos: tuple[int, int]):
        for reciept, reciept_py in zip(root.handler.gui.reciept.reciepts, root.handler.gui.reciept.reciepts_list): #type: ignore
            allowed_ico = reciept_py["allowed"]
            if allowed_ico.rect.collidepoint(mouse_pos):
                if allowed_ico.color == (0, 0, 0) and not root.handler.is_chosen_cell_default():
                    chosen_cell = root.handler.get_chosen_cell()
                    building = root.handler.buildings_manager.get_building_by_coord(root.handler.get_chosen_cell_coord())
                    if root.handler.trigger_manager.building_has_resources(reciept["necessary"], building) and len(building.queue) < building.max_queue: #type: ignore
                        reciept["time"] *= building.data["spped_of_work_mod"]
                        if "." in str(reciept["time"]):
                            reciept["time"] = str(reciept["time"]).split(".")
                            if int(reciept["time"][1][0]) > 4:
                                reciept["time"] = int(reciept["time"][0]) + 1
                            else:
                                reciept["time"] = int(reciept["time"][0])

                        root.handler.buildings_manager.remove_resource(chosen_cell, reciept["necessary"])
                        root.handler.turn_manager.add_event_in_queue(reciept["time"], {"do": "add_item_to_building", "event_data": {"cell": chosen_cell, "items": reciept["production"]}})
                        root.handler.turn_manager.add_event_in_queue(reciept["time"], {"do": "clear_the_queue", "event_data": {"cell": chosen_cell, "reciept": reciept}})
                        building.add_in_queue(reciept.copy()) #type: ignore
                    else:
                        logging("DEBUG", f"reciept {reciept["id"]} is not allowed, because building has not enought resources", "RecieptsManager.use_recipe")
                else:
                    logging("DEBUG", f"reciept {reciept["id"]} is not allowed", "RecieptsManager.use_recipe")