from assets.world.cell import Cell
from assets import root
from assets.functions import logging

class EffectManager:
    def __init__(self):
        pass
    
    def clear_the_queue(self, cell: Cell, reciept: dict):
        root.handler.buildings_manager.get_building_by_coord(cell.coord).remove_from_queue(reciept) #type: ignore
        
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
        logging("INFO", f"execution the effect {effect_type} with data: {effect_data}", "EffectManager.do")
        match effect_type:
            case "take_resources_from_building":
                root.handler.buildings_manager.remove_resource(effect_data["cell"], effect_data["resources"])
            case "add_item_to_building":
                root.handler.buildings_manager.add_resources(effect_data["cell"], effect_data["items"])
            case "clear_the_queue":
                self.clear_the_queue(effect_data["cell"], effect_data["reciept"])
            case "restore_movement_points":
                root.handler.pawns_manager.restore_movement_points(effect_data["target"])
            case "add_resource":
                root.handler.pawns_manager.add_resource(effect_data["target"], effect_data["resource"], effect_data["amout"])
            case "open_share_menu":
                root.change_window_state("share_menu")
                root.handler.gui.sharemenu.open(effect_data["target_of_action"])
            case "stand_here":
                root.handler.pawns_manager.move_pawn(effect_data["target"], effect_data["target_cell"])
            case "build_scheme":
                root.handler.buildings_manager.build(effect_data["target_building_str"], effect_data["building_coord"], effect_data["building_fraction"])
            case _:
                logging("ERROR", f"effect {effect_type} not found", "Effectmanager.do")