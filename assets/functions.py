from . import root
from assets.root import loading, logger

def update_gui():
    '''
    update all gui element
    '''
    root.need_update_gui = True

def change_window_state(new_state:str):
    root.last_window_state = root.window_state
    root.window_state = new_state
    update_gui()

    match root.window_state:
        case "game":
            root.handler.gui.draw = root.handler.gui.game.draw
            root.handler.input_processor.process_keydown = root.handler.input_processor.process_keydown_game
            root.handler.input_processor.process_mousebuttondown = root.handler.input_processor.process_mousebuttondown_game
            root.handler.input_processor.process_mousemotion = root.handler.input_processor.process_mousemotion_game
            root.handler.gui.clouse_all_extra_windows()
        case "fraction":
            root.handler.gui.draw = root.handler.gui.fraction.draw
            root.handler.input_processor.process_keydown = root.handler.input_processor.process_keydown_fraction
            root.handler.input_processor.process_mousebuttondown = root.handler.input_processor.process_mousebuttondown_fraction
            root.handler.input_processor.process_mousemotion = root.handler.input_processor.pass_func #not yet
        case "writing":
            root.handler.gui.draw = root.handler.gui.writing.draw
            root.handler.input_processor.process_keydown = root.handler.input_processor.process_keydown_writing
            root.handler.input_processor.process_mousebuttondown = root.handler.input_processor.process_mousebuttondown_writting
            root.handler.input_processor.process_mousemotion = root.handler.input_processor.pass_func #not yet
        case "technology":
            root.handler.gui.draw = root.handler.gui.technology.draw
            root.handler.input_processor.process_keydown = root.handler.input_processor.process_keydown_technology
            root.handler.input_processor.process_mousebuttondown = root.handler.input_processor.process_mousebuttondown_technology
            root.handler.input_processor.process_mousemotion = root.handler.input_processor.pass_func #not yet
        case "policy":
            root.handler.gui.draw = root.handler.gui.policy.draw
            root.handler.input_processor.process_keydown = root.handler.input_processor.process_keydown_policy
            root.handler.input_processor.process_mousebuttondown = root.handler.input_processor.process_mousebuttondown_policy
            root.handler.input_processor.process_mousemotion = root.handler.input_processor.pass_func #not yet
        case "building":
            root.handler.gui.draw = root.handler.gui.building.draw
            root.handler.input_processor.process_keydown = root.handler.input_processor.process_keydown_building
            root.handler.input_processor.process_mousebuttondown = root.handler.input_processor.process_mousebuttondown_building
            root.handler.input_processor.process_mousemotion = root.handler.input_processor.pass_func #not yet
        case "reciept":
            root.handler.gui.draw = root.handler.gui.reciept.draw
            root.handler.input_processor.process_keydown = root.handler.input_processor.process_keydown_reciept
            root.handler.input_processor.process_mousebuttondown = root.handler.input_processor.process_mousebuttondown_reciept
            root.handler.input_processor.process_mousemotion = root.handler.input_processor.pass_func #not yet
        case "share_menu":
            root.handler.gui.draw = root.handler.gui.sharemenu.draw
            root.handler.input_processor.process_keydown = root.handler.input_processor.process_keydown_share_menu
            root.handler.input_processor.process_mousebuttondown = root.handler.input_processor.process_mousebuttondown_share_menu
            root.handler.input_processor.process_mousemotion = root.handler.input_processor.pass_func #not yet
        case "inventory":
            root.handler.gui.draw = root.handler.gui.inventory.draw
            root.handler.input_processor.process_keydown = root.handler.input_processor.process_keydown_inventory
            root.handler.input_processor.process_mousebuttondown = root.handler.input_processor.process_mousebuttondown_inventory
            root.handler.input_processor.process_mousemotion = root.handler.input_processor.pass_func #not yet
        case _:
            logger.error(f"Unknown window state: {root.window_state}", f"change_window_state({new_state})")

def back_window_state():
    root.window_state, root.last_window_state = root.last_window_state, root.window_state
    change_window_state(root.window_state)
    update_gui()

def start_the_game(game_name: str="New Game", game_seed: int=9999):
    loading.draw("Starting the game...")
    #Initialize game state
    root.game_name = game_name
    root.handler.world_map.map_generate(game_seed)

    loading.draw("Set initial GUI state...")
    #Set initial GUI state
    change_window_state("game")

    loading.draw("Create players fraction...")
    #Create players fraction
    root.handler.allFractions.create_fraction("Player's Fraction", "player", root.player_id)
    root.handler.gui.fraction.open_player_fraction()

    loading.draw("Loading preset stuff...")
    #For the testrun
    root.handler.buildings_manager.build("manufactory", (0, 1), root.player_id)
    root.handler.pawns_manager.spawn("pawn_0", (1, 0), root.player_id)
    root.handler.pawns_manager.spawn("pawn_1", (2, 0), root.player_id)
    root.handler.pawns_manager.spawn("pawn_2", (3, 0), root.player_id)
    root.handler.pawns_manager.spawn("pawn_3", (4, 0), root.player_id)
    #root.handler.pawns_manager.add_resource(0, "resource_0", 2)

    logger.info("game started", f"start_the_game({game_name}, {game_seed})")