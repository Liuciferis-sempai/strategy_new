from assets.world.cell import Cell
from assets import root
from assets.root import logger

class EffectManager:
    def __init__(self):
        pass
    
    def clear_the_queue(self, cell: Cell, reciept: dict):
        root.game_manager.buildings_manager.get_building_by_coord(cell.coord).remove_from_queue(reciept) #type: ignore
        
    def do(self, effect_type: str, effect_data):
        '''
        effect_type:
        - take_resources_from_building (buildings only) args: cell: Cell, resources: dict[str: int]
        - add_item_to_building (buildings only) args: cell: Cell, resources: dict[str: int]
        - clear_the_queue (buildings only) args: cell: Cell, value: int
        - restore_movement_points (pawns only) args: target: int (pawn's id)
        - add_resource (pawns only) args: target: int|Pawn, resource: str, amout: int
        - open_share_menu
        '''
        logger.info(f"execution the effect {effect_type} with data: {effect_data}", f"EffectManager.do({effect_type}, {effect_data})")
        match effect_type:
            case "take_resources_from_building":
                root.game_manager.buildings_manager.remove_resource(effect_data["cell"], effect_data["resources"])
            case "add_item_to_building":
                root.game_manager.buildings_manager.add_resources(effect_data["cell"], effect_data["items"])
            case "clear_the_queue":
                self.clear_the_queue(effect_data["cell"], effect_data["reciept"])
            case "restore_movement_points":
                root.game_manager.pawns_manager.restore_movement_points(effect_data["target"])
            case "add_resource":
                root.game_manager.pawns_manager.add_resource(effect_data["target"], effect_data["resource"], effect_data["amout"])
            case "open_share_menu":
                root.change_window_state("share_menu")
                root.game_manager.gui.sharemenu.open(effect_data["target_of_action"])
            case "stand_here":
                root.game_manager.pawns_manager.move_pawn(effect_data["target"], effect_data["target_cell"])
            case "build_scheme":
                root.game_manager.buildings_manager.build(effect_data["target_building_str"], effect_data["building_coord"], effect_data["building_fraction"])
            case _:
                logger.error(f"effect {effect_type} not found", f"EffectManager.do({effect_type}, {effect_data})")