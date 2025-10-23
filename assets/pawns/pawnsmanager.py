import os
from assets.work_with_files import read_json_file
from .pawn import Pawn
from assets.world.cell import Cell
from assets import root
from assets.functions import logging
from assets.root import loading

class PawnsManager:
    def __init__(self):
        self.pawns = []
        self.types_of_pawns = []
        self.available_pawn_id = 0

        loading.draw("Loading pawn types...")
        self.load_types_of_pawns()

    def load_types_of_pawns(self):
        self.types_of_pawns = []
        for pawnsfile in os.listdir("data/pawns/data"):
            if pawnsfile.endswith(".json"):
                type = read_json_file(f"data/pawns/data/{pawnsfile}")
                self.types_of_pawns.append(type)

    def get_pawn_by_id(self, id: int) -> Pawn:
        for pawn in self.pawns:
            if pawn.id == id:
                return pawn
        logging("ERROR", f"pawn id not found {id}", "PawnsManager.get_pawn_by_id")
        return Pawn()

    def get_pawn_by_name(self, name: str, coord: tuple[int, int]) -> Pawn:
        for pawn in self.pawns:
            if pawn.data.get("name", "") == name and pawn.coord == coord:
                return pawn
        logging("ERROR", f"pawn not found {name} {coord}", "PawnsManager.get_pawn_by_name")
        return Pawn()

    def spawn(self, data: str, coord: tuple[int, int], fraction_id: int) -> bool:
        '''
        use data str to spawn standart pawn
        use data dict to spawn pawn with specials characteristics
        '''
        root.handler.allFractions.get_fraction_by_id(fraction_id).statistics["pawn_count"] += 1 #type: ignore
        for type in self.types_of_pawns:
            if data == type["name"] or data == type:
                if isinstance(data, str):
                    self._spawn(type, coord, fraction_id)
                else:
                    self._spawn(data, coord, fraction_id)
                return True
        return False
    
    def _spawn(self, data: dict, coord: tuple[int, int], fraction_id: int):
        data = data.copy()
        data["fraction_id"] = fraction_id
        cell = root.handler.world_map.get_cell_by_coord(coord)
        if cell != None:
            pawn_id = self.available_pawn_id
            self.available_pawn_id += 1
            data["id"] = pawn_id
            data["coord"] = coord

            self.pawns.append(Pawn(pawn_id, coord, data, False))
            cell.add_pawn(data)
            logging("INFO", f"Spawned pawn id {pawn_id} of type {data.get('type', 'unknown')} at {coord}", "PawnsManager._spawn")

    def despawn(self, id: int):
        for pawn in self.pawns:
            if pawn.id == id:
                root.handler.allFractions.get_fraction_by_id(pawn.fraction_id).statistics["pawn_count"] -= 1 #type: ignore
                self.pawns.remove(pawn)
                cell = root.handler.world_map.get_cell_by_coord(pawn.coord)
                cell.remove_pawn(id) #type: ignore
                logging("INFO", f"Despawned pawn id {id} from {pawn.coord}", "PawnsManager.despawn")
                return
        logging("ERROR", f"Trying to despawn non-existing pawn with id {id}", "PawnsManager.despawn")

    def restore_movement_points(self, pawn: Pawn):
        for p in self.pawns:
            if p.id == pawn.id:
                p.data["movement_points"] = p.data["movement_points_max"]
                cell = root.handler.world_map.get_cell_by_coord(pawn.coord)
                if cell != None:
                    for pawn_ in cell.pawns:
                        pawn_["movement_points"] = p.data["movement_points"]
    
    def add_resource(self, pawn_:int|Pawn, resource:str, amout:int):
        if isinstance(pawn_, int):
            for pawn in self.pawns:
                if pawn_ == pawn.id:
                    pawn.add_resource(resource, amout)
        elif isinstance(pawn_, Pawn):
            for pawn in self.pawns:
                if pawn_ == pawn:
                    pawn.add_resource(resource, amout)

    def move_pawn(self, pawn: Pawn, new_cell: Cell):
        old_cell = root.handler.world_map.get_cell_by_coord(pawn.coord)
        old_cell.remove_pawn(pawn.id)

        pawn.coord = new_cell.coord
        pawn.data["coord"] = new_cell.coord
        new_cell.add_pawn(pawn.data)
        pawn.data["movement_points"] = new_cell.data["subdata"]["movement_points"]
        root.handler.world_map.unmark_region("for_move")
        root.handler.turn_manager.add_event_in_queue(1, {"do": "restore_movement_points", "event_data": {"target": pawn}})
        root.handler.reset_opened_pawn()

    def try_to_move_pawn(self, pawn: Pawn, new_cell):
        if new_cell in root.handler.world_map.marked_region["for_move"]:
            if new_cell.pawns != [] or new_cell.buildings != {}:
                root.handler.gui.game.set_target_coord(new_cell.coord)
                root.handler.gui.game.show_actions(new_cell.pawns, new_cell.buildings)
                return
            self.move_pawn(pawn, new_cell)

    def do_job(self, pawn: Pawn, job_id:str):
        if root.handler.job_manager.is_job_available(job_id, pawn):
            job = root.handler.job_manager.get_job_by_id(root.handler.job_manager.get_job_id_from_name(job_id))
            if job != None:
                result = job["result"]
                result["args"]["target"] = pawn
                if job.get("movement_points_cost", False):
                    if job["movement_points_cost"] == "all":
                        pawn.data["movement_points"] = 0
                    elif isinstance(int, job["movement_points_cost"]):
                        pawn.data["movement_points"] -= job["movement_points_cost"]
                        if pawn.data["movement_points"] < 0:
                            logging("DEBUG", f"Pawn {pawn.id} cannot do job {job_id} due to insufficient movement points.", "PawnsManager.do_job", f"Required: {job['movement_points_cost']}, Available: {pawn.data['movement_points'] + job['movement_points_cost']}")
                            #print(f"pawn {pawn["id"]} can not do this job. Not enought movement points")
                            pawn.data["movement_points"] += job["movement_points_cost"]
                            return

                root.handler.turn_manager.add_event_in_queue(job["work_time"], {"do": result["type"], "event_data": result["args"]}) #job event
                root.handler.turn_manager.add_event_in_queue(1, {"do": "restore_movement_points", "event_data": {"target": pawn}}) #pawn movement points event

                root.handler.world_map.unmark_region("for_move")

                root.handler.gui.game.hide_jobs()
                root.handler.gui.game.main_info_window_content_close()
                logging("INFO", f"Pawn {pawn.id} will do job {job_id}", "PawnsManager.do_job", f"Job result: {result}, work time: {job['work_time']}")
                #print(f"pawn {pawn["id"]} will do {result["type"]} with args: {result["args"]} and finish after {job["work_time"]} turn(s)")
        else:
            logging("DEBUG", f"Pawn {pawn.id} cannot do job {job_id} as it is not available.", "PawnsManager.do_job")
            #print(f"pawn {pawn["id"]} can not do this job")
        return