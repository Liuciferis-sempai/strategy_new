import pygame as py
import root
import copy

def update_gui():
    '''
    update all gui element
    '''
    root.need_update_gui = True

def can_be_int(value: str) -> bool:
    try:
        int(value)
        return True
    except:
        return False

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
    root.last_window_state = root.window_state
    root.window_state = new_state
    root.logger.info(f"changed window state from '{root.last_window_state}' to '{root.window_state}'", f"change_window_state({new_state})")
    update_gui()
    root.game_manager.gui.close_all_extra_windows()

def back_window_state():
    change_window_state(root.last_window_state)

def start_the_game(game_name: str="New Game", game_seed: int=9999):
    root.loading.draw("Starting the game...")
    root.game_manager.game_name = game_name
    root.game_manager.world_map.map_generate(game_seed)

    root.loading.draw("Set initial GUI state...")
    change_window_state("game")

    root.loading.draw("Create players fraction...")
    root.game_manager.fraction_manager.create_fraction("Player's Fraction", "player", root.player_id)
    root.game_manager.gui.fraction.open_player_fraction()

    root.loading.draw("Loading preset stuff...")
    with open("data/preset.txt", "r") as f:
        for line in f.readlines():
            root.game_manager.command_line.process_input(line)

    py.display.set_caption(game_name)
    root.logger.info("game started", f"start_the_game({game_name}, {game_seed})")