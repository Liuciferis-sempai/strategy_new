from .root import logger, loading
from .auxiliary_stuff import *
from . import root
from .gui.gui_manager import GUI
from .managers.pawns.pawnsmanager import PawnsManager
from .managers.pawns.pawn import Pawn
from .managers.reciept_manager import RecieptsManager
from .managers.turnmanager import TurnManager
from .world.worldmap import WorldMap
from .world.cell import Cell
from .gui.inputfield import InputField
from .managers.triggermanager import TriggerManager
from .managers.fraction.fraction_manager import FractionManager, Fraction
from .managers.technologies.technology_manager import TechnologyManager
from .managers.technologies.tech import Tech
from .managers.buildings.buildingsmanager import BuildingsManager
from .managers.buildings.building import Building
from .managers.policy.policytable import PolicyTable
from .managers.effectmanager import EffectManager
from .managers.jobmanager import JobManager
from .managers.resources.resourcemanager import ResourceManager
from .managers.eventmanager import EventManager
from .processing_input.proccessing_input import InputKeyProcessor
from .managers.towns_manager import TownManager
from .managers.storage_manager import StorageManager
from .managers.producer_manager import ProducerManager
from .managers.workbench_manager import WorkbenchManager
from .managers.scientific_manager import ScientificManager
from .managers.achievments_manager import AchievmentsManager
from .helpers.messenger import Messenger
from .helpers.command_line import CommandLine
from .helpers.listener import Listener

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .gui.buttons import Button

class GameManager:
    def __init__(self):
        '''
        Main Manager of game
        '''
        self.game_name = "Noname"

        self.x_offset = 0
        self.y_offset = 0

        self._default_cell = Cell(is_default=False)
        self._default_cell.is_default = True
        self._default_pawn = Pawn(is_default=False)
        self._default_pawn.is_default = True
        self._default_building = Building(is_default=False)
        self._default_building.is_default = True
        self._default_fraction = Fraction(is_default=False)
        self._default_fraction.is_default = True
        self._default_technology = Tech(is_default=False)
        self._default_technology.is_default = True
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
        self.buttons: dict[str, list["Button"]] = {}

        self.messenger = Messenger()
        self.world_map = WorldMap()

        self.command_line = CommandLine()
        self.add_inputfield(self.command_line.inputfield)

        logger.info("gamemanager ended primer initialization", "GameManager.__init__()")

    def initialize(self):
        self.fraction_manager = FractionManager(self)
        self.gui = GUI(self)
        self.pawns_manager = PawnsManager(self)
        self.reciept_manager = RecieptsManager(self)
        self.turn_manager = TurnManager(self)
        self.trigger_manager = TriggerManager(self)
        self.technology_manager = TechnologyManager(self)
        self.buildings_manager = BuildingsManager(self)
        self.policy_table = PolicyTable(self)
        self.effect_manager = EffectManager(self)
        self.job_manager = JobManager(self)
        self.resource_manager = ResourceManager(self)
        self.input_processor = InputKeyProcessor(self)
        self.town_manager = TownManager(self)
        self.storage_manager = StorageManager(self)
        self.producer_manager = ProducerManager(self)
        self.workbench_manager = WorkbenchManager(self)
        self.scientific_manager = ScientificManager(self)
        self.event_manager = EventManager(self)
        self.listener = Listener(self)
        self.achievments_manager = AchievmentsManager(self, root.config["achievments"])

        logger.info("gamemanager ended seconder initialization", "GameManager.initialize()")

    def draw(self):
        self.gui.draw()
        if self.command_line.is_active: self.command_line.draw()
        self.messenger.draw()
        self.event_manager.draw()
        self.achievments_manager.draw()
    
    def update_positions(self):
        self.gui.change_position_for_new_screen_sizes()
        self.command_line.change_position_for_new_screen_sizes()

    def get_cell_under_mouse(self) -> Cell:
        return self.input_processor.game_input.cell_under_mouse

    def get_x_offset(self) -> int:
        return self.x_offset
    
    def set_x_offset(self, value: int):
        self.x_offset = value
    
    def add_x_offset(self, value: int):
        self.x_offset += value

    def get_y_offset(self) -> int:
        return self.y_offset
    
    def set_y_offset(self, value: int):
        self.y_offset = value
    
    def add_y_offset(self, value: int):
        self.y_offset += value

    def get_default_cell(self) -> Cell:
        return self._default_cell
    
    def get_default_pawn(self) -> Pawn:
        return self._default_pawn
    
    def get_default_building(self) -> Building:
        return self._default_building
    
    def get_default_fraction(self) -> Fraction:
        return self._default_fraction
    
    def get_default_technology(self) -> Tech:
        return self._default_technology

    def get_cell(self, coord: None|tuple[int, int, int]|str = None, mouse_click_pos: None|tuple[int, int] = None, **_) -> Cell:
        if coord:
            if isinstance(coord, str): coord = parsing_coord(coord)
            return self.world_map.get_cell_by_coord(coord=coord)
        elif mouse_click_pos:
            return self.world_map.get_cell_by_click_pos(mouse_pos=mouse_click_pos)
        
        logger.error("can not find cell with information about it", f"GameManager.get_cell(coord={coord}, mouse_click_pos={mouse_click_pos})")
        return self._default_cell
    
    def get_pawn(self, coord: tuple[int, int, int]|str|None = None, pawn_type: str|None = None, pawn_name: str|None = None, pawn_category: str|None = None, pawn_id: int|None = None, **_) -> Pawn:
        if coord:
            if isinstance(coord, str): coord = parsing_coord(coord)
            if pawn_type:
                return self.pawns_manager.get_pawn_by_type(pawn_type, coord)
            elif pawn_category:
                return self.pawns_manager.get_pawn_by_category(pawn_category, coord)
            elif pawn_name:
                return self.pawns_manager.get_pawn_by_name(pawn_name, coord)
        elif pawn_id != None:
            return self.pawns_manager.get_pawn_by_id(pawn_id)

        logger.error("can not find cell with information about it", f"GameManager.get_pawn(coord={coord}, pawn_type={pawn_type}, pawn_name={pawn_name}, pawn_category={pawn_category}, pawn_id={pawn_id})")
        return self._default_pawn
    
    def get_pawns(self, coord: tuple[int, int, int]|str|None = None, pawn_type: str|None = None, pawn_category: str|None = None, **_) -> list[Pawn]:
        if coord:
            if isinstance(coord, str): coord = parsing_coord(coord)
            return self.pawns_manager.get_pawns_by_coord(coord)
        elif pawn_type:
            return self.pawns_manager.get_pawns_by_type(pawn_type)
        elif pawn_category:
            return self.pawns_manager.get_pawns_by_category(pawn_category)

        logger.error("can not find cell with information about it", f"GameManager.get_pawn(coord={coord}, pawn_type={pawn_type}, pawn_category={pawn_category})")
        return []
    
    def get_building(self, coord: tuple[int, int, int]|str|None = None, **_) -> Building:
        if coord:
            if isinstance(coord, str): coord = parsing_coord(coord)
            return self.buildings_manager.get_building_by_coord(coord)

        logger.error("can not find building with information about it", f"GameManager.ger_building(coord={coord})")
        return self._default_building

    def execute_effect(self, effect: dict[str, Any]|list[dict[str, Any]], is_parsed: bool = True, **kwargs) -> str:
        '''
        execute effect from effect_manager
        effect need key "effect_type" (name of effect)
        
        :param effect: single effect (dict) or multiple effects list[single effect]
        :type effect: dict|list
        :param is_parsed: was a parsing operation performed beforehand
        :type is_parsed: bool
        :param kwargs: passes keys to parsing_json_data if necessary
        :return: returns a short message about the effect(s) performed (not translated)
        :rtype: str
        '''
        if isinstance(effect, list):
            executed_effects = 0
            for subeffect in effect:
                if subeffect["effect_type"] not in self.effect_manager.effects_names:
                    logger.error(f"unknow effect name {subeffect["effect_type"]}", f"GameManager.execute_effect({effect})")
                    continue
                if not is_parsed: self.parsing_json_data(subeffect, **kwargs)
                self.effect_manager.do(effect_type=subeffect["effect_type"], effect_data=subeffect)
            return f"executed {executed_effects} effects out of {len(effect)}"
        elif isinstance(effect, dict):
            if effect["effect_type"] not in self.effect_manager.effects_names:
                logger.error(f"unknow effect name {effect["effect_type"]}", f"GameManager.execute_effect({effect})")
                return "unknow effect name"
            if not is_parsed: self.parsing_json_data(effect, **kwargs)
            return self.effect_manager.do(effect_type=effect["effect_type"], effect_data=effect)
        return f"unknow effect type {type(effect)}"
    
    def trigger(self, trigger: dict[str, Any]|list[dict[str, Any]], is_parsed: bool = True, **kwargs) -> bool:
        '''
        checks the trigger
        trigger need key "type" (name of trigger)

        :param trigger: single trigger (dict) or multiple triggers list[single trigger]
        :type trigger: dict|list
        :param is_parsed: was a parsing operation performed beforehand
        :type is_parsed: bool
        :param kwargs: passes keys to parsing_json_data if necessary
        :return:
        :rtype: bool
        '''
        try:
            if isinstance(trigger, list):
                for subtrigger in trigger:
                    if not is_parsed: self.parsing_json_data(subtrigger, **kwargs)
                    if not self.trigger_manager.check(subtrigger):
                        return False
                return True
            elif isinstance(trigger, dict):
                if not is_parsed: self.parsing_json_data(trigger, **kwargs)
                return self.trigger_manager.check(trigger)
        except Exception as e:
            logger.error(f"trigger error {repr(e)} by trigger '{trigger}'", f"GameManager(..., kwargs={kwargs})")
            return False
    
    def addListener(self, trigger: dict|list, effect: dict|list) -> tuple:
        return self.listener.add(trigger, effect)
    
    def removeListener(self, listener: tuple) -> bool:
        return self.listener.remove(listener)

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
            new_pawn = self.get_pawn(pawn_id=new_pawn["id"]) #type: ignore
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

    def is_chosen_building_default(self) -> bool:
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
    
    def get_chosen_coord(self) -> tuple[int, int, int]:
        if not self.is_chosen_building_default():
            return self.get_chosen_building_coord()
        elif not self.is_chosen_cell_default():
            return self.get_chosen_cell_coord()
        elif not self.is_chosen_pawn_default():
            return self.get_chosen_pawn_coord()

        logger.error("chosen coord is default", "GameManager.get_chosen_coord()")
        return (-1, -1, 0)

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

    def add_button(self, button: "Button", button_game_state: str):
        if not self.buttons.get(button_game_state):
            self.buttons[button_game_state] = []
        self.buttons[button_game_state].append(button)
    
    def remove_button(self, button_to_remove: "Button"):
        for state in self.buttons:
            for button in self.buttons[state]:
                if button == button_to_remove:
                    self.buttons[state].remove(button)
                    return
    
    def parsing_json_data(self, json_data: dict[str, Any], target_name: str|None = None, calling_fraction_id: int|None = None, **_):
        '''
        prepares a JSON template for processing by code (replaces placeholders in the specified manner)
        do not return anything, but modifies json_data
        @ - spec symbol for deep search
        * - spec symbol for skip this key-value

        :param json_data: data that need prepare
        :type json_data: dict
        :param target_name: necessary if the data provides for the existence of a target (not chosen!)
        :type target_name: str | None = None is default
        :param calling_fraction_id: specifies the faction ID of the caller (optional)
        :type calling_fraction_id: int | None = None is default
        '''
        target_coord = self.get_target_coord()

        if not target_name:
            target_name = "unknow"
            target_building = self._default_building
            target_cell = self._default_cell
            target_pawn = self._default_pawn
        else:
            target_building = self.buildings_manager.get_building_by_coord(target_coord)
            target_pawn = self.get_pawn(pawn_type=target_name, coord=target_coord)
            target_cell = self.get_cell(coord=target_coord)

        to_remove = []
        to_add = []

        for key in json_data:
            if not isinstance(json_data[key], str): continue
            #fraction process
            if "fraction_id" in key:
                if "player" in json_data[key]:
                    json_data[key] = root.player_id
                elif calling_fraction_id:
                    json_data[key] = calling_fraction_id
                elif can_be_int(json_data[key]) and int(json_data[key]) > 0:
                    json_data[key] = int(json_data[key])
            
            elif "coord" in key and "," in json_data[key]:
                json_data[key] = parsing_coord(json_data[key])

            #@ - spec symbol for deep search
            elif "@" in json_data[key]:
                deep_search(json_data, key, target_building, target_pawn, target_cell)

            #process chosen
            elif "chosen" in json_data[key]:
                if is_in("pawn", json_data[key]) and not self.is_chosen_pawn_default():
                    json_data[key] = self.get_chosen_pawn()
                elif is_in("building", json_data[key]) and not self.is_chosen_building_default():
                    json_data[key] = self.get_chosen_building()
                elif is_in("cell", json_data[key]) and not self.is_chosen_cell_default():
                    json_data[key] = self.get_chosen_cell()

            #process target
            elif "target" in json_data[key]:
                if is_in("building", json_data[key]) and not target_building.is_default:
                    json_data[key] = target_building
                elif is_in("pawn", json_data[key]) and not target_pawn.is_default:
                    json_data["target"] = target_pawn
                elif is_in("cell", json_data[key]) and not target_cell.is_default:
                    json_data[key] = target_cell

            elif "on_chosen_coord" in json_data[key]:
                if is_in("building", json_data[key]):
                    json_data[key] = self.get_building(coord=self.get_chosen_coord())
                elif is_in("cell", json_data[key]):
                    json_data[key] = self.get_cell(coord=self.get_chosen_coord())

        for key in to_remove:
            json_data.pop(key)
        
        for key, value in to_add:
            json_data[key] = value