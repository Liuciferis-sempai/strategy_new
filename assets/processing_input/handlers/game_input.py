import pygame as py
import assets.root as root
from assets.processing_input.basic_input_process import BasicInputProcessor
from assets.world.cell import Cell

class GameInputProcessor(BasicInputProcessor):
    def __init__(self, root_prcessor_input):
        super().__init__(root_prcessor_input)

        self._default_cell = Cell()
        self.cell_under_mouse = self._default_cell

    def is_move_button_pressed(self):
        if any([self.k_a_pressed, self.k_d_pressed, self.k_s_pressed, self.k_w_pressed]):
            return True

    def move(self):
        if root.window_state == "game" and not root.input_field_active:
            if self.k_w_pressed:
                root.game_manager.gui.game.world_map.move_map_up()
            elif self.k_s_pressed:
                root.game_manager.gui.game.world_map.move_map_down()
            if self.k_a_pressed:
                root.game_manager.gui.game.world_map.move_map_left()
            elif self.k_d_pressed:
                root.game_manager.gui.game.world_map.move_map_right()
        else:
            self.k_a_pressed = False
            self.k_d_pressed = False
            self.k_s_pressed = False
            self.k_w_pressed = False

    #@logger
    def process_keydown(self, event:py.event.Event):
        if self.process_keydown_for_inputfield(event): return root.update_gui()
        if self.process_keydown_base(event):
            return

        if event.key == py.K_w:
            self.k_w_pressed = True
        elif event.key == py.K_s:
            self.k_s_pressed = True
        elif event.key == py.K_a:
            self.k_a_pressed = True
        elif event.key == py.K_d:
            self.k_d_pressed = True

        elif event.key == py.K_ESCAPE:
            if root.game_manager.command_line.is_active:
                root.game_manager.command_line.deactivete()
            elif not root.game_manager.gui.game.main_info_window_content.closed:
                root.game_manager.gui.game.main_info_window_content_close()
            elif root.game_manager.gui.game.sticked_object != None:
                root.game_manager.gui.game.sticked_object = None
            elif any([root.game_manager.gui.game.jobs_list, root.game_manager.gui.game.buildings_types_list, root.game_manager.gui.game.action_list]):
                root.game_manager.gui.close_all_extra_windows()

        elif event.key == py.K_UP:
            root.cell_size_scale += 1
            if root.cell_size_scale > len(root.cell_sizes)-1:
                root.cell_size_scale = len(root.cell_sizes)-1
            root.game_manager.world_map.resize()
            root.game_manager.gui.change_position_for_new_screen_sizes()
            root.update_gui()

        elif event.key == py.K_DOWN:
            root.cell_size_scale -= 1
            if root.cell_size_scale < 0:
                root.cell_size_scale = 0
            root.game_manager.world_map.resize()
            root.game_manager.gui.change_position_for_new_screen_sizes()
            root.update_gui()

        elif event.key == py.K_CARET:
            if root.game_manager.command_line.is_active:
                root.game_manager.command_line.deactivete()
            else:
                root.game_manager.command_line.activete()

    #@logger
    def process_mousebuttondown(self, event:py.event.Event):
        if self.process_mousebutton_for_inputfield(event): return root.update_gui()
        mouse_pos = event.pos
        if event.button == 1:
            if root.game_manager.gui.game.jobs_list:
                if root.game_manager.gui.game.jobs_list.rect.collidepoint(mouse_pos):
                    root.game_manager.gui.game.jobs_list.click()
                    return

            if root.game_manager.gui.game.action_list:
                if root.game_manager.gui.game.action_list.rect.collidepoint(mouse_pos):
                    root.game_manager.gui.game.action_list.click()
                    return

            if root.game_manager.gui.game.buildings_types_list:
                if root.game_manager.gui.game.buildings_types_list.rect.collidepoint(mouse_pos):
                    root.game_manager.gui.game.buildings_types_list.click()
                    return
                
                for scheme in root.game_manager.gui.game.scheme_list:
                    if scheme.bg_rect.collidepoint(mouse_pos):
                        root.game_manager.gui.game.choise_scheme(scheme)
                        return

            if root.game_manager.gui.game.world_map:
                if root.game_manager.gui.game.world_map.rect.collidepoint(mouse_pos):
                    root.game_manager.gui.close_all_extra_windows()
                    root.game_manager.gui.game.world_map.click(mouse_pos, 1)
                    return

            screen_middle = (root.window_size[0] // 2, root.window_size[1] // 2)

            if mouse_pos[1] < screen_middle[1]:
                for item in root.game_manager.gui.game.header_content:
                    if item.rect.collidepoint(mouse_pos):
                        item.click()
                        return
            elif mouse_pos[1] > screen_middle[1]:
                for item in root.game_manager.gui.game.footer_content:
                    if item.rect.collidepoint(mouse_pos):
                        item.click()
                        return
            #if mouse_pos[0] > screen_middle[0]:
            #    if gui.main_info_window_content:
            #        if gui.main_info_window_content.rect.collidepoint(mouse_pos):
            #            gui.main_info_window_content.click()
            #            return

            root.game_manager.gui.game.main_info_window_content_close()
            root.game_manager.world_map.unchose_cell()
            root.game_manager.gui.close_all_extra_windows()
            root.update_gui()
            
        elif event.button == 3:
            if root.game_manager.gui.game.world_map:
                if root.game_manager.gui.game.world_map.rect.collidepoint(mouse_pos):
                    root.game_manager.gui.close_all_extra_windows()
                    root.game_manager.gui.game.world_map.click(mouse_pos, 3)
                    return

        elif event.button == 4:
            root.cell_size_scale += 1
            if root.cell_size_scale > len(root.cell_sizes)-1:
                root.cell_size_scale = len(root.cell_sizes)-1
            root.game_manager.world_map.resize()
            root.game_manager.gui.change_position_for_new_screen_sizes()
            root.update_gui()

        elif event.button == 5:
            root.cell_size_scale -= 1
            if root.cell_size_scale < 0:
                root.cell_size_scale = 0
            root.game_manager.world_map.resize()
            root.game_manager.gui.change_position_for_new_screen_sizes()
            root.update_gui()
    
    #@logger
    def process_mousemotion(self, event:py.event.Event):
        mouse_pos = event.pos
        if root.game_manager.gui.game.sticked_object:
            root.game_manager.gui.game.sticked_object.change_position(mouse_pos)
            root.update_gui()
            return
        
        rel_mouse_pos = (mouse_pos[0] - root.game_manager.world_map.rect.x - root.game_manager.world_map.x_offset, mouse_pos[1] - root.game_manager.world_map.rect.y - root.game_manager.world_map.y_offset)
        for cell in root.game_manager.world_map.cells_on_screen:
            if cell.rect.collidepoint(rel_mouse_pos):
                self.cell_under_mouse = cell
                return

        self.cell_under_mouse = self._default_cell
        root.game_manager.gui.game.hide_info()