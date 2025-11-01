import assets.root as root
import os
from assets.auxiliary_stuff.work_with_files import read_json_file
from assets.root import loading, logger

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
        logger.error(f"reciept id {reciept_id} not found", f"RecieptsManager.get_reciept_by_id({reciept_id})")
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
        for reciept, reciept_py in zip(root.game_manager.gui.reciept.reciepts, root.game_manager.gui.reciept.reciepts_list): #type: ignore
            allowed_ico = reciept_py["allowed"]
            if allowed_ico.rect.collidepoint(mouse_pos):
                if allowed_ico.color == (0, 0, 0) and not root.game_manager.is_chosen_cell_default():
                    building = root.game_manager.buildings_manager.get_building_by_coord(root.game_manager.get_chosen_cell_coord())
                    if root.game_manager.trigger_manager.building_has_resources(reciept["necessary"], building) and len(building.queue) < building.max_queue: #type: ignore
                        reciept["time"] *= building.data["spped_of_work_mod"]
                        if "." in str(reciept["time"]):
                            reciept["time"] = str(reciept["time"]).split(".")
                            if int(reciept["time"][1][0]) > 4:
                                reciept["time"] = int(reciept["time"][0]) + 1
                            else:
                                reciept["time"] = int(reciept["time"][0])

                        for resource, amout in reciept["necessary"].values():
                            root.game_manager.buildings_manager.remove_resource(building, resource, amout)
                        for resource, amout in reciept["production"]:
                            root.game_manager.turn_manager.add_event_in_queue(reciept["time"], {"do": "add_resource", "event_data": {"building": building, "resource": resource, "amout": amout}})
                        root.game_manager.turn_manager.add_event_in_queue(reciept["time"], {"do": "clear_the_queue", "event_data": {"building": building, "reciept": reciept}})
                        building.add_in_queue(reciept.copy()) #type: ignore
                    else:
                        logger.warning(f"reciept {reciept["id"]} is not allowed, because building has not enought resources", f"RecieptsManager.use_recipe({mouse_pos})")
                else:
                    logger.warning(f"reciept {reciept["id"]} is not allowed", f"RecieptsManager.use_recipe({mouse_pos})")