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
            root.game.gui.draw = root.game.gui.game.draw
            root.game.input_processor.process_keydown = root.game.input_processor.process_keydown_game
            root.game.input_processor.process_mousebuttondown = root.game.input_processor.process_mousebuttondown_game
            root.game.input_processor.process_mousemotion = root.game.input_processor.process_mousemotion_game
            root.game.gui.close_all_extra_windows()
        case "fraction":
            root.game.gui.draw = root.game.gui.fraction.draw
            root.game.input_processor.process_keydown = root.game.input_processor.process_keydown_fraction
            root.game.input_processor.process_mousebuttondown = root.game.input_processor.process_mousebuttondown_fraction
            root.game.input_processor.process_mousemotion = root.game.input_processor.pass_func #not yet
        case "writing":
            root.game.gui.draw = root.game.gui.writing.draw
            root.game.input_processor.process_keydown = root.game.input_processor.process_keydown_writing
            root.game.input_processor.process_mousebuttondown = root.game.input_processor.process_mousebuttondown_writting
            root.game.input_processor.process_mousemotion = root.game.input_processor.pass_func #not yet
        case "technology":
            root.game.gui.draw = root.game.gui.technology.draw
            root.game.input_processor.process_keydown = root.game.input_processor.process_keydown_technology
            root.game.input_processor.process_mousebuttondown = root.game.input_processor.process_mousebuttondown_technology
            root.game.input_processor.process_mousemotion = root.game.input_processor.pass_func #not yet
        case "policy":
            root.game.gui.draw = root.game.gui.policy.draw
            root.game.input_processor.process_keydown = root.game.input_processor.process_keydown_policy
            root.game.input_processor.process_mousebuttondown = root.game.input_processor.process_mousebuttondown_policy
            root.game.input_processor.process_mousemotion = root.game.input_processor.pass_func #not yet
        case "building":
            root.game.gui.draw = root.game.gui.building.draw
            root.game.input_processor.process_keydown = root.game.input_processor.process_keydown_building
            root.game.input_processor.process_mousebuttondown = root.game.input_processor.process_mousebuttondown_building
            root.game.input_processor.process_mousemotion = root.game.input_processor.pass_func #not yet
        case "reciept":
            root.game.gui.draw = root.game.gui.reciept.draw
            root.game.input_processor.process_keydown = root.game.input_processor.process_keydown_reciept
            root.game.input_processor.process_mousebuttondown = root.game.input_processor.process_mousebuttondown_reciept
            root.game.input_processor.process_mousemotion = root.game.input_processor.pass_func #not yet
        case "share_menu":
            root.game.gui.draw = root.game.gui.sharemenu.draw
            root.game.input_processor.process_keydown = root.game.input_processor.process_keydown_share_menu
            root.game.input_processor.process_mousebuttondown = root.game.input_processor.process_mousebuttondown_share_menu
            root.game.input_processor.process_mousemotion = root.game.input_processor.pass_func #not yet
        case "inventory":
            root.game.gui.draw = root.game.gui.inventory.draw
            root.game.input_processor.process_keydown = root.game.input_processor.process_keydown_inventory
            root.game.input_processor.process_mousebuttondown = root.game.input_processor.process_mousebuttondown_inventory
            root.game.input_processor.process_mousemotion = root.game.input_processor.pass_func #not yet
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
    root.game.world_map.map_generate(game_seed)

    loading.draw("Set initial GUI state...")
    #Set initial GUI state
    change_window_state("game")

    loading.draw("Create players fraction...")
    #Create players fraction
    root.game.allFractions.create_fraction("Player's Fraction", "player", root.player_id)
    root.game.gui.fraction.open_player_fraction()

    loading.draw("Loading preset stuff...")
    #For the testrun
    root.game.buildings_manager.build("manufactory", (0, 1), root.player_id)
    root.game.pawns_manager.spawn("pawn_0", (1, 0), root.player_id)
    root.game.pawns_manager.spawn("pawn_1", (2, 0), root.player_id)
    root.game.pawns_manager.spawn("pawn_2", (3, 0), root.player_id)
    root.game.pawns_manager.spawn("pawn_3", (4, 0), root.player_id)
    #root.game.pawns_manager.add_resource(0, "resource_0", 2)

    logger.info("game started", f"start_the_game({game_name}, {game_seed})")