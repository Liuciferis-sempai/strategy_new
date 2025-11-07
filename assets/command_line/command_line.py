import pygame as py
from typing import Any
from assets import root
from assets.root import logger
from assets.pawns.pawn import Pawn
from assets.buildings.building import Building
from assets.world.cell import Cell
from assets.auxiliary_stuff.functions import update_gui
from assets.gui.inputfield import InputField
from assets.gui.textfield import TextField

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
            "food_cons": "food_valued_consumption_per_person_factor"
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
        self.inputfield = InputField(self.width, self.font_size, (0, self.height-self.font_size), "", self.font_size, self.line_color, self, True)

        self.lines: list[TextField] = []

    def add_answer(self, answer: str):
        #print(answer)
        self.lines.append(TextField(self.width, self.font_size, text=answer, font_size=self.font_size, color=self.color, translate=False))
        if len(self.lines) > 5:
            self.lines.pop(0)
        update_gui()

    def process_input(self, value: str):
        value = value.replace("\n", "")
        self.inputfield.value = ""

        input_list: list[str] = value.split(" ")
        inputs: list = []
        effect_name = ""
        effect_data = {}

        if input_list[0] == "set":
            self._process_set_variable(input_list[1], input_list[2:])
            return
        elif input_list[0] == "get":
            self._process_get_variable(input_list[1])
            return
        elif input_list[0] == "show":
            effect_name = "show_statistic"
            inputs.append(input_list[1:])
        
        self._process_regular_command(value, input_list, inputs, effect_name, effect_data)
    
    def _process_get_variable(self, value: str):
        value = self._translate_input_value(value)
        for object in [root, root.game_manager]:
            if hasattr(object, value):
                self.add_answer(f"{value} is {getattr(object, value)}")
        self.add_answer(f"can nor find a {value}")

    def _process_set_variable(self, attribute: str, new_value: Any):
        attribute = self._translate_input_value(attribute)
        for object in [root, root.game_manager]:
            if hasattr(object, attribute):
                if len(new_value) < 2:
                    new_value = new_value[0]
                    if isinstance(new_value, str):
                        if new_value.count(",") == 1:
                            tuple_ =  new_value.split(",")
                            new_value = (int(tuple_[0]), int(tuple_[1]))
                        elif new_value.count(",") > 1:
                            list_ = new_value.split(",")
                            new_value = [int(i) for i in list_]
                setattr(object, attribute, new_value)
                self.add_answer(f"{attribute} has new value {new_value}")
                return
        self.add_answer(f"can nor find a {attribute}")
    
    def _process_regular_command(self, value: str, input_list: list[str], inputs: list, effect_name: str, effect_data: dict):
        input = self._generator_for_input_value(value)
        if input_list[0] == "from" and input_list[2] == "to":
            start_pos = input_list[1].split(",")
            start_coord = (int(start_pos[0]), int(start_pos[1]))

            end_pos = input_list[3].split(",")
            end_coord = (int(end_pos[0]), int(end_pos[1]))

            coord = [start_coord[0], start_coord[1]]

            while coord[0] != end_coord[0] or coord[1] != end_coord[1]:
                inputs, input = self._generate_input_for_coord(coord, input_list[4:], inputs)
                if coord[1] != end_coord[1]:
                    if coord[1] > end_coord[1]:
                        coord[1] -= 1
                    else:
                        coord[1] += 1
                elif coord[0] != end_coord[0]:
                    coord[1] = start_coord[1]
                    if coord[0] > end_coord[0]:
                        coord[0] -= 1
                    else:
                        coord[0] += 1
            else:
                inputs, input = self._generate_input_for_coord(coord, input_list[4:], inputs)
        else:
            inputs.append(input)

        for input in inputs:
            for entry in input:
                word = root.game_manager.effect_manager.translate(entry)
                if word in root.game_manager.effect_manager.effects.keys():
                    effect_name = word
                else:
                    effect_data = self._process_entry(input, entry, effect_name, effect_data) #type: ignore
                    if effect_data == None: return logger.error(f"false processed entry {entry} by {input}", f"CommandLine.process_input({value})")
            self.add_answer(root.game_manager.effect_manager.do(effect_name, effect_data))
    
    def _translate_input_value(self, value: str) -> str:
        return self._translate.get(value, value)
    
    def _generate_input_for_coord(self, coord: list[int], input_list: list[str], inputs: list) -> tuple[list, Any]:
        tail = " ".join(input_list)+f" {coord[0]},{coord[1]}"
        input = self._generator_for_input_value(tail)
        inputs.append(input)
        #print(tail)

        return inputs, input

    def _process_entry(self, input, entry: str, effect_name: str, effect_data: dict) -> dict|None:
        if entry.count(",") == 1:
            if effect_name != "open_area":
                result = self._coord_process(effect_name, entry, effect_data)
                if result == None:
                    logger.error(f"coord {entry} does not exist", f"CommandLine._process_entry({input}, {entry}, {effect_name}, {effect_data})")
                    return None
                else: effect_data = result
            else:
                if effect_data.get("start_coord"):
                    pos =  entry.split(",")
                    effect_data["end_coord"] = (int(pos[0]), int(pos[1]))
                else:
                    pos =  entry.split(",")
                    effect_data["start_coord"] = (int(pos[0]), int(pos[1]))
        elif effect_name in ["spawn", "build"]:
            effect_data = self._object_process(entry, effect_data)
        elif effect_name == "clear_the_queue":
            effect_data["reciept"] = root.game_manager.reciept_manager.get_reciept_by_id(entry)
        elif effect_name == "change_cell":
            effect_data["new_type"] = entry
        elif effect_name == "add_resource":
            try:
                effect_data["amount"] = int(entry)
            except:
                effect_data["resource"] = entry
        else:
            effect_data[entry] = next(input)
        return effect_data
    
    def _object_process(self, entry: str|int, effect_data: dict) -> dict:
        if entry in ["pl", "player"]:
            entry = root.player_id
        try:
            entry = int(entry)
            effect_data["fraction_id"] = entry
        except:
            effect_data["type"] = entry

        return effect_data
    
    def _generator_for_input_value(self, value: str):
        inputs: list[str] = value.split(" ")
        for entry in inputs:
            yield entry

    def _coord_process(self, effect: str, entry: str, data: dict) -> dict|None:
        if not root.game_manager.effect_manager.effects.get(effect, {}).get("coord", False):
            target = self._get_target(entry)
            if isinstance(target, Pawn):
                data["target"] = target
            elif isinstance(target, Building):
                data["building"] = target
            elif isinstance(target, Cell):
                data["cell"] = target
            else:
                return None
        else:
            pos =  entry.split(",")
            data["coord"] = (int(pos[0]), int(pos[1]))
        return data
    
    def _get_target(self, coord: str) -> Pawn|Building|Cell|None:
        pos = coord.split(",")
        pos = (int(pos[0]), int(pos[1]))

        building = root.game_manager.buildings_manager.get_building_by_coord(pos)
        if not building.is_default:
            return building
        
        pawn = root.game_manager.pawns_manager.get_pawn_by_coord(pos)
        if not pawn.is_default:
            return pawn
        
        cell = root.game_manager.world_map.get_cell_by_coord(pos)
        if not cell.is_default:
            return cell
        
        logger.error("coord does not exist", f"CommandLine._get_target({coord})")
        return None

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
        #self.inputfield.draw()