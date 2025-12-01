import pygame as py
from typing import Any, TYPE_CHECKING
from .. import root
from ..root import logger
from ..world.cell import Cell
from ..auxiliary_stuff import *
from ..gui.inputfield import InputField
from ..gui.textfield import TextField

from ..managers.pawns.pawn import Pawn
from ..managers.buildings.building import Building

class CommandLine(py.sprite.Sprite):
    _translate = {
            "pl": "player_id",
            "player": "player_id",
            "ch_cell": "chosen_cell",
            "ch_cell_c": "chosen_cell_coord",
            "ch_pawn": "chosen_pawn",
            "ch_pawn_c": "chosen_pawn_coord",
            "op_pawn": "chosen_pawn",
            "op_pawn_c": "chosen_pawn_coord",
            "window": "window_size",
            "world": "world_map_size",
            "food_frame": "food_sufficiency_factor_frame",
            "food_center": "food_sufficiency_factor_center",
            "time": "time_for_show_info",
            "year": "year_length",
            "growth_rate": "base_growth_rate",
            "food_cons": "food_valued_consumption_per_person_factor",
            "child": "children",
            "res": "resource",
            "add_res": "add_resource",
            "re_res": "remove_resource",
            "pol": "policy"
        }

    def __init__(self, color:tuple[int, int, int, int]=(100, 100, 100, 255), font_size:int=30, line_color:tuple[int, int, int, int]=(150, 150, 150, 255)):
        super().__init__()
        self.line_amount = 7

        self.width = root.window_size[0]
        self.height = font_size*self.line_amount
        self.color = color
        self.position = (0, 0)
        self.font_size = font_size
        self.line_color = line_color
        self.is_active = False

        self.image = py.Surface((self.width, self.height))
        self.image.fill(color)
        self.rect = py.Rect(self.position[0], self.position[1], self.width, self.height)

        self.font = py.font.Font(None, 20)
        self.inputfield = InputField(self.width, self.font_size, (0, self.height-self.font_size), "", self.font_size, self.line_color, (0, 0, 0, 0), input_processor=self, hidden=True)

        self.lines: list[TextField] = []

    def add_answer(self, answer: str):
        #print(answer)
        self.lines.append(TextField(self.width, self.font_size, text=answer, font_size=self.font_size, bg_color=self.color, translate=False))
        if len(self.lines) > self.line_amount:
            self.lines.pop(0)
        update_gui()

    def process_input(self, command_line: str):
        command_line = command_line.replace("\n", "")
        self.inputfield.value = ""

        splited_command: list[str] = command_line.split(" ")
        commands = [splited_command]

        try:
            if splited_command[0] == "from" and splited_command[2] == "to":
                commands = []
                start_coord = self._process_coord({"coord": "coord"}, splited_command[1], {})["coord"]
                end_coord = self._process_coord({"coord": "coord"}, splited_command[3], {})["coord"]
                for x in range(start_coord[0], end_coord[0]+1):
                    for y in range(start_coord[1], end_coord[1]+1):
                        command = [splited_command[4], f"{x},{y}"] + splited_command[5:]
                        commands.append(command)
        except:
            pass
        
        for command in commands:
            command_type = command[0]
            try:
                if command_type == "set":
                    self._process_set_command(command[1:])
                elif command_type == "get":
                    self._process_get_command(command[1:])
                elif command_type == "add":
                    self._process_add_command(command[1:])
                elif command_type == "remove":
                    self._process_remove_command(command[1:])
                elif command_type == "build":
                    self._process_build_command(command[1:])
                elif command_type == "spawn":
                    self._process_spawn_command(command[1:])
                elif command_type == "open":
                    self._process_open_command(command[1:])
                elif command_type == "show":
                    self._process_show_command(command[1:])
                elif command_type == "create":
                    self._process_create_command(command[1:])
                elif command_type == "damage":
                    self._process_attack_command(command[1:])
                elif command_type == "help":
                    self._process_help_command(command[1:])
                else:
                    self._process_usual_command(command[0], command[1:])
            except IndexError as e:
                logger.error(f"can not process command {command_line} because the key is missing ({e})", f"CommandLine.process_input({command_line})")
                self.add_answer(f"ERROR: the key {e} is missing")
            except KeyError as e:
                logger.error(f"can not process command {command_line} because the key {e} is missing", f"CommandLine.process_input({command_line})")
                self.add_answer(f"ERROR: the key {e} is missing")
            except Exception as e:
                logger.error(f"can not process command {command_line} because '{e}'", f"CommandLine.process_input({command_line})")
                self.add_answer(f"ERROR: {repr(e)}")
    
    def _process_set_command(self, splited_command: list[str]):
        attribute = self._translate_value(splited_command[0])
        for storage in [root, root.game_manager]:
            if hasattr(storage, attribute):
                new_value = self._process_value(splited_command[1:])
                if len(new_value) == 1:
                    new_value = new_value[0]
                    if can_be_int(new_value):
                        new_value = int(new_value)
                elif len(new_value) == 0:
                    self.add_answer(f"new value has an impossible value: '{new_value}'")
                    return
                setattr(storage, attribute, new_value)
                self.add_answer(f"new {attribute} is '{new_value}'")
                return

    def _process_get_command(self, splited_command: list[str]):
        target_type = splited_command[0]
        target_coord = None
        if len(splited_command) > 1 and "," in splited_command[1]:
            target_coord = self._splite_coord(splited_command[1])

        target_name = None
        if len(splited_command) > 2 and "," in splited_command[1]:
            target_name = splited_command[2]

        if target_coord:
            if target_name:
                target = self._get_target_at_coord(target_coord, target_name=target_name, target_type=target_type)
            else:
                target = self._get_target_at_coord(target_coord, target_type=target_type)
            
            if target:
                if isinstance(target, list):
                    for line in target:
                        if line:
                            self.add_answer(f"{target_coord}: {line}")
                else:
                    self.add_answer(f"{target_type}: {target}")
                return
        elif self._process_get_target(target_type, splited_command): return
        else:
            attribute = self._translate_value(target_type)
            for storage in [root, root.game_manager]:
                if hasattr(storage, attribute):
                    value = getattr(storage, attribute)
                    self.add_answer(f"{attribute} has value '{value}'")
                    return
        self.add_answer(f"target {target_type} not found")

    def _process_get_target(self, target: str, splited_command: list[str]) -> bool:
        match target:
            case _:
                return False

    def _process_add_command(self, splited_command: list[str]):
        command_target = self._translate_value(splited_command[0])

        if command_target == "resource":
            effect_name = "add_resource"
        elif command_target == "pop":
            effect_name = "add_popgroup"
            self._process_popgroup_command(effect_name, splited_command[1:])
            return
        elif command_target == "policy":
            effect_name = "add_policy"
        else:
            raise Exception("second argument must be a name of added object")
        
        self._process_usual_command(effect_name, splited_command[1:])

    def _process_remove_command(self, splited_command: list[str]):
        command_target = self._translate_value(splited_command[0])

        if command_target == "resource":
            effect_name = "take_resource"
        elif command_target == "pop":
            effect_name = "remove_popgroup"
            self._process_popgroup_command(effect_name, splited_command[1:])
        elif command_target == "policy":
            effect_name = "remove_policy"
        elif command_target == "building":
            effect_name = "remove_building"
        elif command_target == "pawn":
            effect_name = "despawn"
        else:
            raise Exception("second argument must be a name of object to add")
        
        self._process_usual_command(effect_name, splited_command[1:])

    def _process_build_command(self, splited_command: list[str]):
        self._process_usual_command("build", splited_command)

    def _process_spawn_command(self, splited_command: list[str]):
        self._process_usual_command("spawn", splited_command)

    def _process_open_command(self, splited_command: list[str]):
        effect_data = {}
        if splited_command[0] == "area":
            start_coord = splited_command[1].split(",")
            if len(start_coord) == 2:
                effect_data["start_coord"] = (int(start_coord[0]), int(start_coord[1]), 0)
            else:
                effect_data["start_coord"] = (int(start_coord[0]), int(start_coord[1], int(start_coord[2])))

            end_coord = splited_command[2].split(",")
            if len(end_coord) == 2:
                effect_data["end_coord"] = (int(end_coord[0]), int(end_coord[1]), 0)
            else:
                effect_data["end_coord"] = (int(end_coord[0]), int(end_coord[1]), int(end_coord[2]))

            self.add_answer(root.game_manager.effect_manager.do("open_area", effect_data))

        elif splited_command[0] == "building":
            try: fraction_id = int(splited_command[1])
            except: fraction_id = root.player_id
            fraction = root.game_manager.fraction_manager.get_fraction_by_id(fraction_id)
            all_buildings = root.game_manager.buildings_manager.get_all_possible_buildings_types()
            opened_buildings_amount = 0
            for building_type in all_buildings:
                if building_type not in fraction.allowed_buildings:
                    fraction.allowed_buildings.append(building_type)
                    opened_buildings_amount += 1
            self.add_answer(f"opened {opened_buildings_amount} buildings")

        elif splited_command[0] == "pawn":
            try: fraction_id = int(splited_command[1])
            except: fraction_id = root.player_id
            fraction = root.game_manager.fraction_manager.get_fraction_by_id(fraction_id)
            all_pawns = root.game_manager.pawns_manager.get_all_pawns_types()
            opened_pawns_amount = 0
            for pawn_type in all_pawns:
                if pawn_type not in fraction.allowed_pawns:
                    fraction.allowed_pawns.append(pawn_type)
                    opened_pawns_amount += 1
            self.add_answer(f"opened {opened_pawns_amount}")

        elif splited_command[0] == "reciept":
            try: fraction_id = int(splited_command[1])
            except: fraction_id = root.player_id
            fraction = root.game_manager.fraction_manager.get_fraction_by_id(fraction_id)
            all_reciepts = root.game_manager.reciept_manager.get_all_reciepts_id()
            opened_reciepts_amount = 0
            for reciept in all_reciepts:
                if reciept not in fraction.reciepts:
                    fraction.reciepts.append(reciept)
                    opened_reciepts_amount += 1
            self.add_answer(f"opened {opened_reciepts_amount} reciept")

        else:
            raise Exception("second argument must be name of object to open")

    def _process_show_command(self, splited_command: list[str]):
        coord = self._process_coord({"coord": "coord"}, splited_command[0], {})["coord"]
        self.add_answer(root.game_manager.effect_manager.do("show_statistic", {"coord": coord}))

    def _process_create_command(self, splited_command: list[str]):
        target_of_creation = splited_command[0]
        if target_of_creation == "fraction":
            effect = "create_fraction"
        else:
            raise Exception("second argument must be name of object to create")
        effect_data = {}
        command = self._generate_command(splited_command[1:])

        for entry in command:
            if not effect_data.get("name"):
                effect_data["name"] = entry
            elif not effect_data.get("type"):
                effect_data["type"] = entry
            else:
                if "=" in entry:
                    key, value, *_ = entry.split("=")
                    effect_data[key] = value
                else:
                    effect_data[entry] = next(command)
        
        if not effect_data.get("type", False):
            effect_data["type"] = "bot"
        if not effect_data.get("name", False):
            effect_data["name"] = random_name()

        self.add_answer(root.game_manager.effect_manager.do(effect, effect_data))

    def _process_attack_command(self, splited_command: list[str]):
        coord_data = self._process_coord({"pawn": "pawn", "building": "building"}, splited_command[0], {})
        for _, val in coord_data.items():
            self.add_answer(root.game_manager.effect_manager.do("attack", {"target": val, "data": {"damage": int(splited_command[1]), "type": splited_command[2] if len(splited_command)>2 else "none"}}))

    def _process_popgroup_command(self, effect_name: str, splited_command: list[str]):
        town = root.game_manager.town_manager.get_town_by_coord(self._process_coord({"coord": "coord"}, splited_command[0], {})["coord"])
        effect_data = {"town": "Town", "size": {}, "popgroup_name": splited_command[1]}
        command = self._generate_command(splited_command[2:])

        for entry in command:
            effect_data["size"][self._translate_value(entry)] = int(next(command))
        
        self.add_answer(root.game_manager.effect_manager.do(effect_name, effect_data))
    
    def _process_help_command(self, splited_command: list[str]):
        if splited_command == []:
            items = root.game_manager.effect_manager.effects.keys()
            answer = f""
            for key in items:
                answer += f"{key}; "
            self.add_answer(answer)
        else:
            effect_name = self._translate_value(splited_command[0])
            if effect_name in root.game_manager.effect_manager.effects.keys():
                items = root.game_manager.effect_manager.effects[effect_name].items()
                answer = f"{effect_name}-> "
                for key, value in items:
                    answer += f"{key}: {value}; ".replace("|", " or ")
                self.add_answer(answer)
            elif effect_name == "target":
                self.add_answer(f"to specify a target, it is enough to indicate its coordinates")
            elif effect_name == "coord":
                self.add_answer(f"the correct entry for coordinates is: x,y or x,y,z (default z is 0)")
            else:
                self.add_answer(f"unknow command '{effect_name}'")

    def _process_usual_command(self, effect_name: str, splited_command: list[str]):
        command = self._generate_command(splited_command)
        effect = root.game_manager.effect_manager.effects[effect_name]
        keys = effect.keys()
        effect_data = {}

        for entry in command:
            entry = self._translate_value(entry)
            if "," in entry:
                effect_data = self._process_coord(effect, entry, effect_data)
            elif can_be_int(entry):
                if "fraction_id" in keys and not effect_data.get("fraction_id"):
                    effect_data["fraction_id"] = int(entry)
                elif "amount" in keys and not effect_data.get("amount"):
                    effect_data["amount"] = int(entry)
                elif "size" in keys and not effect_data.get("size"):
                    effect_data["size"] = int(entry)
            elif "fraction_id" in keys and entry == "player_id" and not effect_data.get("fraction_id"):
                effect_data["fraction_id"] = root.player_id
            elif "type" in keys and (entry in root.game_manager.buildings_manager.get_all_possible_buildings_types() or entry in root.game_manager.pawns_manager.get_all_pawns_types()):
                effect_data["type"] = entry
            elif effect_name in ["add_resource", "remove_resource"]and not effect_data.get("resource"):
                effect_data["resource"] = entry
            elif effect_name in ["add_policy", "remove_policy"] and not effect_data.get("policy"):
                effect_data["policy"] = entry
            else:
                if "=" in entry:
                    key, value, *_ = entry.split("=")
                    effect_data[key] = value
                else:
                    effect_data[entry] = next(command)

        self.add_answer(root.game_manager.effect_manager.do(effect_name, effect_data))

    def _splite_coord(self, entry: str) -> tuple[int, int, int]:
        if entry.count(",") == 1:
            target_coord = entry.split(",")
            return (int(target_coord[0]), int(target_coord[1]), 0)
        elif entry.count(",") == 2:
            target_coord = entry.split(",")
            return (int(target_coord[0]), int(target_coord[1]), int(target_coord[2]))
        else:
            raise Exception(f"incorrect coordinate entry ({entry}) exp: 1,7")

    def _process_coord(self, effect: dict[str, Any], entry: str, effect_data: dict) -> dict:
        target_coord = self._splite_coord(entry)

        keys = effect.keys()
        if "coord" in keys:
            effect_data["coord"] = target_coord
            return effect_data
        
        pawns = root.game_manager.pawns_manager.get_pawns_by_coord(target_coord)
        if "pawn" in keys and pawns != [] and pawns[0]:
            effect_data["pawn"] = pawns[0]
            return effect_data

        building = root.game_manager.buildings_manager.get_building_by_coord(target_coord)
        if "building" in keys and building:
            effect_data["building"] = building
            return effect_data
    
        cell = root.game_manager.world_map.get_cell_by_coord(target_coord)
        if "cell" in keys and cell:
            effect_data["cell"] = root.game_manager.world_map.get_cell_by_coord(target_coord)
            return effect_data

        return effect_data

    def _get_target_at_coord(self, coord: tuple[int, int, int], target_type: str = "any", target_name: str = "any") -> Cell|Pawn|Building|list|None:
        cell = root.game_manager.world_map.get_cell_by_coord(coord)
        
        if target_name == "any" and target_type == "any":
            return cell
        else:
            if target_type == "any":
                target = self._get_building_at_cell(cell, target_name)
                if target: return target
                target = self._get_pawn_at_cell(cell, target_name)
                if target: return target
            elif target_type == "pawn":
                target = self._get_pawn_at_cell(cell, target_name)
                return target
            elif target_type == "building":
                target = self._get_building_at_cell(cell, target_name)
            elif target_type == "all":
                return [cell, self._get_building_at_cell(cell, target_name), self._get_pawn_at_cell(cell, target_name)]

            return None
    
    def _get_building_at_cell(self, cell: Cell, building_name: str = "any") -> Building|None:
        if cell.buildings != {}:
            if cell.buildings["name"] == building_name or cell.buildings["type"] == building_name or building_name == "any":
                return root.game_manager.buildings_manager.get_building_by_coord(cell.coord)
        return None
    
    def _get_pawn_at_cell(self, cell: Cell, pawn_name: str = "any") -> Pawn|None|list[Pawn]:
        if cell.pawns != []:
            pawns: list[Pawn] = [root.game_manager.pawns_manager.get_pawn_by_id(pawn["id"]) for pawn in cell.pawns]
            if len(pawns) == 1 or pawn_name == "any":
                return pawns[0]
            elif len(pawns) == 0:
                return None
            elif pawn_name == "all":
                return pawns
            else:
                for pawn in pawns:
                    if pawn.name == pawn_name or pawn.type == pawn_name:
                        return pawn
        return None

    def _process_value(self, splited_command: list[str]) -> list[str]:
        for value in splited_command:
            if value.count(",") == 1:
               value = value.split(",")
               value = (int(value[0]), int(value[1]), 0)
            elif value.count(",") == 2:
                value = value.split(",")
                value = (int(value[0]), int(value[1]), int(value[2]))
            elif value.count(",") > 2:
                value = value.split(",")
                value = [int(v) for v in value]
        return splited_command

    def _translate_value(self, value: str):
        return self._translate.get(value, value)

    def _generate_command(self, splited_command: list[str]):
        for entry in splited_command:
            yield entry

    def activete(self):
        self.is_active = True
        self.inputfield.hidden = False
        self.inputfield.value = ""
        self.inputfield.click()

    def deactivete(self):
        self.is_active = False
        self.inputfield.hidden = True
        root.input_field_active = False

    def change_position_for_new_screen_sizes(self):
        self.width = root.window_size[0]
        self.height = self.font_size*self.line_amount

        self.image = py.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = py.Rect(self.position[0], self.position[1], self.width, self.height)

        self.inputfield.change_size(self.width, self.font_size)
        self.inputfield.rect.top = self.height - self.font_size

    def draw(self):
        root.screen.blit(self.image, self.rect)
        for i, line in enumerate(self.lines[::-1]):
            line.change_position((0, self.inputfield.rect.top-self.font_size*(i+1)))
            line.draw()
        self.inputfield.draw()