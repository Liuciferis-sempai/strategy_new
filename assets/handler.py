from assets import root
from assets.root import loading
from assets.functions import logging
from assets.gui.gui_manager import GUI
from assets.pawns.pawnsmanager import PawnsManager
from assets.pawns.pawn import Pawn
from assets.reciepts.reciept import RecieptsManager
from assets.turn_manager.turnmanager import TurnManager
from assets.world.worldmap import WorldMap
from assets.world.cell import Cell
from assets.triggers.triggermanager import TriggerManager
from assets.fraction.fraction_manager import AllFactions, Fraction
from assets.technologies.techtree import Techtree
from assets.buildings.buildingsmanager import BuildingsManager
from assets.policy.policytable import PolicyTable
from assets.effects.effectmanager import EffectManager
from assets.jobs.jobmanager import JobManager
from assets.resources.resourcemanager import ResourceManager
from assets.proccessing_input import InputKeyProcessor


class Handler:
    def __init__(self):
        loading.draw("Loading variables...")
        self.chosen_cell = Cell()
        self.chosen_cell_coord = self.chosen_cell.coord
        self.opened_pawn = Pawn()
        self.opened_pawn_coord = self.opened_pawn.coord

        loading.draw("Loading handler...")
        self.allFractions = AllFactions()
        self.world_map = WorldMap()
        self.gui = GUI()
        self.pawns_manager = PawnsManager()
        self.reciept_manager = RecieptsManager()
        self.turn_manager = TurnManager()
        self.trigger_manager = TriggerManager()
        self.tech_tree = Techtree()
        self.buildings_manager = BuildingsManager()
        self.policy_table = PolicyTable()
        self.effect_manager = EffectManager()
        self.job_manager = JobManager()
        self.resource_manager = ResourceManager()
        self.input_processor = InputKeyProcessor()
    
    def update_positions(self):
        self.gui.change_position_for_new_screen_sizes()
        self.policy_table.update_positions()

    def set_chosen_cell(self, new_chosen_cell: Cell):
        logging("INFO", f"chosen cell changed from {self.chosen_cell} to {new_chosen_cell}", "Handler.set_chosen_cell")
        self.chosen_cell = new_chosen_cell
        self.chosen_cell_coord = self.chosen_cell.coord
    
    def get_chosen_cell(self) -> Cell:
        if self.chosen_cell.is_default:
            logging("ERROR", f"query chosen cell before it is defined", "Handler.get_chosen_cell")
        else:
            logging("INFO", f"query chosen cell: {self.chosen_cell}", "Handler.get_chosen_cell")
        return self.chosen_cell
    
    def reset_chosen_cell(self):
        logging("INFO", "chosen cell reset", "Handler.reset_chosen_cell")
        self.chosen_cell = Cell()
        self.chosen_cell_coord = self.chosen_cell.coord
    
    def get_chosen_cell_coord(self) -> tuple[int, int]:
        if self.chosen_cell.is_default:
            logging("ERROR", f"query chosen cell coord before chosen cell is defined", "Handler.get_chosen_cell_coord")
        else:
            logging("INFO", f"query chosen cell coord: {self.chosen_cell_coord}", "Handler.get_chosen_cell_coord")
        return self.chosen_cell_coord
    
    def is_chosen_cell_default(self) -> bool:
        return self.chosen_cell.is_default
    
    def get_opened_pawn(self) -> Pawn:
        if self.opened_pawn.is_default:
            logging("ERROR", f"query opened pawn before it is defined", "Handler.get_opened_pawn")
        else:
            logging("INFO", f"query opened pawn: {self.opened_pawn}", "Handler.get_opened_pawn")
        return self.opened_pawn
    
    def get_opened_pawn_coord(self) -> tuple[int, int]:
        if self.opened_pawn.is_default:
            logging("ERROR", f"query opened pawn before it is defined", "Handler.get_opened_pawn_coord")
        else:
            logging("INFO", f"query opened pawn: {self.opened_pawn_coord}", "Handler.get_opened_pawn_coord")
        return self.opened_pawn_coord
    
    def is_opened_pawn_default(self) -> bool:
        if self.opened_pawn.is_default:
            logging("WARNING", "opened pawn is default", "Handler.is_opened_pawn_default", f"self.opened_pawn: {self.opened_pawn} ,self.opened_pawn.is_default: {self.opened_pawn.is_default}")
        return self.opened_pawn.is_default
    
    def set_opened_pawn(self, new_pawn: Pawn|dict):
        logging("INFO", f"open pawn {new_pawn}", "Handler.set_opened_pawn")
        if isinstance(new_pawn, dict):
            new_pawn = self.pawns_manager.get_pawn_by_id(new_pawn["id"]) #type: ignore
            logging("INFO", f"new pawn was dict. now is {new_pawn}", "Handler.set_opened_pawn")
            if new_pawn.is_default:
                logging("ERROR", "new pawn is default. Something is wrong", "Handler.set_opened_pawn")

        if isinstance(new_pawn, Pawn):
            logging("INFO", f"opened pawn changed from {self.opened_pawn} to {new_pawn}", "Handler.set_opened_pawn")
            self.opened_pawn = new_pawn
            self.opened_pawn_coord = self.opened_pawn.coord
            if self.opened_pawn.is_default:
                logging("ERROR", "new pawn is default. Something is wrong", "Handler.set_open_pawn")
        else:
            logging("ERROR", f"attempt to assign an impossible value to opened pawn", "Handler.set_opened_pawn", f"new value: {new_pawn}")

    def update_opened_pawn_coord(self):
        self.opened_pawn_coord = self.opened_pawn.coord

    def reset_opened_pawn(self):
        logging("INFO", "opened pawn reset", "Handler.reset_opened_pawn")
        self.opened_pawn = Pawn()
        self.opened_pawn_coord = self.opened_pawn.coord