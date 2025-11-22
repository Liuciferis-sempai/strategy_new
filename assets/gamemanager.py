from .root import logger, loading
from . import root
from .gui.gui_manager import GUI
from .managers.pawns.pawnsmanager import PawnsManager
from .managers.pawns.pawn import Pawn
from .managers.reciept import RecieptsManager
from .managers.turnmanager import TurnManager
from .world.worldmap import WorldMap
from .world.cell import Cell
from .gui.inputfield import InputField
from .managers.triggermanager import TriggerManager
from .managers.fraction.fraction_manager import FractionManager, Fraction
from .managers.technologies.techtree import Techtree
from .managers.buildings.buildingsmanager import BuildingsManager
from .managers.buildings.building import Building
from .managers.policy.policytable import PolicyTable
from .managers.effectmanager import EffectManager
from .managers.jobmanager import JobManager
from .managers.resources.resourcemanager import ResourceManager
from .processing_input.proccessing_input import InputKeyProcessor
from .helpers.command_line import CommandLine
from .managers.towns.towns_manager import TownManager
from .helpers.messenger import Messenger

class GameManager:
    def __init__(self):
        '''
        Main Manager of game
        '''
        self.game_name = "Noname"

        self._default_cell = Cell(is_default=False)
        self._default_cell.is_default = True
        self._default_pawn = Pawn(is_default=False)
        self._default_pawn.is_default = True
        self._default_building = Building(is_default=False)
        self._default_building.is_default = True
        self._default_fraction = Fraction(is_default=False)
        self._default_fraction.is_default = True

        self._default_chosen_inputfield = InputField()

        self.chosen_cell = self._default_cell
        self.chosen_cell_coord = self.chosen_cell.coord
        self.chosen_pawn = self._default_pawn
        self.chosen_pawn_coord = self.chosen_pawn.coord
        self.chosen_building = self._default_building
        self.chosen_building_coord = self.chosen_building.coord
        self.targets_coord = (-1, -1, -1)
        self.chosen_inputfield = self._default_chosen_inputfield

        self.input_fields: list[InputField] = []

        self.messenger = Messenger()
        self.world_map = WorldMap()

        self.command_line = CommandLine()
        self.input_fields.append(self.command_line.inputfield)

        self.fraction_manager = FractionManager(self)
        self.gui = GUI(self)
        self.pawns_manager = PawnsManager(self)
        self.reciept_manager = RecieptsManager(self)
        self.turn_manager = TurnManager(self)
        self.trigger_manager = TriggerManager(self)
        self.tech_tree = Techtree(self)
        self.buildings_manager = BuildingsManager(self)
        self.policy_table = PolicyTable(self)
        self.effect_manager = EffectManager(self)
        self.job_manager = JobManager(self)
        self.resource_manager = ResourceManager(self)
        self.input_processor = InputKeyProcessor(self)
        self.town_manager = TownManager(self)

        logger.info("gamemanager ended initialization", "GameManager.initialize()")

    def draw(self):
        self.gui.draw()
        if self.command_line.is_active:
            self.command_line.draw()
        self.messenger.draw()
        #for input in self.input_fields:
        #    if not input.hidden:
        #        input.draw()
    
    def update_positions(self):
        self.gui.change_position_for_new_screen_sizes()
        self.gui.policy.update_positions()
        self.command_line.change_position_for_new_screen_sizes()

    def get_default_cell(self) -> Cell:
        return self._default_cell
    
    def get_default_pawn(self) -> Pawn:
        return self._default_pawn
    
    def get_default_building(self) -> Building:
        return self._default_building
    
    def get_default_fraction(self) -> Fraction:
        return self._default_fraction

    def set_chosen_cell(self, new_chosen_cell: "Cell"):
        logger.info(f"chosen cell changed from {self.chosen_cell} to {new_chosen_cell}", f"Game.set_chosen_cell({new_chosen_cell})")
        self.chosen_cell = new_chosen_cell
        self.chosen_cell_coord = self.chosen_cell.coord
    
    def get_chosen_cell(self) -> Cell:
        if not self.chosen_cell:
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
    
    def get_chosen_cell_coord(self) -> tuple[int, int, int]:
        if not self.chosen_cell:
            logger.error(f"query chosen cell coord before chosen cell is defined", "Game.get_chosen_cell_coord()")
        #else:
        #    logger.info(f"query chosen cell coord: {self.chosen_cell_coord}", "Game.get_chosen_cell_coord()")
        return self.chosen_cell_coord
    
    def is_chosen_cell_default(self) -> bool:
        return self.chosen_cell.is_default
    
    def get_chosen_pawn(self) -> Pawn:
        if not self.chosen_pawn:
            logger.error(f"query opened pawn before it is defined", "Game.get_chosen_pawn()")
        #else:
        #    logger.info(f"query opened pawn: {self.chosen_pawn}", "Game.get_chosen_pawn()")
        return self.chosen_pawn
    
    def get_chosen_pawn_coord(self) -> tuple[int, int, int]:
        if not self.chosen_pawn:
            logger.error(f"query opened pawn coord before it is defined", "Game.get_chosen_pawn_coord()")
        #else:
        #    logger.info(f"query opened pawn: {self.chosen_pawn_coord}", "Game.get_chosen_pawn_coord()")
        return self.chosen_pawn_coord
    
    def is_chosen_pawn_default(self) -> bool:
        #if not self.chosen_pawn:
        #    logger.info("opened pawn is default", "Game.is_chosen_pawn_default()")
        return self.chosen_pawn.is_default
    
    def set_chosen_pawn(self, new_pawn: Pawn|dict):
        logger.info(f"open pawn {new_pawn}", f"Game.set_chosen_pawn({new_pawn})")
        if isinstance(new_pawn, dict):
            new_pawn = self.pawns_manager.get_pawn_by_id(new_pawn["id"]) #type: ignore
            logger.info(f"new pawn was dict. now is {new_pawn}", f"Game.set_chosen_pawn({new_pawn})")
            if new_pawn.is_default:
                logger.error("new pawn is default. Something is wrong", f"Game.set_chosen_pawn({new_pawn})")

        if isinstance(new_pawn, Pawn):
            logger.info(f"opened pawn changed from {self.chosen_pawn} to {new_pawn}", f"Game.set_chosen_pawn({new_pawn})")
            self.chosen_pawn = new_pawn
            self.chosen_pawn_coord = self.chosen_pawn.coord
            if self.chosen_pawn.is_default:
                logger.error("new pawn is default. Something is wrong", f"Game.set_open_pawn({new_pawn})")
        else:
            logger.error(f"attempt to assign an impossible value to opened pawn", f"Game.set_chosen_pawn({new_pawn})")
        self.update_chosen_pawn_coord()

    def update_chosen_pawn_coord(self):
        self.chosen_pawn_coord = self.chosen_pawn.coord

    def reset_chosen_pawn(self):
        logger.info("opened pawn reset", "Game.reset_chosen_pawn()")
        self.chosen_pawn = self._default_pawn
        self.chosen_pawn_coord = self.chosen_pawn.coord
    
    def get_chosen_building(self) -> Building:
        if not self.chosen_building:
            logger.error(f"query chosen building before it is defined", "GameManager.get_chosen_building()")
        return self.chosen_building

    def is_chosen_building_defult(self) -> bool:
        return self.chosen_building.is_default

    def set_chosen_building(self, building: Building|dict):
        if isinstance(building, dict):
            building = self.buildings_manager.get_building_by_coord(building["coord"])

        if not building:
            logger.error("new building is default. Something is wrong", f"GameManager.set_chosen_building({building})")
        logger.info(f"new chosen building is {building}", f"GameManager.set_chosen_building(...)")
        self.chosen_building = building
        self.update_chosen_building_coord()

    def reset_chosen_building(self):
        logger.info("chosen building is reset", "GameManager.reset_chosen_building()")
        self.chosen_building = self._default_building
        self.update_chosen_building_coord()
    
    def get_chosen_building_coord(self) -> tuple[int, int, int]:
        return self.chosen_building_coord
    
    def update_chosen_building_coord(self):
        self.chosen_building_coord = self.chosen_building.coord

    def is_chosen_building_coord_default(self):
        return self.chosen_building.is_default

    def get_target_coord(self):
        if self.is_target_coord_default():
            logger.error(f"query target coord before it is defined", "Game.get_target_coord()")
        return self.targets_coord
    
    def set_target_coord(self, new_target_coord: tuple[int, int, int]):
        logger.info(f"target coord changet from {self.targets_coord} to {new_target_coord}", f"GUIGame.set_target_coord({new_target_coord})")
        self.targets_coord = new_target_coord

    def reset_target_coord(self):
        logger.info(f"target coord reset", "GUIGame.set_target_coord_null()")
        self.targets_coord = (-1, -1, -1)
    
    def is_target_coord_default(self):
        if self.targets_coord == (-1, -1, -1):
        #    logger.info("target coord is default", "Game.is_target_coord_default()")
            return True
        return False
    
    def get_chosen_inputfield(self):
        if self.is_chosen_inputfield_default():
            logger.error("query chosen inputfield  before it is defined", "Game.get_chosen_inputfield()")
        return self.chosen_inputfield

    def is_chosen_inputfield_default(self):
        if self.chosen_inputfield == self._default_chosen_inputfield:
        #    logger.info("chosen inputfield is default", "Game.is_chosen_inputfield_default()")
            return True
        else:
            return False
    
    def chose_input_field(self, inputfield: InputField):
        self.chosen_inputfield = inputfield
    
    def reset_chosen_inputfield(self):
        self.chosen_inputfield = self._default_chosen_inputfield
    
    def add_inputfield(self, inputfield: InputField):
        self.input_fields.append(inputfield)