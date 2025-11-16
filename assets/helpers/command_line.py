import pygame as py
from typing import Any, TYPE_CHECKING
from .. import root
from ..root import logger
from ..world.cell import Cell
from ..auxiliary_stuff import update_gui, can_be_int
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
            "op_pawn": "opened_pawn",
            "op_pawn_c": "opened_pawn_coord",
            "window": "window_size",
            "world": "world_map_size",
            "food_frame": "food_sufficiency_factor_frame",
            "food_center": "food_sufficiency_factor_center",
            "time": "time_for_show_info",
            "year": "year_length",
            "growth_rate": "base_growth_rate",
            "food_cons": "food_valued_consumption_per_person_factor",
            "child": "children"
        }

    def __init__(self, color:tuple[int, int, int, int]=(100, 100, 100, 255), font_size:int=30, line_color:tuple[int, int, int, int]=(150, 150, 150, 255)):
        super().__init__()
        self.width = root.window_size[0]
        self.height = font_size*5
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
        if len(self.lines) > 5:
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
                else:
                    self._process_usual_command(command[0], command[1:])
            except Exception as e:
                logger.error(f"can not process command {command_line} because {e}", f"CommandLine.process_input({command_line})")
                self.add_answer(f"ERROR: {e}")
    
    def _process_set_command(self, splited_command: list[str]):
        attribute = self._translate_value(splited_command[0])
        for storage in [root, root.game_manager]:
            if hasattr(storage, attribute):
                new_value = self._process_value(splited_command[1:])
                if len(new_value) == 1:
                    new_value = new_value[0]
                elif len(new_value) == 0:
                    self.add_answer(f"new value has an impossible value: '{new_value}'")
                    return
                setattr(storage, attribute, new_value)
                self.add_answer(f"{attribute} new value is '{new_value}'")
                return

    def _finde_attribute(self, splited_command: list[str]) -> tuple[str, Pawn|Building|Cell|None]:
        attribute = self._translate_value(splited_command[0])
        if splited_command[0].count(",") == 1:
            coord_data = self._process_coord({"cell": "cell", "pawn": "pawn", "building": "building"}, splited_command[0], {})
            for key, val in coord_data.items():
                return (f"{key}: {val}", val)
        for storage in [root, root.game_manager]:
            if hasattr(storage, attribute):
                value = getattr(storage, attribute)
                return (f"{attribute} has value '{value}'", None)
        return (f"no attribute {splited_command[0]}", None)
    
    def _get_attribute(self, storage, data: str) -> str:
        if "." in data:
            data_list = data.split(".")
            if hasattr(storage, data_list[0]):
                att = getattr(storage, data_list[0])
                att = self._get_attribute(att, ".".join(data_list[1:]))
                return f"{storage}.{data} is {att}"
            return f"{storage} has no {data_list[0]}"
        else:
            if hasattr(storage, data):
                value = getattr(storage, data)
                return str(value)
            return f"{storage} has no {data}"
    
    def _process_get_command(self, splited_command: list[str]):
        attribute = self._finde_attribute(splited_command)

        if isinstance(attribute[1], Pawn|Building|Cell):
            if len(splited_command) > 1:
                answer = self._get_attribute(attribute[1], splited_command[1])
                self.add_answer(answer)
                return
        self.add_answer(attribute[0])

    def _process_add_command(self, splited_command: list[str]):
        command_target = splited_command[0]

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
        command_target = splited_command[0]

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
                effect_data[entry] = next(command)

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
                elif "amout" in keys and not effect_data.get("amout"):
                    effect_data["amout"] = int(entry)
                elif "size" in keys and not effect_data.get("size"):
                    effect_data["size"] = int(entry)
            elif "fraction_id" in keys and entry == "player_id" and not effect_data.get("fraction_id"):
                effect_data["fraction_id"] = root.player_id
            elif "type" in keys and (entry in root.game_manager.buildings_manager.get_all_possible_buildings_names() or entry in root.game_manager.pawns_manager.get_all_pawns_types()):
                effect_data["type"] = entry
            elif "add_resource" == effect_name and not effect_data.get("resource"):
                effect_data["resource"] = entry
            else:
                effect_data[entry] = next(command)

        self.add_answer(root.game_manager.effect_manager.do(effect_name, effect_data))

    def _process_coord(self, effect: dict[str, Any], entry: str, effect_data: dict) -> dict:
        if entry.count(",") == 1:
            target_coord = entry.split(",")
            target_coord = (int(target_coord[0]), int(target_coord[1]), 0)
        elif entry.count(",") == 2:
            target_coord = entry.split(",")
            target_coord = (int(target_coord[0]), int(target_coord[1]), int(target_coord[2]))
        else:
            raise Exception(f"incorrect coordinate entry ({entry}) exp: 1,7")

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
        self.height = self.font_size*5

        self.image = py.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = py.Rect(self.position[0], self.position[1], self.width, self.height)

        self.inputfield.change_size(self.width, self.height)
        self.inputfield.rect.top = self.height - self.font_size

    def draw(self):
        root.screen.blit(self.image, self.rect)
        for i, line in enumerate(self.lines[::-1]):
            line.change_position((0, self.inputfield.rect.top-self.font_size*(i+1)))
            line.draw()
        self.inputfield.draw()