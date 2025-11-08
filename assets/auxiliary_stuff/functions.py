import pygame as py
from .. import root
from assets.root import loading, logger

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
    root.last_window_state, root.window_state = root.window_state, new_state
    logger.info(f"changed window state from '{root.last_window_state}' to '{root.window_size}'", f"change_window_state({new_state})")
    update_gui()
    root.game_manager.gui.close_all_extra_windows()

    match root.window_state:
        case "game":
            root.game_manager.gui.draw = root.game_manager.gui.game.draw
            root.game_manager.input_processor.process_keydown = root.game_manager.input_processor.game_input.process_keydown
            root.game_manager.input_processor.process_mousebuttondown = root.game_manager.input_processor.game_input.process_mousebuttondown
            root.game_manager.input_processor.process_mousemotion = root.game_manager.input_processor.game_input.process_mousemotion
        case "fraction":
            root.game_manager.gui.draw = root.game_manager.gui.fraction.draw
            root.game_manager.input_processor.process_keydown = root.game_manager.input_processor.fraction_input.process_keydown
            root.game_manager.input_processor.process_mousebuttondown = root.game_manager.input_processor.fraction_input.process_mousebuttondown
            root.game_manager.input_processor.process_mousemotion = root.game_manager.input_processor.pass_func #not yet
        case "writing":
            root.game_manager.gui.draw = root.game_manager.gui.writing.draw
            root.game_manager.input_processor.process_keydown = root.game_manager.input_processor.writing_input.process_keydown
            root.game_manager.input_processor.process_mousebuttondown = root.game_manager.input_processor.writing_input.process_mousebuttondown
            root.game_manager.input_processor.process_mousemotion = root.game_manager.input_processor.pass_func #not yet
        case "technology":
            root.game_manager.gui.draw = root.game_manager.gui.technology.draw
            root.game_manager.input_processor.process_keydown = root.game_manager.input_processor.technology_input.process_keydown
            root.game_manager.input_processor.process_mousebuttondown = root.game_manager.input_processor.technology_input.process_mousebuttondown
            root.game_manager.input_processor.process_mousemotion = root.game_manager.input_processor.pass_func #not yet
        case "policy":
            root.game_manager.gui.draw = root.game_manager.gui.policy.draw
            root.game_manager.input_processor.process_keydown = root.game_manager.input_processor.policy_input.process_keydown
            root.game_manager.input_processor.process_mousebuttondown = root.game_manager.input_processor.policy_input.process_mousebuttondown
            root.game_manager.input_processor.process_mousemotion = root.game_manager.input_processor.pass_func #not yet
        case "building":
            root.game_manager.gui.draw = root.game_manager.gui.building.draw
            root.game_manager.input_processor.process_keydown = root.game_manager.input_processor.building_input.process_keydown
            root.game_manager.input_processor.process_mousebuttondown = root.game_manager.input_processor.building_input.process_mousebuttondown
            root.game_manager.input_processor.process_mousemotion = root.game_manager.input_processor.pass_func #not yet
        case "reciept":
            root.game_manager.gui.draw = root.game_manager.gui.reciept.draw
            root.game_manager.input_processor.process_keydown = root.game_manager.input_processor.reciept_input.process_keydown
            root.game_manager.input_processor.process_mousebuttondown = root.game_manager.input_processor.reciept_input.process_mousebuttondown
            root.game_manager.input_processor.process_mousemotion = root.game_manager.input_processor.pass_func #not yet
        case "share_menu":
            root.game_manager.gui.draw = root.game_manager.gui.sharemenu.draw
            root.game_manager.input_processor.process_keydown = root.game_manager.input_processor.share_menu_input.process_keydown
            root.game_manager.input_processor.process_mousebuttondown = root.game_manager.input_processor.share_menu_input.process_mousebuttondown
            root.game_manager.input_processor.process_mousemotion = root.game_manager.input_processor.pass_func #not yet
        case "inventory":
            root.game_manager.gui.draw = root.game_manager.gui.inventory.draw
            root.game_manager.input_processor.process_keydown = root.game_manager.input_processor.inventory_input.process_keydown
            root.game_manager.input_processor.process_mousebuttondown = root.game_manager.input_processor.inventory_input.process_mousebuttondown
            root.game_manager.input_processor.process_mousemotion = root.game_manager.input_processor.pass_func #not yet
        case _:
            logger.error(f"Unknown window state: {root.window_state}", f"change_window_state({new_state})")

def back_window_state():
    root.window_state, root.last_window_state = root.last_window_state, root.window_state
    change_window_state(root.window_state)
    update_gui()

def start_the_game(game_name: str="New Game", game_seed: int=9999):
    loading.draw("Starting the game...")
    #Initialize game state
    root.game_manager.game_name = game_name
    root.game_manager.world_map.map_generate(game_seed)

    loading.draw("Set initial GUI state...")
    #Set initial GUI state
    change_window_state("game")

    loading.draw("Create players fraction...")
    #Create players fraction
    root.game_manager.fraction_manager.create_fraction("Player's Fraction", "player", root.player_id)
    root.game_manager.gui.fraction.open_player_fraction()

    loading.draw("Loading preset stuff...")
    with open("data/preset.txt", "r") as f:
        for line in f.readlines():
            root.game_manager.command_line.process_input(line)
    #For the testrun
    #root.game_manager.buildings_manager.build("manufactory", (0, 1), root.player_id)
    #root.game_manager.buildings_manager.build("storage", (0, 2), root.player_id)
    #root.game_manager.buildings_manager.build("lumberjack", (0, 3), root.player_id)
    #root.game_manager.pawns_manager.spawn("pawn_0", (1, 0), root.player_id)
    #root.game_manager.pawns_manager.spawn("pawn_1", (2, 0), root.player_id)
    #root.game_manager.pawns_manager.spawn("pawn_2", (3, 0), root.player_id)
    #root.game_manager.pawns_manager.spawn("pawn_3", (4, 0), root.player_id)
    #root.game_manager.pawns_manager.add_resource(0, "resource_0", 2)

    #from assets.gui.inputfield import InputField
    #root.game_manager.add_inputfield(InputField(width=200, height=50, bg_color=(100, 100, 100, 255), font_size=50))

    py.display.set_caption(game_name)
    logger.info("game started", f"start_the_game({game_name}, {game_seed})")