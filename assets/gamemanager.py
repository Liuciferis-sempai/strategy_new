from assets.root import logger
from assets.root import loading
from assets.gui.gui_manager import GUI
from assets.pawns.pawnsmanager import PawnsManager
from assets.pawns.pawn import Pawn
from assets.reciepts.reciept import RecieptsManager
from assets.turn_manager.turnmanager import TurnManager
from assets.world.worldmap import WorldMap
from assets.world.cell import Cell
from assets.gui.inputfield import InputField
from assets.triggers.triggermanager import TriggerManager
from assets.fraction.fraction_manager import FractionManager, Fraction
from assets.technologies.techtree import Techtree
from assets.buildings.buildingsmanager import BuildingsManager
from assets.policy.policytable import PolicyTable
from assets.effects.effectmanager import EffectManager
from assets.jobs.jobmanager import JobManager
from assets.resources.resourcemanager import ResourceManager
from assets.processing_input.proccessing_input import InputKeyProcessor
from assets.command_line.command_line import CommandLine
from assets.towns.towns_manager import TownManager

class GameManager:
    def __init__(self):
        loading.draw("Loading game manager...")
        self.game_name = "Noname"

        self._default_cell = Cell()
        self._default_pawn = Pawn()
        self._default_chosen_inputfield = InputField()
        self.chosen_cell = self._default_cell
        self.chosen_cell_coord = self.chosen_cell.coord
        self.opened_pawn = self._default_pawn
        self.opened_pawn_coord = self.opened_pawn.coord
        self.targets_coord = (-1, -1)
        self.chosen_inputfield = self._default_chosen_inputfield

        self.input_fields: list[InputField] = []

        loading.draw("Loading other managers...")
        self.fraction_manager = FractionManager()
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
        self.town_manager = TownManager()

        self.command_line = CommandLine()
        self.input_fields.append(self.command_line.inputfield)

    def draw(self):
        self.gui.draw()
        if self.command_line.is_active:
            self.command_line.draw()
        for input in self.input_fields:
            if not input.hidden:
                input.draw()
    
    def update_positions(self):
        self.gui.change_position_for_new_screen_sizes()
        self.gui.policy.update_positions()

    def set_chosen_cell(self, new_chosen_cell: Cell):
        logger.info(f"chosen cell changed from {self.chosen_cell} to {new_chosen_cell}", f"Game.set_chosen_cell({new_chosen_cell})")
        self.chosen_cell = new_chosen_cell
        self.chosen_cell_coord = self.chosen_cell.coord
    
    def get_chosen_cell(self) -> Cell:
        if self.chosen_cell.is_default:
            logger.error(f"query chosen cell before it is defined", "Game.get_chosen_cell()")
        #else:
        #    logger.info(f"query chosen cell: {self.chosen_cell}", "Game.get_chosen_cell()")
        return self.chosen_cell
    
    def reset_chosen_cell(self, call_uncose_cell: bool = True):
        logger.info("chosen cell reset", "Game.reset_chosen_cell()")
        if call_uncose_cell:
            self.world_map.unchose_cell()
        self.chosen_cell = self._default_cell
        self.chosen_cell_coord = self.chosen_cell.coord
    
    def get_chosen_cell_coord(self) -> tuple[int, int]:
        if self.chosen_cell.is_default:
            logger.error(f"query chosen cell coord before chosen cell is defined", "Game.get_chosen_cell_coord()")
        #else:
        #    logger.info(f"query chosen cell coord: {self.chosen_cell_coord}", "Game.get_chosen_cell_coord()")
        return self.chosen_cell_coord
    
    def is_chosen_cell_default(self) -> bool:
        return self.chosen_cell.is_default
    
    def get_opened_pawn(self) -> Pawn:
        if self.opened_pawn.is_default:
            logger.error(f"query opened pawn before it is defined", "Game.get_opened_pawn()")
        #else:
        #    logger.info(f"query opened pawn: {self.opened_pawn}", "Game.get_opened_pawn()")
        return self.opened_pawn
    
    def get_opened_pawn_coord(self) -> tuple[int, int]:
        if self.opened_pawn.is_default:
            logger.error(f"query opened pawn coord before it is defined", "Game.get_opened_pawn_coord()")
        #else:
        #    logger.info(f"query opened pawn: {self.opened_pawn_coord}", "Game.get_opened_pawn_coord()")
        return self.opened_pawn_coord
    
    def is_opened_pawn_default(self) -> bool:
        if self.opened_pawn.is_default:
            logger.warning("opened pawn is default", "Game.is_opened_pawn_default()")
        return self.opened_pawn.is_default
    
    def set_opened_pawn(self, new_pawn: Pawn|dict):
        logger.info(f"open pawn {new_pawn}", f"Game.set_opened_pawn({new_pawn})")
        if isinstance(new_pawn, dict):
            new_pawn = self.pawns_manager.get_pawn_by_id(new_pawn["id"]) #type: ignore
            logger.info(f"new pawn was dict. now is {new_pawn}", f"Game.set_opened_pawn({new_pawn})")
            if new_pawn.is_default:
                logger.error("new pawn is default. Something is wrong", f"Game.set_opened_pawn({new_pawn})")

        if isinstance(new_pawn, Pawn):
            logger.info(f"opened pawn changed from {self.opened_pawn} to {new_pawn}", f"Game.set_opened_pawn({new_pawn})")
            self.opened_pawn = new_pawn
            self.opened_pawn_coord = self.opened_pawn.coord
            if self.opened_pawn.is_default:
                logger.error("new pawn is default. Something is wrong", f"Game.set_open_pawn({new_pawn})")
        else:
            logger.error(f"attempt to assign an impossible value to opened pawn", f"Game.set_opened_pawn({new_pawn})")
        self.update_opened_pawn_coord()

    def update_opened_pawn_coord(self):
        self.opened_pawn_coord = self.opened_pawn.coord

    def reset_opened_pawn(self):
        logger.info("opened pawn reset", "Game.reset_opened_pawn()")
        self.opened_pawn = self._default_pawn
        self.opened_pawn_coord = self.opened_pawn.coord

    def get_target_coord(self):
        if self.is_target_coord_default():
            logger.error(f"query target coord before it is defined", "Game.get_target_coord()")
        return self.targets_coord
    
    def set_target_coord(self, new_target_coord: tuple[int, int]):
        logger.info(f"target coord changet from {self.targets_coord} to {new_target_coord}", f"GUIGame.set_target_coord({new_target_coord})")
        self.targets_coord = new_target_coord

    def reset_target_coord(self):
        logger.info(f"target coord reset", "GUIGame.set_target_coord_null()")
        self.targets_coord = (-1, -1)
    
    def is_target_coord_default(self):
        if self.targets_coord == (-1, -1):
            logger.warning("target coord is default", "Game.is_target_coord_default()")
            return True
        return False
    
    def get_chosen_inputfield(self):
        if self.is_chosen_inputfield_default():
            logger.error("query chosen inputfield  before it is defined", "Game.get_chosen_inputfield()")
        return self.chosen_inputfield

    def is_chosen_inputfield_default(self):
        return self.chosen_inputfield == self._default_chosen_inputfield
    
    def chose_input_field(self, inputfield: InputField):
        self.chosen_inputfield = inputfield
    
    def reset_chosen_inputfield(self):
        self.chosen_inputfield = self._default_chosen_inputfield
    
    def add_inputfield(self, inputfield: InputField):
        self.input_fields.append(inputfield)