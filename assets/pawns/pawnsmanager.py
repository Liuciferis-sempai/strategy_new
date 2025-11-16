import os
import copy
from assets.auxiliary_stuff import read_json_file
from .pawn import Pawn
from assets.world.cell import Cell
from assets import root
from assets.root import loading, logger

class PawnsManager:
    def __init__(self):
        self._default_pawn: Pawn = Pawn()

        self.pawns: list[Pawn] = []
        self.pawns_types: list[str] = []
        self.types_of_pawns: list[dict] = []
        self.available_pawn_id = 0

        loading.draw("Loading pawn types...")
        self.load_types_of_pawns()

    def load_types_of_pawns(self):
        self.types_of_pawns = []
        for pawnsfile in os.listdir("data/pawns/data"):
            if pawnsfile.endswith(".json"):
                type = read_json_file(f"data/pawns/data/{pawnsfile}")
                self.types_of_pawns.append(type)
        self.pawns_types = []
        for pawntype in self.types_of_pawns:
            self.pawns_types.append(pawntype.get("type", "unknow"))
    
    def get_all_pawns_types(self) -> list[str]:
        return self.pawns_types
    
    def get_all_pawns_sample(self) -> list[dict]:
        return self.types_of_pawns
    
    def get_pawn_sample_by_type(self, pawn_type: str) -> dict:
        for type in self.types_of_pawns:
            if type["type"] == pawn_type:
                return copy.deepcopy(type)
        logger.error(f"{pawn_type} does not exist", f"PawnManager({pawn_type})")
        return {}

    def get_pawn_by_id(self, id: int) -> Pawn:
        for pawn in self.pawns:
            if pawn.id == id:
                return pawn
        logger.error(f"pawn id not found {id}", f"PawnsManager.get_pawn_by_id({id})")
        return self._default_pawn

    def get_pawn_by_type(self, pawn_type: str, coord: tuple[int, int, int]) -> Pawn:
        for pawn in self.pawns:
            if pawn.type == pawn_type and pawn.coord == coord:
                return pawn
        logger.error(f"pawn not found {pawn_type} {coord}", f"PawnsManager.get_pawn_by_name({pawn_type}, {coord})")
        return self._default_pawn
    
    def get_pawn_by_coord(self, pawn_type: str, coord: tuple[int, int, int]) -> Pawn:
        for pawn in self.pawns:
            if pawn.coord == coord and pawn.type == pawn_type:
                return pawn
        logger.error(f"pawn not found {pawn_type} {coord}", f"PawnsManager.get_pawn_by_name({pawn_type}, {coord})")
        return self._default_pawn
    
    def get_pawns_by_coord(self, coord: tuple[int, int, int]) -> list[Pawn]:
        pawns = []
        for pawn in self.pawns:
            if pawn.coord == coord:
                pawns.append(pawn)
        return pawns

    def spawn(self, data: str|dict, coord: tuple[int, int, int], fraction_id: int) -> bool:
        '''
        use data str to spawn standart pawn
        use data dict to spawn pawn with specials characteristics
        '''
        root.game_manager.fraction_manager.get_fraction_by_id(fraction_id).statistics["pawn_count"] += 1 #type: ignore
        if isinstance(data, str):
            for type in self.types_of_pawns:
                if data == type["type"]:
                    self._spawn(copy.deepcopy(type), coord, fraction_id)
                    return True
        else:
            self._spawn(data, coord, fraction_id)
            return True
        return False
    
    def _spawn(self, data: dict, coord: tuple[int, int, int], fraction_id: int):
        data = data.copy()
        data["fraction_id"] = fraction_id
        cell = root.game_manager.world_map.get_cell_by_coord(coord)
        pawn_id = self.available_pawn_id
        self.available_pawn_id += 1
        data["id"] = pawn_id
        data["coord"] = coord

        self.pawns.append(Pawn(pawn_id, coord, data, False))
        cell.add_pawn(data)
        logger.info(f"Spawned pawn id {pawn_id} of type {data.get('type', 'unknown')} at {coord}", f"PawnsManager._spawn({data}, {coord}, {fraction_id})")

    def despawn(self, id: int):
        for pawn in self.pawns:
            if pawn.id == id:
                root.game_manager.fraction_manager.get_fraction_by_id(pawn.fraction_id).statistics["pawn_count"] -= 1 #type: ignore
                self.pawns.remove(pawn)
                cell = root.game_manager.world_map.get_cell_by_coord(pawn.coord)
                cell.remove_pawn(id) #type: ignore
                logger.info(f"Despawned pawn id {id} from {pawn.coord}", f"PawnsManager.despawn({id})")
                return
        logger.error(f"Trying to despawn non-existing pawn with id {id}", f"PawnsManager.despawn({id})")

    def restore_movement_points(self, pawn: Pawn) -> str:
        pawn.data["movement_points"] = pawn.data["movement_points_max"]
        cell = root.game_manager.world_map.get_cell_by_coord(pawn.coord)
        for pawn_ in cell.pawns:
            if pawn_["id"] == pawn.id:
                pawn_["movement_points"] = pawn.data["movement_points"]
        return f"movement points by pawn {pawn.name} [{pawn.type} {pawn.id}] successfully restored to {pawn.data["movement_points"]}"
    
    def add_resource(self, pawn_:int|Pawn, resource:str, amout:int) -> str:
        if isinstance(pawn_, int):
            for pawn in self.pawns:
                if pawn_ == pawn.id:
                    pawn.add_resource(resource, amout)
                    return f"pawn {pawn.id} received {resource} in quantity {amout}"
        elif isinstance(pawn_, Pawn):
            for pawn in self.pawns:
                if pawn_ == pawn:
                    pawn.add_resource(resource, amout)
                    return f"pawn {pawn.id} received {resource} in quantity {amout}"
        return f"pawn {pawn_} not found"
    
    def remove_resource(self, pawn_:int|Pawn, resource:str, amout:int):
        if isinstance(pawn_, int):
            for pawn in self.pawns:
                if pawn_ == pawn.id:
                    pawn.remove_resource(resource, amout)
                    return f"pawn {pawn.id} lost {resource} in quantity {amout}"
        elif isinstance(pawn_, Pawn):
            for pawn in self.pawns:
                if pawn_ == pawn:
                    pawn.remove_resource(resource, amout)
                    return f"pawn {pawn.id} lost {resource} in quantity {amout}"
        return f"pawn {pawn_} not found"

    def move_pawn(self, pawn: Pawn, new_cell: Cell):
        old_cell = root.game_manager.world_map.get_cell_by_coord(pawn.coord)
        old_cell.remove_pawn(pawn.id)

        pawn.coord = new_cell.coord
        pawn.data["coord"] = new_cell.coord
        new_cell.add_pawn(pawn.data)
        
        pawn.data["movement_points"] = new_cell.data["subdata"]["movement_points"]
        root.game_manager.world_map.unmark_region("for_move")
        root.game_manager.turn_manager.add_event_in_queue(1, {"do": "restore_movement_points", "event_data": {"pawn": pawn}})
        root.game_manager.reset_opened_pawn()
        
        logger.info(f"{pawn} moved from {old_cell} to {new_cell}", f"PawnsManager.move_pawn(...)")
        return f"pawn {pawn.name} ({pawn.id} moved from {old_cell.coord} to {new_cell.coord}) and has rest {pawn.data["movement_points"]} movement_points"

    def try_to_move_pawn(self, pawn: Pawn, new_cell: Cell) -> bool:
        if pawn.fraction_id != root.player_id: return False
        if new_cell in root.game_manager.world_map.marked_region["for_move"]:
            if new_cell.pawns != [] or new_cell.buildings != {}:
                return False
            self.move_pawn(pawn, new_cell)
            return True
        return False
    
    def do_job(self, pawn: Pawn, job_name: str):
        root.game_manager.gui.close_all_extra_windows()
        job_id = root.game_manager.job_manager.get_job_id_from_name(job_name)
        if root.game_manager.job_manager.is_job_available(job_name, pawn):
            job = root.game_manager.job_manager.get_job_by_id(job_id)

            if not self._process_pawn_movement_point_for_job(job, job_id, pawn): return #if pawn has not enought movements points

            self._execute_job(job, job_name)
            
            root.game_manager.world_map.unmark_region("for_move")
            root.game_manager.gui.close_all_extra_windows()
            logger.info(f"Pawn '{pawn.id}' will do job '{job_id}'", f"PawnsManager.do_job({pawn}, {job_id})")
    
    def _execute_job(self, job: dict, job_name: str):
        if isinstance(job["result"], dict):
            result = root.game_manager.job_manager.procces_result(job, job_name)["result"]
            root.game_manager.turn_manager.add_event_in_queue(job["work_time"], {"do": result["type"], "event_data": result["args"]})
        else:
            for result in job["result"]:
                temp_job_dict = job
                temp_job_dict["result"] = result
                result = root.game_manager.job_manager.procces_result(temp_job_dict, job_name)["result"]
                root.game_manager.turn_manager.add_event_in_queue(job["work_time"], {"do": result["type"], "event_data": result["args"]})
    
    def _process_pawn_movement_point_for_job(self, job: dict, job_id: str, pawn: Pawn) -> bool:
        if job.get("movement_points_cost", False):
            if job["movement_points_cost"] == "all":
                pawn.data["movement_points"] = 0
            else:
                if pawn.data["movement_points"] - job["movement_points_cost"] < 0:
                    logger.warning(f"Pawn '{pawn.id}' cannot do job '{job_id}' due to insufficient movement points.", f"PawnsManager.do_job({pawn}, {job_id})")
                    return False
                pawn.data["movement_points"] -= job["movement_points_cost"]
                root.game_manager.turn_manager.add_event_in_queue(job["work_time"], {"do": "restore_movement_points", "event_data": {"pawn": pawn}})
        return True
    
    #def do_job(self, pawn: Pawn, job_id:str):
    #    if root.game_manager.job_manager.is_job_available(job_id, pawn):
    #        job = root.game_manager.job_manager.get_job_by_id(root.game_manager.job_manager.get_job_id_from_name(job_id))
    #        if job != None:
    #            result = job["result"]
    #            result["args"]["pawn"] = pawn
    #            if job.get("movement_points_cost", False):
    #                if job["movement_points_cost"] == "all":
    #                    pawn.data["movement_points"] = 0
    #                elif isinstance(int, job["movement_points_cost"]):
    #                    pawn.data["movement_points"] -= job["movement_points_cost"]
    #                    if pawn.data["movement_points"] < 0:
    #                        logger.warning(f"Pawn '{pawn.id}' cannot do job '{job_id}' due to insufficient movement points.", f"PawnsManager.do_job({pawn}, {job_id})")
    #                        #print(f"pawn {pawn["id"]} can not do this job. Not enought movement points")
    #                        pawn.data["movement_points"] += job["movement_points_cost"]
    #                        return
    #
    #            root.game_manager.turn_manager.add_event_in_queue(job["work_time"], {"do": result["type"], "event_data": result["args"]}) #job event
    #            root.game_manager.turn_manager.add_event_in_queue(job["work_time"], {"do": "restore_movement_points", "event_data": {"pawn": pawn}}) #pawn movement points event
    #
    #            root.game_manager.world_map.unmark_region("for_move")
    #
    #            root.game_manager.gui.close_all_extra_windows()
    #            logger.info(f"Pawn '{pawn.id}' will do job '{job_id}'", f"PawnsManager.do_job({pawn}, {job_id})")
    #            #print(f"pawn {pawn["id"]} will do {result["type"]} with args: {result["args"]} and finish after {job["work_time"]} turn(s)")
    #    else:
    #        logger.warning(f"Pawn '{pawn.id}' cannot do job '{job_id}' as it is not available.", f"PawnsManager.do_job({pawn}, {job_id})")
    #        #print(f"pawn {pawn["id"]} can not do this job")
    #    return