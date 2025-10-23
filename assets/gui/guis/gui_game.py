from ..buttons import *
from ..infoboxs import *
from ..contentbox import *
from ..statistikbox import *
from ..textfield import *
from ..iconbox import *
from ..listof import *
import assets.root as root
from assets.pawns.pawn import Pawn
from assets.decorators import timeit

class GUIGame:
    def __init__(self):
        self.turn_counter = ContentBox(position=(10, 10), value=0, img="turn_ico.png", allowed_range=[0, 9999])
        self.header_info_content = [self.turn_counter]

        self.header_content = [FractionButton(), TechnologyButton(), PolicyButton()]

        self.opened_object = None

        self.targets_coord = (-1, -1)

        self.next_turn_button = NextTurnButton()
        self.show_scheme_list_button = SchemeListButton()
        self.open_building_interface_button = BuildingButton()
        self.show_job_button = ShowJobButton()
        self.open_reciept_button = RecieptButton()
        self.open_inventory_button = OpenInventoryButton()
        self.open_scheme_button = OpenInventoryButton()

        self.jobs_list = None
        self.action_list = None
        self.buildings_list = {}
        self.buildings_types_list = None
        self.scheme_list = []
        self.building_info = []

        self.set_standard_footer()

        self.main_info_window_content = InfoBox(title="Info Box", text="Description", position=(root.window_size[0]-root.interface_size*2, 20))
        self.world_map = root.handler.world_map

        self.sticked_object = None

        self.change_position_for_new_screen_sizes()

    def get_target_coord(self):
        if self.targets_coord == (-1, -1):
            logging("ERROR", f"target coord are {self.targets_coord}", "GUIGame.get_target_coord")
        else:
            logging("INFO", f"target coord are {self.targets_coord}", "GUIGame.get_target_coord")
        return self.targets_coord
    
    def set_target_coord(self, new_target_coord: tuple[int, int]):
        logging("INFO", f"target coord changet from {self.targets_coord} to {new_target_coord}", "GUIGame.set_target_coord")
        self.targets_coord = new_target_coord

    def set_target_coord_null(self):
        logging("INFO", f"target coord reset", "GUIGame.set_target_coord_null")
        self.targets_coord = (-1, -1)

    def set_standard_footer(self):
        self.footer_content = [self.next_turn_button, self.show_scheme_list_button]
    
    def change_position_for_new_screen_sizes(self):
        # Change position of header info content
        header_info_tab = 1
        for i, item in enumerate(self.header_info_content):
            if i == 0:
                item.change_position((10, 10))
            else:
                item_position = self.header_info_content[i-1].rect.topleft
                item_position = (item_position[0]+root.info_box_size[0]+20, item_position[1])
                if item_position[0]+item.width > root.window_size[0]-root.interface_size*2:
                    item_position = (10, item_position[1]+root.info_box_size[1]+5)
                    header_info_tab += 1
                item.change_position(item_position)

        # Header
        header_tab = 0
        for i, item in enumerate(self.header_content):
            if i == 0:
                item.change_position((10, 20+root.info_box_size[1]*header_info_tab))
            else:
                item_position = self.header_content[i-1].rect.topleft
                item_position = (item_position[0]+root.button_standard_size[0]+20, item_position[1])
                if item_position[0]+item.width > root.window_size[0]-root.button_standard_size[0]*2:
                    item_position = (10, item_position[1]+root.button_standard_size[1]+20)
                    header_tab += 1
                item.change_position(item_position)

        # Footer
        footer_tab = 0
        for i, item in enumerate(self.footer_content):
            if i == 0:
                item.change_position((10, root.window_size[1]-root.button_standard_size[1]-20))
            else:
                item_position = self.footer_content[i-1].rect.topleft
                item_position = (item_position[0]+root.button_standard_size[0]+20, root.window_size[1]-root.button_standard_size[1]-20)
                if item_position[0]+item.width > root.window_size[0]:
                    for item in self.footer_content:
                        item.change_position((item.rect.x, root.window_size[1]-root.button_standard_size[1]-20-root.button_standard_size[1]-20))
                    item_position = (10, root.window_size[1]-root.button_standard_size[1]-20)
                    footer_tab += 1
                item.change_position(item_position)
        
        # Main info window
        if self.main_info_window_content:
            item_position = (root.window_size[0]-self.main_info_window_content.width, 20)
            self.main_info_window_content.change_position(item_position)
    
        # World map
        if self.world_map:
            self.world_map.change_position(header_tab, footer_tab, header_info_tab)

        #self.building_reciept_button.change_position((root.window_size[0]-110, 10))
    
    def open_main_info_window(self, data:dict):
        '''
        {"title": title, "text": text}
        '''
        main_info = InfoBox(data.get("title", "unknow_title"), data.get("text", "unknow_text"), position=(root.window_size[0]-root.interface_size*2, 20))
        self.main_info_window_content = main_info
    
    def main_info_window_content_close(self):
        self.main_info_window_content.close()
        self.opened_object = None
        self.set_standard_footer()
        update_gui()

    def choise_scheme(self, scheme: Icon):
        self.sticked_object = Icon(width=scheme.width, height=scheme.height, color=scheme.color, position=(py.mouse.get_pos()[0]-scheme.width//2, py.mouse.get_pos()[1]-scheme.height//2), img=scheme.img, spec_path="data/buildings/img")
        self.hide_scheme_list()

    def open_scheme(self):
        self.footer_content = [self.next_turn_button, self.open_scheme_button]

    def open_scheme_type(self, building_type: str):
        self.scheme_list = []
        for i, building in enumerate(self.buildings_list.get(building_type, [])):
            self.scheme_list.append(Icon(root.cell_sizes[root.cell_size_scale][0], root.cell_sizes[root.cell_size_scale][1], position=(root.interface_size+10+(root.cell_sizes[root.cell_size_scale][1]*i), root.handler.world_map.rect.bottomleft[1]-root.cell_sizes[root.cell_size_scale][1]), img=f"{building.data['img']}", spec_path="data/buildings/img", bg=(125, 125, 125, 255))) #type: ignore
        self.change_position_for_new_screen_sizes()
        update_gui()

    def open_scheme_list(self):
        self.buildings_list = root.handler.buildings_manager.get_all_unique_buildings_sorted_by_types(True)
        self.buildings_types_list = ListOf(list(self.buildings_list.keys()), position=(0, root.handler.world_map.rect.bottomleft[1]), type_of_list="scheme_list", open_direction="up")
        self.change_position_for_new_screen_sizes()
        update_gui()

    def open_building(self):
        self.footer_content = [self.next_turn_button, self.open_building_interface_button, self.open_inventory_button]
        if root.handler.buildings_manager.get_building_by_coord(root.handler.get_chosen_cell_coord()).is_workbench: #type: ignore
            self.footer_content.append(self.open_reciept_button)
        self.opened_object = root.handler.get_chosen_cell().buildings
        self.change_position_for_new_screen_sizes()
        update_gui()

    def open_pawn(self):
        self.footer_content = [self.next_turn_button, self.show_job_button, self.open_inventory_button]
        self.opened_object = root.handler.get_opened_pawn()
        self.change_position_for_new_screen_sizes()
        update_gui()
    
    def show_jobs(self):
        if not root.handler.is_opened_pawn_default():
            self.jobs_list = ListOf(root.handler.job_manager.get_jobs_id_for_pawn(root.handler.get_opened_pawn()), position=self.show_job_button.rect.topleft, type_of_list="job_list")
        update_gui()

    def show_pawn_info(self, pawn: Pawn, mouse_pos: tuple[int, int]):
        pass
    
    def show_building_info(self, coord: tuple[int, int], mouse_pos: tuple[int, int]):
        building = root.handler.buildings_manager.get_building_by_coord(coord)

        building_name = TextField(text=building.name, 
                                    position=(
                                        mouse_pos[0]+10,
                                        mouse_pos[1]+10
                                    ), font_size=20)
        building_service = TextField(text=f"service:*{building.get_service()}/{building.get_max_service()}",
                                    position=(
                                        mouse_pos[0]+10,
                                        mouse_pos[1]+building_name.text_rect.height+10
                                    ), font_size=20)
        building_hp = TextField(text=f"hp:*{building.get_hp()}/{building.get_max_hp()}",
                                position=(
                                    mouse_pos[0]+10,
                                    mouse_pos[1]+building_name.text_rect.height+building_service.text_rect.height+10
                                ), font_size=20)
        building_info_bg = Icon(
            max([building_name.text_rect.width, building_service.text_rect.width, building_hp.text_rect.width])+20,
            sum([building_name.text_rect.height, building_service.text_rect.height, building_hp.text_rect.height])+20, position=(mouse_pos[0], mouse_pos[1]),
            bg=(150, 150, 150, 255)
        )

        self.building_info = [building_info_bg, building_name, building_service, building_hp]
    
    def hide_building_info(self):
        #root.handler.world_map.redraw_cells_under(self.building_info[0])
        self.building_info = []
        root.update_gui()

    def hide_action_list(self):
        self.action_list = None
        self.set_target_coord_null()
        update_gui()
    
    def hide_jobs(self):
        self.jobs_list = None
        update_gui()

    def hide_scheme_list(self):
        self.buildings_types_list = None
        self.scheme_list = []
        update_gui()
    
    def show_actions(self, pawns:list[dict], buildings:dict[str, int]):
        mouse_pos = py.mouse.get_pos()
        if mouse_pos[1] > root.window_size[1]:
            open_direction = "up"
        else:
            open_direction = "down"
        if not root.handler.is_opened_pawn_default():
            action_list = []
            for pawn in pawns:
                if pawn["fraction_id"] != root.player_id:
                    action_list.append(f"attack.{pawn["name"]}")
                else:
                    action_list.append(f"share.with_{pawn["name"]}")
                    if pawn["type"] != root.handler.get_opened_pawn().type and "stand_here" not in action_list:
                        action_list.append("stand_here")
            if buildings.get("fraction_id") == root.player_id:
                action_list.append(f"share.with_{buildings["name"]}")
                if "stand_here" not in action_list and pawns == []:
                    action_list.append("stand_here")
            elif buildings != {}:
                action_list.append(f"attack.{buildings["name"]}")
            self.action_list = ListOf(action_list, position=mouse_pos, open_direction=open_direction, type_of_list="job_list")
        update_gui()

    #@timeit
    def draw(self):
        root.screen.fill((0, 0, 0))
        # Draw world map
        if self.world_map:
            self.world_map.draw()

        # Draw header info content
        for item in self.header_info_content:
            item.draw()

        # Draw header
        for item in self.header_content:
            item.draw()

        # Draw footer
        for item in self.footer_content:
            item.draw()

        if self.jobs_list:
            self.jobs_list.draw()

        # Draw main info window
        if self.main_info_window_content:
            #self.main_info_window_content.draw()
            pass

        if self.action_list:
            self.action_list.draw()

        if self.buildings_types_list:
            self.buildings_types_list.draw()

        for scheme in self.scheme_list:
            scheme.draw()

        if self.sticked_object:
            self.sticked_object.draw()

        if self.building_info != []:
            for info in self.building_info:
                info.draw()

        root.need_update_gui = False