import pygame as py
from .. import root
import copy
from typing import Any, TypeGuard
import time
from random import randint, choice

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
    
def wrap_text(text: str, max_width: int, font: py.font.Font | None = None) -> list[str]:
    if font is None:
        font = py.font.Font(None, 20)
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