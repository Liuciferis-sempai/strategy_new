import os
import json
import copy
from typing import Any, TYPE_CHECKING
from .. import root
from ..root import loading, logger
from .pawns.pawn import Pawn
from ..auxiliary_stuff import *

if TYPE_CHECKING:
    from ..gamemanager import GameManager

class JobManager:
    def __init__(self, game_manager: "GameManager"):
        self.game_manager = game_manager
        self.jobs: dict[str, dict] = {}

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
        if equal(job.get("pawn_category"), get(pawn, "category")) or is_empty(job.get("pawn_category")):
            if equal(job.get("pawn_types"), get(pawn, "type")) or is_empty(job.get("pawn_types")):
                return True
        return False

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
        target_name = job_name.split(".")[-1].replace("with_", "")

        if job != {}:
            if self._are_type_or_id_there(job, pawn):
                if isinstance(job["trigger"], dict):
                    return self._check_job_trigger(job["trigger"], target_name, pawn.fraction_id)
                elif isinstance(job["trigger"], list):
                    result = []
                    for trigger in job["trigger"]:
                        result.append(self._check_job_trigger(trigger, target_name, pawn.fraction_id))
                    return all(result)
            else:
                logger.warning(f"job type or id is not enable for job {job_id}.", f"JobManager.is_job_availible({job_id}, {pawn})")
        else:
            logger.warning(f"job id is not recognized '{job_id}'", f"JobManager.is_job_available({job_id}, {pawn})")
        return False
    
    def _check_job_trigger(self, trigger: dict, target_name: str, fraction_id: int|None = None) -> bool:
        self.game_manager.parsing_json_data(trigger, target_name, calling_fraction_id=fraction_id)
        is_allowed = self.game_manager.trigger(trigger)
        if not is_allowed: self.game_manager.messenger.print_buffer()
        return is_allowed