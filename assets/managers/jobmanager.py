import os
import json
import copy
from typing import Any, TYPE_CHECKING
from .. import root
from ..root import loading, logger
from .pawns.pawn import Pawn

if TYPE_CHECKING:
    from ..gamemanager import GameManager

class JobManager:
    def __init__(self, game_manager: "GameManager"):
        self.game_manager = game_manager
        self.jobs = {}

        loading.draw("Loading job types...")
        self.load_jobs()
    
    def load_jobs(self):
        self.jobs = {}
        for jobfile in os.listdir("data/jobs"):
            if jobfile.endswith(".json"):
                with open(f"data/jobs/{jobfile}", "r", encoding="utf-8") as f:
                    job_data = json.load(f)
                    self.jobs[job_data["id"]] = job_data

    def _are_type_or_id_there(self, job: dict, pawn: dict|Pawn) -> bool:
        '''
        checking if pawn type or id is in job's allowed types or ids
        '''
        if isinstance(pawn, dict):
            if job.get("pawn_category", []) == [] or "any" in job.get("pawn_category", []) or pawn["category"] in job.get("pawn_category", []):
                    if job.get("pawn_types", []) == [] or "any" in job.get("pawn_types", []) or pawn["type"] in job.get("pawn_types", []):
                        return True

        elif isinstance(pawn, Pawn):
            if job.get("pawn_category", []) == [] or "any" in job.get("pawn_category", []) or pawn.category in job.get("pawn_category", []):
                    if job.get("pawn_types", []) == [] or "any" in job.get("pawn_types", []) or pawn.type in job.get("pawn_types", []):
                        return True
        return False
    
    def _procces_trigger(self, trigger: dict, job_name: str) -> dict:
        chosen_cell_coord = self.game_manager.get_chosen_cell_coord()
        target_coord = self.game_manager.get_target_coord()

        if trigger["args"].get("target_of_action", None) != None:
            trigger["args"]["target_of_action"] = job_name.replace("with_", "")
            trigger["args"]["coord"] = target_coord
        
        if trigger["args"].get("target_building_coord", None) != None:
            trigger["args"]["target_building_coord"] = chosen_cell_coord

        return trigger
    
    def procces_result(self, job: dict, job_name: str) -> dict:
        chosen_cell_coord = self.game_manager.get_chosen_cell_coord()
        target_coord = self.game_manager.get_target_coord()
    
        if job["result"]["args"].get("target_building_coord", None) != None:
            job["result"]["args"]["target_building_coord"] = chosen_cell_coord

        if job["result"]["type"] == "attack":
            target_name = job_name.split(".")[-1]
            if target_name in self.game_manager.buildings_manager.get_all_possible_buildings_names():
                target = self.game_manager.buildings_manager.get_building_by_coord(self.game_manager.get_target_coord())
            else:
                target = self.game_manager.pawns_manager.get_pawn_by_coord(target_name, self.game_manager.get_target_coord())
            job["result"]["args"]["target"] = target
            job["result"]["args"]["data"] = self.game_manager.get_chosen_pawn().attack

        if job["result"]["args"].get("target_of_action", None) != None:
            target_of_action = job_name.split(".")[-1]
            job["result"]["args"]["target_of_action"] = target_of_action.replace("with_", "")

        if job["result"]["args"].get("target_cell", None) != None:
            job["result"]["args"]["target_cell"] = self.game_manager.world_map.get_cell_by_coord(target_coord)

        if job["result"]["args"].get("target_building_str", None) != None:
            building = self.game_manager.world_map.get_cell_by_coord(chosen_cell_coord).buildings
            job["result"]["args"]["target_building_str"] = building.get("name", "").replace("scheme:of_", "")
            job["result"]["args"]["building_coord"] = chosen_cell_coord
            job["result"]["args"]["building_fraction"] = building.get("fraction_id", -1)
        
        if job["result"]["args"].get("fauna_loot", None) != None:
            job["result"]["args"]["loot"] = self.game_manager.get_chosen_cell().fauna.get("loot", {})

        if "pawn" in self.game_manager.effect_manager.effects[job["result"]["type"]].keys():
            job["result"]["args"]["pawn"] = self.game_manager.get_chosen_pawn()

        return job

    def _replace_target_in_args(self, job: dict, job_id: str) -> dict:
        '''
        prepares the work result for processing by the effects manager, replacing placeholders with game objects
        '''
        chosen_cell_coord = self.game_manager.get_chosen_cell_coord()
        target_coord = self.game_manager.get_target_coord()

        if job["trigger"]["args"].get("target_of_action", None) != None:
            job["trigger"]["args"]["target_of_action"] = job_id.split(".")[-1]
            job["trigger"]["args"]["target_of_action"] = job["trigger"]["args"]["target_of_action"].replace("with_", "")
            job["trigger"]["args"]["coord"] = target_coord
        
        if job["trigger"]["args"].get("target_building_coord", None) != None:
            job["result"]["args"]["target_building_coord"] = chosen_cell_coord
        
        if job["result"]["type"] == "attack":
            target_name = job_id.split(".")[-1]
            if target_name in self.game_manager.buildings_manager.get_all_possible_buildings_names():
                target = self.game_manager.buildings_manager.get_building_by_coord(self.game_manager.get_target_coord())
            else:
                target = self.game_manager.pawns_manager.get_pawn_by_coord(target_name, self.game_manager.get_target_coord())
            job["result"]["args"]["target"] = target
            job["result"]["args"]["data"] = self.game_manager.get_chosen_pawn().attack

        if job["result"]["args"].get("target_of_action", None) != None:
            target_of_action = job_id.split(".")[-1]
            job["result"]["args"]["target_of_action"] = target_of_action.replace("with_", "")

        if job["result"]["args"].get("target_cell", None) != None:
            job["result"]["args"]["target_cell"] = self.game_manager.world_map.get_cell_by_coord(target_coord)

        if job["result"]["args"].get("target_building_str", None) != None:
            building = self.game_manager.world_map.get_cell_by_coord(chosen_cell_coord).buildings
            job["result"]["args"]["target_building_str"] = building.get("name", "").replace("scheme:of_", "")
            job["result"]["args"]["building_coord"] = chosen_cell_coord
            job["result"]["args"]["building_fraction"] = building.get("fraction_id", -1)

        return job

    def get_job_id_from_name(self, name: str) -> str:
        '''
        if job_id is like "build_house.with_pawnname", it will return "build_house" (removes excess) in other cases return name as is
        '''
        return name.split(".")[0] if "." in name else name
    
    def get_job_by_id(self, job_id: str) -> dict:
        job = self.jobs.get(job_id, None)
        if job:
            return copy.deepcopy(job)
        logger.error(f"job id is not founded {job_id}", f"JobManager.get_job_by_id({job_id})")
        return {}.copy()
    
    def get_jobs_for_pawn(self, pawn: Pawn) -> list:
        jobs = []
        for job in self.jobs.values():
            if job.get("type", "work") == "work":
                if self._are_type_or_id_there(job, pawn):
                    jobs.append(copy.deepcopy(job))

        return jobs

    def get_jobs_id_for_pawn(self, pawn: Pawn) -> list:
        jobs = []
        for job in self.jobs.values():
            if job.get("type", "work") == "work":
                if self._are_type_or_id_there(job, pawn):
                    if self._are_type_or_id_there(job, pawn):
                        jobs.append(job["id"])

        return jobs
    
    #def is_job_available(self, job_name: str, pawn: "Pawn") -> bool:
    #    job = self.get_job_by_id(self.get_job_id_from_name(job_name))
    #    if job:
    #        if self._are_type_or_id_there(job, pawn):
    #            if isinstance(job["trigger"], dict):
    #                return self._is_job_available(job, job_name, pawn)
    #            elif isinstance(job["trigger"], list):
    #                result = []
    #                for trigger in job["trigger"]:
    #                    temp_job = job
    #                    temp_job["trigger"] = trigger
    #                    result.append(self._is_job_available(temp_job, job_name, pawn))
    #                return all(result)
    #        else:
    #            logger.warning(f"job type or id is not enable for this job.", f"JobManager.is_job_availible({job_name}, {pawn})")
    #    else:
    #        logger.warning(f"job id is not recognized '{self.get_job_id_from_name(job_name)}'", f"JobManager.is_job_available({job_name}, {pawn})")
    #    return False
    
    #def _is_job_available(self, job: dict, job_name: str, pawn: "Pawn") -> bool:
    #    if hasattr(self.game_manager.trigger_manager, job["trigger"]["type"]):
    #        job = self._replace_target_in_args(job, job_name)
    #        trigger_func = getattr(self.game_manager.trigger_manager, job["trigger"]["type"])
    #        return trigger_func(pawn, job["trigger"].get("args", {})) #type: ignore
    #    return False
    

    def is_job_available(self, job_name: str, pawn: "Pawn") -> bool:
        job_id = self.get_job_id_from_name(job_name)
        job = self.get_job_by_id(job_id)
        if job != {}:
            if self._are_type_or_id_there(job, pawn):
                if isinstance(job["trigger"], dict):
                    return self._check_job_trigger(job["trigger"], job_name, pawn)
                elif isinstance(job["trigger"], list):
                    result = []
                    for trigger in job["trigger"]:
                        result.append(self._check_job_trigger(trigger, job_name, pawn))
                    return all(result)
            else:
                logger.warning(f"job type or id is not enable for job {job_id}.", f"JobManager.is_job_availible({job_id}, {pawn})")
        else:
            logger.warning(f"job id is not recognized '{job_id}'", f"JobManager.is_job_available({job_id}, {pawn})")
        return False
    
    def _check_job_trigger(self, trigger: dict, job_name: str, pawn: "Pawn") -> bool:
        if hasattr(self.game_manager.trigger_manager, trigger["type"]):
            trigger = self._procces_trigger(trigger, job_name)
            trigger_func = getattr(self.game_manager.trigger_manager, trigger["type"])
            is_allowed = trigger_func(pawn, **trigger["args"])
            if not is_allowed: self.game_manager.messenger.print_buffer()
            return is_allowed
        return False