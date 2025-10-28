import os
import json
import assets.triggers as tm
from assets.pawns.pawn import Pawn
from assets import root
from assets.root import loading, logger

class JobManager:
    def __init__(self):
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
            if job.get("pawn_types", []) == [] or "any" in job.get("pawn_types", []) or pawn["type"] in job.get("pawn_types", []):
                    if job.get("pawn_ids", []) == [] or "any" in job.get("pawn_ids", []) or pawn["id"] in job.get("pawn_ids", []):
                        return True

        elif isinstance(pawn, Pawn):
            if job.get("pawn_types", []) == [] or "any" in job.get("pawn_types", []) or pawn.type in job.get("pawn_types", []):
                    if job.get("pawn_ids", []) == [] or "any" in job.get("pawn_ids", []) or pawn.id in job.get("pawn_ids", []):
                        return True
        return False

    def _replace_target_in_args(self, job: dict, job_id: str, i: int = 0) -> dict:
        '''
        replacing str "target_of_action" in actual target pawn's name and add coord of target pawn's cell
        if there is no target pawn, then job will return without changes
        coord can be (-1, -1) if there is no target cell in root file. check it in this case
        '''
        chosen_cell_coord = root.game.get_chosen_cell_coord()
        target_coord = root.game.gui.game.get_target_coord()

        if job["trigger"]["args"].get("target_of_action", None) != None:
            job["trigger"]["args"]["target_of_action"] = job_id.split(".")[-1]
            job["trigger"]["args"]["target_of_action"] = job["trigger"]["args"]["target_of_action"].replace("with_", "")
            job["trigger"]["args"]["coord"] = target_coord
        
        if job["trigger"]["args"].get("target_building_coord", None) != None:
            job["result"]["args"]["target_building_coord"] = chosen_cell_coord

        if job["result"]["args"].get("target_of_action", None) != None:
            job["result"]["args"]["target_of_action"] = job_id.split(".")[-1]
            job["result"]["args"]["target_of_action"] = job["result"]["args"]["target_of_action"].replace("with_", "")

        if job["result"]["args"].get("target_cell", None) != None:
            job["result"]["args"]["target_cell"] = root.game.world_map.get_cell_by_coord(target_coord)

        if job["result"]["args"].get("target_building_str", None) != None:
            building = root.game.world_map.get_cell_by_coord(chosen_cell_coord).buildings
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
            return job.copy()
        logger.error(f"job id is not founded {job_id}", f"JobManager.get_job_by_id({job_id})")
        return {}
    
    def get_jobs_for_pawn(self, pawn: Pawn) -> list:
        jobs = []
        for job in self.jobs.values():
            if job.get("type", "work") == "work":
                if self._are_type_or_id_there(job, pawn):
                    jobs.append(job.copy())

        return jobs

    def get_jobs_id_for_pawn(self, pawn: Pawn) -> list:
        jobs = []
        for job in self.jobs.values():
            if job.get("type", "work") == "work":
                if self._are_type_or_id_there(job, pawn):
                    if self._are_type_or_id_there(job, pawn):
                        jobs.append(job["id"])

        return jobs
    
    def is_job_available(self, job_id: str, pawn: Pawn) -> bool:
        job = self.get_job_by_id(self.get_job_id_from_name(job_id))
        if job:
            if self._are_type_or_id_there(job, pawn):
                if isinstance(job["trigger"], dict):
                    return self._is_job_available(job, job_id, pawn)
                elif isinstance(job["trigger"], list):
                    result = []
                    for trigger in job["trigger"]:
                        temp_job = job
                        temp_job["trigger"] = trigger
                        result.append(self._is_job_available(temp_job, job_id, pawn))
                    return all(result)
            else:
                logger.warning(f"job type or id is not enable for this job.", f"JobManager.is_job_availible({job_id}, {pawn})")
        else:
            logger.warning(f"job id is not recognized '{self.get_job_id_from_name(job_id)}'", f"JobManager.is_job_available({job_id}, {pawn})")
        return False
    
    def _is_job_available(self, job: dict, job_id: str, pawn: Pawn) -> bool:
        if hasattr(root.game.trigger_manager, job["trigger"]["type"]):
            job = self._replace_target_in_args(job, job_id)
            trigger_func = getattr(root.game.trigger_manager, job["trigger"]["type"])
            return trigger_func(pawn, job["trigger"].get("args", {})) #type: ignore
        return False