import pygame as py
from ..buttons import *
from ..infoboxs import *
from ..contentbox import *
from ..statistikbox import *
from ..textfield import *
from ..iconbox import *
from ..listof import *
from ..inputfield import *
from ... import root
from ...root import logger
from ...auxiliary_stuff import *
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from managers.pawns.pawn import Pawn
    from world.cell import Cell
    from ...gamemanager import GameManager

class GUIGame:
    def __init__(self, game_manager: "GameManager"):
        self.game_manager = game_manager

        self.turn_counter = ContentBox(position=(10, 10), value=0, img="turn_ico.png", allowed_range=[0, 9999])
        self.type_science_0 = ContentBox(position=(10, 10), value=0, allowed_range=[0, 9999])
        self.type_science_1 = ContentBox(position=(10, 10), value=0, allowed_range=[0, 9999])
        self.science_contentboxes = [self.type_science_0, self.type_science_1]
        self.header_info_content = [self.turn_counter, self.type_science_0, self.type_science_1]

        self.header_content: list[Button] = [FractionButton(), TechnologyButton(), PolicyButton()]

        self.next_turn_button = NextTurnButton()
        self.show_scheme_list_button = SchemeListButton()
        self.open_building_interface_button = BuildingButton()
        self.show_job_button = ShowJobButton()
        self.open_reciept_button = RecieptButton()
        self.open_inventory_button = OpenInventoryButton()
        self.open_scheme_button = OpenInventoryButton()
        self.open_spawn_button = OpneSpawnButton()
        self.cancel_upgrade_button = CancelUpgradeButton()

        self.jobs_list: None|ListOf = None
        self.action_list: None|ListOf = None
        self.buildings_list = {}
        self.buildings_types_list = None
        self.scheme_list = []
        self.cell_info: list[TextField|Icon] = []
        self.cell_under_mouse: "Cell" = self.game_manager.get_default_cell()

        self.set_standard_footer()

        self.main_info_window_content = TextField(int(root.interface_size*1.5), 60, font_size=60 , positioning="right", auto_width=True)

        self.sticked_object = None

        self.change_position_for_new_screen_sizes()

    def set_standard_footer(self):
        self.footer_content: list[Button] = [self.next_turn_button, self.show_scheme_list_button]

    def update_header_info_content(self) -> int:
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
        return header_info_tab

    def update_header_tab_content(self, header_info_tab: int) -> tuple[int, int]:
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

        self.game_manager.messenger.change_position((10, (root.button_standard_size[1]+20)*(header_tab+1)+20+root.info_box_size[1]*header_info_tab))
        return header_info_tab, header_tab
    
    def update_footer_tab_content(self) -> int:
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

        return footer_tab
    
    def change_position_for_new_screen_sizes(self):
        header_info_tab = self.update_header_info_content()
        header_info_tab, header_tab = self.update_header_tab_content(header_info_tab)
        footer_tab = self.update_footer_tab_content()
        
        # Main info window
        if self.main_info_window_content:
            item_position = (root.window_size[0], root.window_size[1]-self.main_info_window_content.rect.height-(root.button_standard_size[1]+20)*(footer_tab+1)-10)
            self.main_info_window_content.change_position(item_position)
    
        # World map
        if self.game_manager.world_map:
            self.game_manager.world_map.change_position(header_tab, footer_tab, header_info_tab)

        #self.building_reciept_button.change_position((root.window_size[0]-110, 10))
    
    def open_main_info_window(self, text: str):
        self.main_info_window_content.set_text(text)
    
    def close_main_info_window(self):
        self.main_info_window_content.set_text("")
        update_gui()

    def choice_scheme(self, scheme: Icon):
        self.sticked_object = Icon(width=scheme.width, height=scheme.height, color=scheme.color, position=(py.mouse.get_pos()[0]-scheme.width//2, py.mouse.get_pos()[1]-scheme.height//2), img=scheme.img, spec_path="data/buildings/img")
        self.hide_scheme_list()

    def open_scheme(self):
        self.footer_content = [self.next_turn_button, self.open_scheme_button]

    def open_scheme_type(self, building_category: str):
        self.scheme_list = []
        cell_side_size = get_cell_side_size()
        for i, building in enumerate(self.buildings_list.get(building_category, [])):
            self.scheme_list.append(
                Icon(cell_side_size, cell_side_size,
                    position=(
                        root.interface_size+10+(cell_side_size*i),
                        self.game_manager.world_map.rect.bottomleft[1]-cell_side_size
                    ),
                    img=f"{building['img']}",
                    spec_path="data/buildings/img/",
                    bg=(125, 125, 125, 255))
                )
        #self.change_position_for_new_screen_sizes()
        update_gui()

    def open_scheme_list(self):
        self.buildings_list = self.game_manager.buildings_manager.get_all_unique_buildings_sorted_by_categories(True)
        self.buildings_types_list = ListOf(
            list(self.buildings_list.keys()),
            position=(0, self.game_manager.world_map.rect.bottomleft[1]),
            open_direction="up",
            window_state="game",
            func=partial(root.game_manager.gui.game.open_scheme_type)
            )
        #self.change_position_for_new_screen_sizes()
        update_gui()

    def open_building(self):
        building = self.game_manager.get_chosen_building()
        self.footer_content = [self.next_turn_button]
        if not building.is_scheme:
            self.footer_content.append(self.open_building_interface_button)
        else:
            self.footer_content.append(self.cancel_upgrade_button)
        self.footer_content.append(self.open_inventory_button)
        if building.is_workbench and not building.is_scheme:
            self.footer_content.append(self.open_reciept_button)
        if building.is_town and not building.is_scheme:
            self.footer_content.append(self.open_spawn_button)
        self.update_footer_tab_content()
        update_gui()

    def open_pawn(self):
        self.footer_content = [self.next_turn_button, self.show_job_button, self.open_inventory_button]
        self.update_footer_tab_content()
        update_gui()
    
    def show_jobs(self):
        if not self.game_manager.is_chosen_pawn_default():
            self.jobs_list = ListOf(
                self.game_manager.job_manager.get_jobs_id_for_pawn(self.game_manager.get_chosen_pawn()),
                position=self.show_job_button.rect.topleft,
                window_state="game",
                func=partial(self.game_manager.pawns_manager.do_job, root.game_manager.get_chosen_pawn())
            )
        update_gui()

    def show_achievments(self, achievment: dict):
        pass

    def show_info_about_cell_under_mouse(self):
        if root.game_manager.get_cell_under_mouse() == self.cell_under_mouse: return

        cell = self.game_manager.get_cell_under_mouse()
        if cell.is_default: return

        mouse_pos = py.mouse.get_pos()

        if self.action_list != None and self.action_list.rect.collidepoint(mouse_pos): return
        if self.jobs_list != None and self.jobs_list.rect.collidepoint(mouse_pos): return
        self.cell_under_mouse = cell

        cell_info: list[list[TextField]] = [[]]
        self.cell_info = []
        y_offset = 0
        font_size = 25

        fraction = self.game_manager.fraction_manager.get_player_fraction()

        if self.game_manager.world_map.display_mode == "normal":
            tettain_name = cell.type if cell.is_opened else "not researched cell"
            move_points = f"[{cell.data["subdata"].get("movement_points")}]" if cell.data["subdata"].get("movement_points") != None else ""
            auxiliary_cell_info = f"(x:{cell.coord[0]} y:{cell.coord[1]}) {move_points}"
            
            terrain = TextField(text="terrain_name", text_kwargs={"name": tettain_name, "auxiliary_cell_info": auxiliary_cell_info},
                                    position=(
                                        mouse_pos[0]+10,
                                        mouse_pos[1]
                                    ), font_size=font_size, bg_color=(0, 0, 0, 0))
            cell_info[-1].append(terrain)
            if cell.flora != {} and cell.is_opened:
                flora = TextField(text=cell.flora["name"],
                                    position=(
                                        mouse_pos[0]+10,
                                        mouse_pos[1]+terrain.text_rect.height
                                    ), font_size=font_size, bg_color=(0, 0, 0, 0))
                cell_info[-1].append(flora)
            if cell.fauna != {} and cell.is_opened:
                fauna = TextField(text=cell.fauna["name"],
                                    position=(
                                        mouse_pos[0]+10,
                                        mouse_pos[1]+terrain.text_rect.height+flora.text_rect.height if cell.flora != {} else mouse_pos[1]+terrain.text_rect.height #type: ignore
                                    ), font_size=font_size, bg_color=(0, 0, 0, 0))
                cell_info[-1].append(fauna)
        else:
            terrain = TextField(text="terrain_characteristic", text_kwargs={"key": self.game_manager.world_map.display_mode, "value": cell.get(self.game_manager.world_map.display_mode)},
                                position=(
                                        mouse_pos[0]+10,
                                        mouse_pos[1]
                                    ), font_size=font_size, bg_color=(0, 0, 0, 0))
            cell_info[-1].append(terrain)
        y_offset += sum([info.text_rect.height for info in cell_info[-1]])+10

        if cell.buildings != {} and cell.is_opened:
            cell_info.append([])
            building = self.game_manager.get_building(coord=cell.coord)

            building_name = TextField(text=f"*{building.name}", 
                                        position=(
                                            mouse_pos[0]+10,
                                            mouse_pos[1]+y_offset+10
                                        ), font_size=font_size, bg_color=(0, 0, 0, 0))
            building_service = TextField(text="service_level", text_kwargs={"service_now": building.get_service(), "service_max": building.get_max_service()},
                                        position=(
                                            mouse_pos[0]+10,
                                            mouse_pos[1]+y_offset+building_name.text_rect.height+10
                                        ), font_size=font_size, bg_color=(0, 0, 0, 0))
            building_hp = TextField(text="building_hp_level", text_kwargs={"hp_now": building.get_hp(), "hp_max": building.get_max_hp()},
                                    position=(
                                        mouse_pos[0]+10,
                                        mouse_pos[1]+y_offset+building_name.text_rect.height+building_service.text_rect.height+10
                                    ), font_size=font_size, bg_color=(0, 0, 0, 0))
            building_belongs = TextField(text="building_belongs", text_kwargs={"fraction_name": fraction.name},
                                        position=(
                                            mouse_pos[0]+10,
                                            mouse_pos[1]+y_offset+building_name.text_rect.height+building_service.text_rect.height+building_hp.text_rect.height+10
                                        ), font_size=font_size, bg_color=(0, 0, 0, 0))
            building_can_work = TextField(text="can_work" if building.can_work else "can_not_work",
                                        position=(
                                            mouse_pos[0]+10,
                                            mouse_pos[1]+y_offset+building_name.text_rect.height+building_service.text_rect.height+building_hp.text_rect.height+building_belongs.text_rect.height+10
                                        ), font_size=font_size, bg_color=(0, 0, 0, 0))

            cell_info[-1].append(building_name)
            cell_info[-1].append(building_service)
            cell_info[-1].append(building_hp)
            cell_info[-1].append(building_belongs)
            cell_info[-1].append(building_can_work)

            y_offset += sum([building_name.text_rect.height, building_service.text_rect.height, building_hp.text_rect.height, building_belongs.text_rect.height, building_can_work.text_rect.height])

            if building.is_town:
                population = building.town.get_population()
                for group, pop in population.items():
                    town_pop = TextField(text=f"population_group_size", text_kwargs={"group": group, "size": pop},
                                        position=(
                                            mouse_pos[0]+10,
                                            mouse_pos[1]+y_offset+10
                                        ), font_size=font_size, bg_color=(0, 0, 0, 0))
                    cell_info[-1].append(town_pop)
                    y_offset += town_pop.text_rect.height
                y_offset += 10

        if cell.pawns != [] and cell.is_opened:
            for pawn_in_cell in cell.pawns:
                cell_info.append([])
                pawn = self.game_manager.get_pawn(pawn_id=pawn_in_cell["id"])
                pawn_name = TextField(text=f"*{pawn.name}",
                                       position=(
                                           mouse_pos[0]+10,
                                           mouse_pos[1]+y_offset+10
                                       ), font_size=font_size, bg_color=(0, 0, 0, 0))
                pawn_hp = TextField(text="pawn_hp_level",text_kwargs={"hp_now": pawn.get_hp(), "hp_max": pawn.get_max_hp()},
                                    position=(
                                        mouse_pos[0]+10,
                                        mouse_pos[1]+y_offset+pawn_name.text_rect.height+10
                                    ), font_size=font_size, bg_color=(0, 0, 0, 0))
                pawn_belongs = TextField(text="pawn_belongs", text_kwargs={"fraction_name": fraction.name},
                                        position=(
                                            mouse_pos[0]+10,
                                            mouse_pos[1]+y_offset+pawn_name.text_rect.height+pawn_hp.text_rect.height+10
                                        ), font_size=font_size, bg_color=(0, 0, 0, 0))

                cell_info[-1].append(pawn_name)
                cell_info[-1].append(pawn_hp)
                cell_info[-1].append(pawn_belongs)

                y_offset += sum([pawn_name.text_rect.height, pawn_hp.text_rect.height, pawn_belongs.text_rect.height])+10

        if cell_info != []:
            y_offset = 0
            max_width = 0
            for info in cell_info:
                new_max_width = max([content.text_rect.width for content in info])
                if new_max_width > max_width:
                    max_width = new_max_width
            
            if mouse_pos[0]+5+max_width+20 > root.window_size[0]:
                x_offset = max_width + 25
                pos = (mouse_pos[0] - x_offset, mouse_pos[1])
            else:
                x_offset = 0
                pos = mouse_pos

            for info in cell_info:
                bg = Icon(
                    max_width+20,
                    sum([content.text_rect.height for content in info])+10,
                    position=(pos[0]+5, pos[1]+y_offset),
                    bg=(150, 150, 150, 255)
                )
                y_offset += bg.rect.height+5
                self.cell_info.append(bg)
                for info_content in info:
                    info_content.change_position((info_content.position[0]-x_offset, info_content.position[1]))
                    self.cell_info.append(info_content)

        update_gui()
 
    def hide_info(self):
        self.cell_info = []
        update_gui()

    def hide_action_list(self):
        self.action_list = None
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
        if not self.game_manager.is_chosen_pawn_default():
            action_list = []
            for pawn in pawns:
                if pawn["fraction_id"] != root.player_id:
                    action_list.append(f"attack.{pawn["type"]}")
                else:
                    action_list.append(f"share.with_{pawn["type"]}")
                    if pawn["type"] != self.game_manager.get_chosen_pawn().type and "stand_here" not in action_list:
                        action_list.append("stand_here")
            if buildings.get("fraction_id") == root.player_id:
                action_list.append(f"share.with_{buildings["type"]}")
                if "stand_here" not in action_list and is_empty(pawns):
                    action_list.append("stand_here")
            elif buildings != {}:
                action_list.append(f"attack.{buildings["type"]}")
            self.action_list = ListOf(
                action_list,
                position=mouse_pos,
                open_direction=open_direction,
                window_state="game",
                func=partial(self.game_manager.pawns_manager.do_job, root.game_manager.get_chosen_pawn())
            )
        update_gui()

    #@timeit
    def draw(self):
        root.screen.fill((0, 0, 0))

        # Draw world map
        if self.game_manager.world_map:
            self.game_manager.world_map.draw()

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
        if self.main_info_window_content.text != "":
            self.main_info_window_content.draw()
            pass

        if self.action_list:
            self.action_list.draw()

        if self.buildings_types_list:
            self.buildings_types_list.draw()

        for scheme in self.scheme_list:
            scheme.draw()

        if self.sticked_object:
            self.sticked_object.draw()

        if self.cell_info != []:
            for info in self.cell_info:
                info.draw()

        root.need_update_gui = False
    
    def move_up(self):
        self.game_manager.world_map.move_map_up()

    def move_down(self):
        self.game_manager.world_map.move_map_down()

    def move_left(self):
        self.game_manager.world_map.move_map_left()

    def move_right(self):
        self.game_manager.world_map.move_map_right()