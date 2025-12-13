import pygame as py
from ... import root
from typing import Any, TYPE_CHECKING
from ..basic_input_process import BasicInputProcessor

if TYPE_CHECKING:
    from ...gamemanager import GameManager

from ...world.cell import Cell

class GameInputProcessor(BasicInputProcessor):
    def __init__(self, root_prcessor_input, game_manager: "GameManager"):
        super().__init__(root_prcessor_input, game_manager)

        self._default_cell = self.game_manager.get_default_cell()
        self.cell_under_mouse = self._default_cell

    #@logger
    def process_keydown(self, event:py.event.Event):
        if event.key == py.K_w:
            self.k_w_pressed = True
        elif event.key == py.K_s:
            self.k_s_pressed = True
        elif event.key == py.K_a:
            self.k_a_pressed = True
        elif event.key == py.K_d:
            self.k_d_pressed = True

        elif event.key == py.K_ESCAPE:
            if self.game_manager.command_line.is_active:
                self.game_manager.command_line.deactivete()
            elif not self.game_manager.is_chosen_cell_default():
                self.game_manager.reset_chosen_cell()
                self.game_manager.gui.game.close_main_info_window()
            #elif self.game_manager.gui.game.main_info_window_content.text != "":
            #    self.game_manager.gui.game.close_main_info_window()
            elif self.game_manager.gui.game.sticked_object != None:
                self.game_manager.gui.game.sticked_object = None
            elif any([self.game_manager.gui.game.jobs_list, self.game_manager.gui.game.buildings_types_list, self.game_manager.gui.game.action_list]):
                self.game_manager.gui.close_all_extra_windows()

        elif event.key == py.K_UP:
            root.cell_size_scale += 1
            if root.cell_size_scale > len(root.cell_sizes)-1:
                root.cell_size_scale = len(root.cell_sizes)-1
            self.game_manager.world_map.resize()
            self.game_manager.gui.change_position_for_new_screen_sizes()
            root.update_gui()

        elif event.key == py.K_DOWN:
            root.cell_size_scale -= 1
            if root.cell_size_scale < 0:
                root.cell_size_scale = 0
            self.game_manager.world_map.resize()
            self.game_manager.gui.change_position_for_new_screen_sizes()
            root.update_gui()

        elif event.key == py.K_CARET:
            if self.game_manager.command_line.is_active:
                self.game_manager.command_line.deactivete()
            else:
                self.game_manager.command_line.activete()
            root.update_gui()

        elif event.key == py.K_F1:
            self.game_manager.world_map.change_display_mode("normal")
            root.update_gui()
        elif event.key == py.K_F2:
            self.game_manager.world_map.change_display_mode("fraction")
            root.update_gui()
        elif event.key == py.K_F3:
            self.game_manager.world_map.change_display_mode("temperature")
            root.update_gui()
        elif event.key == py.K_F4:
            self.game_manager.world_map.change_display_mode("humidity")
            root.update_gui()
        elif event.key == py.K_F5:
            self.game_manager.world_map.change_display_mode("height")
            root.update_gui()
        elif event.key == py.K_F6:
            self.game_manager.world_map.change_display_mode("soil_fertility")
            root.update_gui()
        elif event.key == py.K_F7:
            self.game_manager.world_map.change_display_mode("difficulty")
            root.update_gui()

    #@logger
    def process_mousebuttondown(self, event:py.event.Event, rel_mouse_pos:tuple[int, int]):
        if event.button == 1:
            #if self.game_manager.gui.game.jobs_list:
            #    if self.game_manager.gui.game.jobs_list.rect.collidepoint(rel_mouse_pos):
            #        self.game_manager.gui.game.jobs_list.click()
            #        return

            #if self.game_manager.gui.game.action_list:
            #    if self.game_manager.gui.game.action_list.rect.collidepoint(rel_mouse_pos):
            #        self.game_manager.gui.game.action_list.click()
            #        return

            if self.game_manager.gui.game.buildings_types_list:
            #    if self.game_manager.gui.game.buildings_types_list.rect.collidepoint(rel_mouse_pos):
            #        self.game_manager.gui.game.buildings_types_list.click()
            #        return
                
                for scheme in self.game_manager.gui.game.scheme_list:
                    if scheme.bg_rect.collidepoint(rel_mouse_pos):
                        self.game_manager.gui.game.choice_scheme(scheme)
                        return

            if self.game_manager.world_map:
                if self.game_manager.world_map.rect.collidepoint(rel_mouse_pos):
                    self.game_manager.gui.close_all_extra_windows()
                    self.game_manager.world_map.click(rel_mouse_pos, 1)
                    return

            screen_middle = (root.window_size[0] // 2, root.window_size[1] // 2)

            #if rel_mouse_pos[1] < screen_middle[1]:
            #    for item in self.game_manager.gui.game.header_content:
            #        if item.rect.collidepoint(rel_mouse_pos):
            #            item.click(1, rel_mouse_pos)
            #            return
            if rel_mouse_pos[1] > screen_middle[1]:
                for item in self.game_manager.gui.game.footer_content:
                    if item.rect.collidepoint(rel_mouse_pos):
                        item.click(1, rel_mouse_pos)
                        return
            #if rel_mouse_pos[0] > screen_middle[0]:
            #    if gui.main_info_window_content:
            #        if gui.main_info_window_content.rect.collidepoint(rel_mouse_pos):
            #            gui.main_info_window_content.click()
            #            return

            self.game_manager.gui.game.close_main_info_window()
            self.game_manager.world_map.unchose_cell()
            self.game_manager.gui.close_all_extra_windows()
            root.update_gui()
            
        elif event.button == 3:
            if self.game_manager.world_map:
                if self.game_manager.world_map.rect.collidepoint(rel_mouse_pos):
                    self.game_manager.gui.close_all_extra_windows()
                    self.game_manager.world_map.click(rel_mouse_pos, 3)
                    return

        #elif event.button == 4:
        #    root.cell_size_scale += 1
        #    if root.cell_size_scale > len(root.cell_sizes)-1:
        #        root.cell_size_scale = len(root.cell_sizes)-1
        #    self.game_manager.world_map.resize()
        #    self.game_manager.gui.change_position_for_new_screen_sizes()
        #    root.update_gui()

        #elif event.button == 5:
        #    root.cell_size_scale -= 1
        #    if root.cell_size_scale < 0:
        #        root.cell_size_scale = 0
        #    self.game_manager.world_map.resize()
        #    self.game_manager.gui.change_position_for_new_screen_sizes()
        #    root.update_gui()
    
    #@logger
    def process_mousemotion(self, event:py.event.Event):
        mouse_pos = event.pos
        if self.game_manager.gui.game.sticked_object:
            self.game_manager.gui.game.sticked_object.change_position(mouse_pos)
            root.update_gui()
            return

        cell = self.game_manager.get_cell(mouse_click_pos=mouse_pos)
        if cell:
            self.cell_under_mouse = cell
            return

        self.cell_under_mouse = self._default_cell
        self.game_manager.gui.game.hide_info()