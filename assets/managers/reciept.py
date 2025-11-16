from .. import root
import os
from ..auxiliary_stuff import read_json_file
from ..root import loading, logger
import copy

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
                return copy.deepcopy(reciept)
        logger.error(f"reciept id {reciept_id} not found", f"RecieptsManager.get_reciept_by_id({reciept_id})")
        return {}
    
    def get_reciepts_for_workbench(self, workbench_type: str, workbench_level: int) -> list:
        allowed_reciepts = []
        for reciept in self.reciepts:
            for workbench_type_ in reciept["workbench_types"]:
                for allowed_type, allowed_level in workbench_type_.items():
                    if allowed_type == workbench_type and allowed_level <= workbench_level:
                        allowed_reciepts.append(copy.deepcopy(reciept))
        return allowed_reciepts

    def use_recipe(self, reciept_id: str):
        building = root.game_manager.buildings_manager.get_building_by_coord(root.game_manager.get_chosen_cell_coord())
        if not building.can_work:
            logger.warning(f"{building} can not work", f"RecieptManager.use_reciept({reciept_id})")
            return

        for reciept in self.get_reciepts_for_workbench(building.type, building.level):
            if reciept["id"] == reciept_id:
                if  not root.game_manager.is_chosen_cell_default():
                    if root.game_manager.trigger_manager.target_has_resources(reciept["necessary"], building) and len(building.queue) < building.max_queue:
                        reciept["time"] /= building.data["speed_of_work_mod"]
                        if "." in str(reciept["time"]):
                            reciept["time"] = str(reciept["time"]).split(".")
                            if int(reciept["time"][1][0]) > 4:
                                reciept["time"] = int(reciept["time"][0]) + 1
                            else:
                                reciept["time"] = int(reciept["time"][0])

                        for resource, amout in reciept["necessary"].values():
                            root.game_manager.buildings_manager.remove_resource(building, resource, amout)
                        for resource, amout in reciept["production"]:
                            root.game_manager.turn_manager.add_event_in_queue(reciept["time"], {"do": "add_resource", "event_data": {"building": "Building", "resource": resource, "amout": amout}})
                        root.game_manager.turn_manager.add_event_in_queue(reciept["time"], {"do": "clear_the_queue", "event_data": {"building": "Building", "reciept": reciept}})
                        building.add_in_queue(reciept.copy())
                        logger.info(f"added reciept {reciept["id"]} in queue for {building}", f"RecieptManager.use_reciept({reciept_id})")
                        return
                    else:
                        logger.warning(f"reciept {reciept["id"]} is not allowed, because building has not enought resources", f"RecieptsManager.use_recipe({reciept_id})")
                        return
                else:
                    logger.warning(f"reciept {reciept["id"]} is not allowed", f"RecieptsManager.use_recipe({reciept_id})")
                    return
        logger.warning(f"recipet with id {reciept_id} does not exist", f"RecieptsManager.use_recipe({reciept_id})")