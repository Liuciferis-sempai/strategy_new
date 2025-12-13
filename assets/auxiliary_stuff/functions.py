import pygame as py
from .. import root
import copy
from typing import Any, TypeGuard
import time
from random import randint, choice
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..managers.buildings.building import Building
    from ..managers.pawns.pawn import Pawn
    from ..world.cell import Cell

def normalize_cell_coord(x: int|None = None, y: int|None = None, z: int|None = None, coord: tuple[int, int, int]|None = None) -> tuple[int, int, int]:
        width, height = root.world_map_size
        width -= 1
        height -= 1
        if coord:
            x = coord[0]
            y = coord[1]
            z = coord[2]
        
        if x:
            if x <= 0: x = width + x
            elif x > width: x -= width
        if y:
            if y <= 0: y = height + y
            elif y > height: y -= height
        if z:
            if z not in root.game_manager.world_map.terrain.keys(): z = 0

        return (x if x else 0, y if y else 0, z if z else 0)

def append(obj: dict, key: str, value: Any):
    '''
    add 'value' in list in 'obj' under key 'key'

    :param obj: dict[str, list]
    :param key: str key for obj
    :param value: value for list in obj under key
    '''
    if has(obj, key):
        obj[key].append(value)
    else:
        obj[key] = [value]

def has(obj: object, name: str|int) -> bool:
    '''
    checks if an object has attribute 'name' (value of attribute is not important)

    :param obj: some object that can have attribute or value in himself
    :param name: name of attribute or index (for list)
    :return: True if 'obj' has atribute 'name'
    '''
    if isinstance(obj, dict):
        if name in obj.keys():
            return True
        return False
    elif isinstance(obj, list):
        if isinstance(name, int):
            try:
                obj[name]
                return True
            except: return False
        for item in obj:
            if item == name:
                return True
        return False
    elif isinstance(obj, str):
        if str(name) in obj:
            return True
        return False
    return hasattr(obj, str(name))

def deep_search(json_data: dict[str, str], key: str, target_building: "Building", target_pawn: "Pawn", target_cell: "Cell"):
        request = json_data[key].split(" ")[1:]
        if has(request, 3): default_value = request[3]
        else: default_value = None
        try:
            if not has(request, 2): raise Exception("missing way")
            if "target" in request[0]:
                if "building" in request[1] and not target_building.is_default: obj = target_building
                elif "pawn" in request[1] and not target_pawn.is_default: obj = target_pawn
                elif "cell" in request[1] and not target_cell.is_default: obj = target_cell
                else: raise Exception("missing target type")
            elif "chosen" in request[0]:
                if "building" in request[1]: obj = root.game_manager.get_chosen_building()
                elif "pawn" in request[1]: obj = root.game_manager.get_chosen_pawn()
                elif "cell" in request[1]: obj = root.game_manager.get_chosen_cell()
                else: raise Exception("missing chosen type")
            elif "on_chosen_coord" in request[0]:
                if "building" in request[1]: obj = root.game_manager.get_building(coord=root.game_manager.get_chosen_coord())
                elif "cell" in request[1]: obj = root.game_manager.get_cell(coord=root.game_manager.get_chosen_coord())
                else: raise Exception("missing (or is false) chosen type")
            else: raise Exception("missing search type")
            if obj.is_default: raise Exception("target/chosen is default")
            json_data[key] = deep_get(obj, request[2], default_value)
        except Exception as e:
            root.logger.error(f"fatal error '{repr(e)}' by deep parsing of '{json_data}'", "GameManager.parsing_json_data(...)")
            json_data[key] = "none"

def double_get(obj: dict[Any, Any], key: Any, second_key: Any, default_value: Any = None) -> Any:
    '''
    return value under 'key' in 'obj', if 'key' does not exist, then return value under 'second_key', if 'second_key' does not exist in 'obj' too, then return 'default_value'
    '''
    return obj.get(key, obj.get(second_key, default_value))

def get(obj: object, name: str|int, default_value: Any = None) -> Any:
    '''
    return value of 'obj' under name 'name' or default value 

    :param obj: some object that can have attribute or value in himself
    :param name: name of attribute or index (for list)
    :param default_value: default value, that will return if 'obj' has not attribute 'name'
    :return: return value of 'obj' under name 'name' or default value
    '''
    if isinstance(obj, dict):
        return obj.get(name, default_value)
    elif isinstance(obj, list):
        try:    return obj[int(name)]
        except: return default_value
    else:
        return getattr(obj, str(name), default_value)

def is_empty(obj: object) -> bool:
    '''
    checks if an object is empty
    None is empty

    :param obj: some object that can have attribute or value in himself
    '''
    if isinstance(obj, str):
        return obj.strip() == ""
    elif isinstance(obj, list):
        return len(obj) == 0
    elif isinstance(obj, dict):
        return len(obj) == 0
    elif obj == None:
        return True
    return False

def is_in(value: str, roster: list|list) -> bool:
    return value in roster or "any" in roster or "any" in value

def equal(value1: Any, value2: Any) -> bool:
    '''
    checks if value1 and value2 are equal
    if one of two value is "any" or have "any" in himself (list), then it will automatically return True
    '''
    if isinstance(value1, str):
        value1 = value1.strip()
        if value1 == "any":
            return True
    elif isinstance(value1, list):
        if "any" in value1:
            return True

    if isinstance(value2, str):
        value2 = value2.strip()
        if value2 == "any":
            return True
    elif isinstance(value2, list):
        if "any" in value2:
            return True

    if value1 == value2:
        return True

    return False

def parsing_coord(coord_for_parsing: str) -> tuple[int, int, int]:
    '''
    transforms a string into coordinates (the separator is ",")
    '''
    coord = coord_for_parsing.split(",")
    try:
        if len(coord) == 2:
            return (int(coord[0]), int(coord[1]), 0)
        elif len(coord) == 3:
            return (int(coord[0]), int(coord[1]), int(coord[2]))
    except: pass

    root.logger.error("parsing coord error", f"parsing_coord({coord_for_parsing})")
    return (0, 0, 0)

def deep_get(obj: object, way: str, default_value: Any|None = None) -> Any:
    '''
    get the value of the child object

    :type obj: object
    :param way: path to a value using a dot -> object_attribute.attribute_of_object_attribute.searched_object
    :type way: str
    :param default_value: any value that will be returned if the object was not found
    :type default_value: Any | None
    :return:
    :rtype: Any
    '''
    way_to_module = way.split(".")

    for i, mod in enumerate(way_to_module):
        obj = get(obj, mod, default_value)
        if i == len(way_to_module)-1: return obj
        if obj == default_value: return default_value

    return default_value

def get_cell_size() -> tuple[int, int]:
    return root.cell_sizes[root.cell_size_scale]

def get_cell_side_size() -> int:
    return root.cell_sizes[root.cell_size_scale][0]

def random_name(key_word: str = "none", lenght: tuple[int, int] = (5, 7)) -> str: # @TODO rewrite generation
    word_lenght = randint(lenght[0], lenght[1])
    word = ""
    for _ in range(word_lenght):
        word += choice(["q", "w", "e", "r", "t", "z", "u", "i", "o", "p", "a", "s", "d", "f", "g", "h", "j", "k", "l", "y", "x", "c", "v", "b", "n", "m"])

    return word.capitalize()

def extract_building_data_for_cell(building_data: dict[str, Any]) -> dict[str, str|int]:
    data = {
        "name": building_data["name"],
        "type": building_data["type"],
        "desc": building_data["desc"],
        "coord": building_data["coord"],
        "img": building_data["img"],
        "fraction_id": building_data["fraction_id"],
        "type": building_data["type"],
        "level": building_data["level"],
        "is_scheme": building_data.get("is_scheme", False)
    }
    return data

def update_gui():
    '''
    update all gui element in next tick
    '''
    root.need_update_gui = True

def can_be_int(value: Any) -> TypeGuard[int|str|bytes|bytearray]:
    try:
        int(value)
        return True
    except:
        return False

def to_int(value: Any, default_value: int = 0) -> int:
    try:
        return int(value)
    except:
        return default_value
    
def wrap_text(text: str, max_width: int, font: py.font.Font|None = None) -> list[str]:
    if font is None: font = py.font.Font(None, 20)

    wrapped_lines = []
    for line in text.splitlines():
        words = line.split(" ")
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                wrapped_lines.append(current_line.strip())
                current_line = word + " "
        if current_line:
            wrapped_lines.append(current_line.strip())
    return wrapped_lines

def hex_to_rgb(hex) -> tuple[int, int, int]:
  rgb = []
  for i in (0, 2, 4):
    decimal = int(hex[i:i+2], 16)
    rgb.append(decimal)
  
  return tuple(rgb)

def is_color_cold(color_hex: str) -> bool:
    rgb = hex_to_rgb(color_hex.lstrip('#'))
    if rgb[0] + rgb[1] < rgb[2]:
        return True
    return False

def is_color_warm(color_hex: str) -> bool:
    rgb = hex_to_rgb(color_hex.lstrip('#'))
    if rgb[0] + rgb[1] > rgb[2]:
        return True
    return False

def cold_degree(color_hex: str) -> float:
    '''
    return how cold is color (from 0 to 1)
    '''
    rgb = hex_to_rgb(color_hex.lstrip('#'))
    return max(0, (rgb[2] - (rgb[0] + rgb[1])/2) / 255)

def change_window_state(new_state:str):
    match new_state:
        case "game":
            root.game_manager.gui.draw = root.game_manager.gui.game.draw
            root.game_manager.input_processor.process_keydown = root.game_manager.input_processor.game_input.process_keydown
            root.game_manager.input_processor.process_mousebuttondown = root.game_manager.input_processor.game_input.process_mousebuttondown
            root.game_manager.input_processor.process_mousemotion = root.game_manager.input_processor.game_input.process_mousemotion
            root.game_manager.gui.show_info_under_mouse = root.game_manager.gui.game.show_info_about_cell_under_mouse
            root.game_manager.gui.move_up = root.game_manager.gui.game.move_up
            root.game_manager.gui.move_down = root.game_manager.gui.game.move_down
            root.game_manager.gui.move_left = root.game_manager.gui.game.move_left
            root.game_manager.gui.move_right = root.game_manager.gui.game.move_right
        case "fraction":
            root.game_manager.gui.draw = root.game_manager.gui.fraction.draw
            root.game_manager.input_processor.process_keydown = root.game_manager.input_processor.fraction_input.process_keydown
            root.game_manager.input_processor.process_mousebuttondown = root.game_manager.input_processor.fraction_input.process_mousebuttondown
            root.game_manager.input_processor.process_mousemotion = root.game_manager.input_processor.pass_func #not yet
            root.game_manager.gui.show_info_under_mouse = root.game_manager.gui.pass_func #not yet
            root.game_manager.gui.move_up = root.game_manager.gui.fraction.move_up
            root.game_manager.gui.move_down = root.game_manager.gui.fraction.move_down
            root.game_manager.gui.move_left = root.game_manager.gui.fraction.move_left
            root.game_manager.gui.move_right = root.game_manager.gui.fraction.move_right
        case "writing":
            root.game_manager.gui.draw = root.game_manager.gui.writing.draw
            root.game_manager.input_processor.process_keydown = root.game_manager.input_processor.writing_input.process_keydown
            root.game_manager.input_processor.process_mousebuttondown = root.game_manager.input_processor.writing_input.process_mousebuttondown
            root.game_manager.input_processor.process_mousemotion = root.game_manager.input_processor.pass_func #not yet
            root.game_manager.gui.show_info_under_mouse = root.game_manager.gui.pass_func #not yet
            root.game_manager.gui.move_up = root.game_manager.gui.writing.move_up
            root.game_manager.gui.move_down = root.game_manager.gui.writing.move_down
            root.game_manager.gui.move_left = root.game_manager.gui.writing.move_left
            root.game_manager.gui.move_right = root.game_manager.gui.writing.move_right
        case "technology":
            root.game_manager.gui.draw = root.game_manager.gui.technology.draw
            root.game_manager.input_processor.process_keydown = root.game_manager.input_processor.technology_input.process_keydown
            root.game_manager.input_processor.process_mousebuttondown = root.game_manager.input_processor.technology_input.process_mousebuttondown
            root.game_manager.input_processor.process_mousemotion = root.game_manager.input_processor.pass_func #not yet
            root.game_manager.gui.show_info_under_mouse = root.game_manager.gui.pass_func #not yet
            root.game_manager.gui.move_up = root.game_manager.gui.technology.move_up
            root.game_manager.gui.move_down = root.game_manager.gui.technology.move_down
            root.game_manager.gui.move_left = root.game_manager.gui.technology.move_left
            root.game_manager.gui.move_right = root.game_manager.gui.technology.move_right
        case "policy":
            root.game_manager.gui.draw = root.game_manager.gui.policy.draw
            root.game_manager.input_processor.process_keydown = root.game_manager.input_processor.policy_input.process_keydown
            root.game_manager.input_processor.process_mousebuttondown = root.game_manager.input_processor.policy_input.process_mousebuttondown
            root.game_manager.input_processor.process_mousemotion = root.game_manager.input_processor.pass_func #not yet
            root.game_manager.gui.show_info_under_mouse = root.game_manager.gui.pass_func #not yet
            root.game_manager.gui.move_up = root.game_manager.gui.policy.move_up
            root.game_manager.gui.move_down = root.game_manager.gui.policy.move_down
            root.game_manager.gui.move_left = root.game_manager.gui.policy.move_left
            root.game_manager.gui.move_right = root.game_manager.gui.policy.move_right
        case "building":
            root.game_manager.gui.draw = root.game_manager.gui.building.draw
            root.game_manager.input_processor.process_keydown = root.game_manager.input_processor.building_input.process_keydown
            root.game_manager.input_processor.process_mousebuttondown = root.game_manager.input_processor.building_input.process_mousebuttondown
            root.game_manager.input_processor.process_mousemotion = root.game_manager.input_processor.pass_func #not yet
            root.game_manager.gui.show_info_under_mouse = root.game_manager.gui.pass_func #not yet
            root.game_manager.gui.move_up = root.game_manager.gui.building.move_up
            root.game_manager.gui.move_down = root.game_manager.gui.building.move_down
            root.game_manager.gui.move_left = root.game_manager.gui.building.move_left
            root.game_manager.gui.move_right = root.game_manager.gui.building.move_right
        case "reciept":
            root.game_manager.gui.draw = root.game_manager.gui.reciept.draw
            root.game_manager.input_processor.process_keydown = root.game_manager.input_processor.reciept_input.process_keydown
            root.game_manager.input_processor.process_mousebuttondown = root.game_manager.input_processor.reciept_input.process_mousebuttondown
            root.game_manager.input_processor.process_mousemotion = root.game_manager.input_processor.pass_func #not yet
            root.game_manager.gui.show_info_under_mouse = root.game_manager.gui.pass_func #not yet
            root.game_manager.gui.move_up = root.game_manager.gui.reciept.move_up
            root.game_manager.gui.move_down = root.game_manager.gui.reciept.move_down
            root.game_manager.gui.move_left = root.game_manager.gui.reciept.move_left
            root.game_manager.gui.move_right = root.game_manager.gui.reciept.move_right
        case "share_menu":
            root.game_manager.gui.draw = root.game_manager.gui.sharemenu.draw
            root.game_manager.input_processor.process_keydown = root.game_manager.input_processor.share_menu_input.process_keydown
            root.game_manager.input_processor.process_mousebuttondown = root.game_manager.input_processor.share_menu_input.process_mousebuttondown
            root.game_manager.input_processor.process_mousemotion = root.game_manager.input_processor.pass_func #not yet
            root.game_manager.gui.show_info_under_mouse = root.game_manager.gui.pass_func #not yet
            root.game_manager.gui.move_up = root.game_manager.gui.sharemenu.move_up
            root.game_manager.gui.move_down = root.game_manager.gui.sharemenu.move_down
            root.game_manager.gui.move_left = root.game_manager.gui.sharemenu.move_left
            root.game_manager.gui.move_right = root.game_manager.gui.sharemenu.move_right
        case "inventory":
            root.game_manager.gui.draw = root.game_manager.gui.inventory.draw
            root.game_manager.input_processor.process_keydown = root.game_manager.input_processor.inventory_input.process_keydown
            root.game_manager.input_processor.process_mousebuttondown = root.game_manager.input_processor.inventory_input.process_mousebuttondown
            root.game_manager.input_processor.process_mousemotion = root.game_manager.input_processor.pass_func #not yet
            root.game_manager.gui.show_info_under_mouse = root.game_manager.gui.pass_func #not yet
            root.game_manager.gui.move_up = root.game_manager.gui.inventory.move_up
            root.game_manager.gui.move_down = root.game_manager.gui.inventory.move_down
            root.game_manager.gui.move_left = root.game_manager.gui.inventory.move_left
            root.game_manager.gui.move_right = root.game_manager.gui.inventory.move_right
        case "spawn":
            root.game_manager.gui.draw = root.game_manager.gui.spawn.draw
            root.game_manager.input_processor.process_keydown = root.game_manager.input_processor.spawn.process_keydown
            root.game_manager.input_processor.process_mousebuttondown = root.game_manager.input_processor.spawn.process_mousebuttondown
            root.game_manager.input_processor.process_mousemotion = root.game_manager.input_processor.pass_func #not yet
            root.game_manager.gui.show_info_under_mouse = root.game_manager.gui.pass_func #not yet
            root.game_manager.gui.move_up = root.game_manager.gui.spawn.move_up
            root.game_manager.gui.move_down = root.game_manager.gui.spawn.move_down
            root.game_manager.gui.move_left = root.game_manager.gui.spawn.move_left
            root.game_manager.gui.move_right = root.game_manager.gui.spawn.move_right
        case _:
            root.logger.error(f"Unknown window state: {new_state}", f"change_window_state({new_state})")
            return
    root.game_manager.set_x_offset(0)
    root.game_manager.set_y_offset(0)
    root.last_window_state = root.window_state
    root.window_state = new_state
    root.logger.info(f"changed window state from '{root.last_window_state}' to '{root.window_state}'", f"change_window_state({new_state})")
    update_gui()
    root.game_manager.gui.close_all_extra_windows()

def back_window_state():
    change_window_state(root.last_window_state)

def start_the_game(game_name: str="New Game", player_fraction_name: str = "Player's Fraction", game_seed: int=9999):
    root.loading.draw("initialization...", f"Starting the '{game_name}'...")
    root.game_manager.game_name = game_name
    root.game_manager.world_map.map_generate(game_seed)

    root.loading.draw("Set initial GUI state...")
    change_window_state("game")

    root.loading.draw("Create players fraction...")
    root.game_manager.fraction_manager.create_fraction(player_fraction_name, "player", root.player_id)
    root.game_manager.gui.fraction.open_player_fraction()

    root.loading.draw("Loading preset stuff...")
    with open("data/preset.txt", "r") as f:
        for line in f.readlines():
            if line.startswith("#") or line.strip() == "": continue
            root.game_manager.command_line.process_input(line)

    py.display.set_caption(game_name)
    root.logger.info("game started", f"start_the_game({game_name}, {game_seed})")

    root.game_manager.achievments_manager.do_achievment("first_try")