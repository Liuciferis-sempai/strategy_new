import os
from assets.work_with_files import read_json_file
from .pawn import Pawn
from assets.world.cell import Cell
from assets import root
from assets.root import loading, logger

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
        logger.error(f"pawn id not found {id}", f"PawnsManager.get_pawn_by_id({id})")
        return Pawn()

    def get_pawn_by_name(self, name: str, coord: tuple[int, int]) -> Pawn:
        for pawn in self.pawns:
            if pawn.data.get("name", "") == name and pawn.coord == coord:
                return pawn
        logger.error(f"pawn not found {name} {coord}", f"PawnsManager.get_pawn_by_name({name}, {coord})")
        return Pawn()

    def spawn(self, data: str, coord: tuple[int, int], fraction_id: int) -> bool:
        '''
        use data str to spawn standart pawn
        use data dict to spawn pawn with specials characteristics
        '''
        root.game.allFractions.get_fraction_by_id(fraction_id).statistics["pawn_count"] += 1 #type: ignore
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
        cell = root.game.world_map.get_cell_by_coord(coord)
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
                root.game.allFractions.get_fraction_by_id(pawn.fraction_id).statistics["pawn_count"] -= 1 #type: ignore
                self.pawns.remove(pawn)
                cell = root.game.world_map.get_cell_by_coord(pawn.coord)
                cell.remove_pawn(id) #type: ignore
                logger.info(f"Despawned pawn id {id} from {pawn.coord}", f"PawnsManager.despawn({id})")
                return
        logger.error(f"Trying to despawn non-existing pawn with id {id}", f"PawnsManager.despawn({id})")

    def restore_movement_points(self, pawn: Pawn):
        for p in self.pawns:
            if p.id == pawn.id:
                p.data["movement_points"] = p.data["movement_points_max"]
                cell = root.game.world_map.get_cell_by_coord(pawn.coord)
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
        old_cell = root.game.world_map.get_cell_by_coord(pawn.coord)
        old_cell.remove_pawn(pawn.id)

        pawn.coord = new_cell.coord
        pawn.data["coord"] = new_cell.coord
        new_cell.add_pawn(pawn.data)
        
        pawn.data["movement_points"] = new_cell.data["subdata"]["movement_points"]
        root.game.world_map.unmark_region("for_move")
        root.game.turn_manager.add_event_in_queue(1, {"do": "restore_movement_points", "event_data": {"target": pawn}})
        root.game.reset_opened_pawn()
        
        logger.info(f"{pawn} moved from {old_cell} to {new_cell}", f"PawnsManager.move_pawn(...)")

    def try_to_move_pawn(self, pawn: Pawn, new_cell: Cell):
        if new_cell in root.game.world_map.marked_region["for_move"]:
            if new_cell.pawns != [] or new_cell.buildings != {}:
                root.game.gui.game.set_target_coord(new_cell.coord)
                root.game.gui.game.show_actions(new_cell.pawns, new_cell.buildings)
                return
            self.move_pawn(pawn, new_cell)

    def do_job(self, pawn: Pawn, job_id:str):
        if root.game.job_manager.is_job_available(job_id, pawn):
            job = root.game.job_manager.get_job_by_id(root.game.job_manager.get_job_id_from_name(job_id))
            if job != None:
                result = job["result"]
                result["args"]["target"] = pawn
                if job.get("movement_points_cost", False):
                    if job["movement_points_cost"] == "all":
                        pawn.data["movement_points"] = 0
                    elif isinstance(int, job["movement_points_cost"]):
                        pawn.data["movement_points"] -= job["movement_points_cost"]
                        if pawn.data["movement_points"] < 0:
                            logger.warning(f"Pawn '{pawn.id}' cannot do job '{job_id}' due to insufficient movement points.", f"PawnsManager.do_job({pawn}, {job_id})")
                            #print(f"pawn {pawn["id"]} can not do this job. Not enought movement points")
                            pawn.data["movement_points"] += job["movement_points_cost"]
                            return

                root.game.turn_manager.add_event_in_queue(job["work_time"], {"do": result["type"], "event_data": result["args"]}) #job event
                root.game.turn_manager.add_event_in_queue(1, {"do": "restore_movement_points", "event_data": {"target": pawn}}) #pawn movement points event

                root.game.world_map.unmark_region("for_move")

                root.game.gui.close_all_extra_windows()
                logger.info(f"Pawn '{pawn.id}' will do job '{job_id}'", f"PawnsManager.do_job({pawn}, {job_id})")
                #print(f"pawn {pawn["id"]} will do {result["type"]} with args: {result["args"]} and finish after {job["work_time"]} turn(s)")
        else:
            logger.warning(f"Pawn '{pawn.id}' cannot do job '{job_id}' as it is not available.", f"PawnsManager.do_job({pawn}, {job_id})")
            #print(f"pawn {pawn["id"]} can not do this job")
        return