import pygame as py
import assets.root as root
from assets.world.cell import Cell
from assets.functions import logging
from assets.functions import update_gui

class InputKeyProcessor:
    def __init__(self):
         
        self.is_ctrl_pressed = False
        self.is_shift_pressed = False
        self.is_alt_pressed = False

        self.k_a_pressed = False
        self.k_d_pressed = False
        self.k_s_pressed = False
        self.k_w_pressed = False

        #self.scale_index = 4

        self.cell_under_mouse = Cell()

    def is_move_button_pressed(self):
        if any([self.k_a_pressed, self.k_d_pressed, self.k_s_pressed, self.k_w_pressed]):
            return True

    def move(self):
        if root.window_state == "game":
            if self.k_w_pressed:
                root.handler.gui.game.world_map.move_map_up()
            elif self.k_s_pressed:
                root.handler.gui.game.world_map.move_map_down()
            if self.k_a_pressed:
                root.handler.gui.game.world_map.move_map_left()
            elif self.k_d_pressed:
                root.handler.gui.game.world_map.move_map_right()
        else:
            self.k_a_pressed = False
            self.k_d_pressed = False
            self.k_s_pressed = False
            self.k_w_pressed = False
        
    #PROCESS_KEYDOWN----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #@logger
    def process_keydown(self, event:py.event.Event):
        self.process_keydown_base(event) #will be replaced in root.change_window_state

    #@logger
    def process_keydown_base(self, event:py.event.Event) -> bool:
        if event.key == py.K_LCTRL or event.key == py.K_RCTRL:
            self.is_ctrl_pressed = True
            return True
        elif event.key == py.K_LSHIFT or event.key == py.K_RSHIFT:
            self.is_shift_pressed = True
            return True
        elif event.key == py.K_LALT or event.key == py.K_RALT:
            self.is_alt_pressed = True
            return True

        elif event.key == py.K_ESCAPE:
            timed_variable = root.window_state
            root.window_state = root.last_window_state
            root.last_window_state = timed_variable
            update_gui()
        return False

    #@logger
    def process_keydown_game(self, event:py.event.Event):
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
            if not root.handler.gui.game.main_info_window_content.closed:
                root.handler.gui.game.main_info_window_content_close()
            elif root.handler.gui.game.sticked_object != None:
                root.handler.gui.game.sticked_object = None
            elif any([root.handler.gui.game.jobs_list, root.handler.gui.game.buildings_types_list, root.handler.gui.game.action_list]):
                root.handler.gui.game.hide_jobs()
                root.handler.gui.game.hide_action_list()
                root.handler.gui.game.hide_scheme_list()
        elif event.key == py.K_UP:
            root.cell_size_scale += 1
            if root.cell_size_scale > len(root.cell_sizes)-1:
                root.cell_size_scale = len(root.cell_sizes)-1
            root.handler.world_map.resize()
            root.handler.gui.change_position_for_new_screen_sizes()
            update_gui()
        elif event.key == py.K_DOWN:
            root.cell_size_scale -= 1
            if root.cell_size_scale < 0:
                root.cell_size_scale = 0
            root.handler.world_map.resize()
            root.handler.gui.change_position_for_new_screen_sizes()
            update_gui()

    #@logger
    def process_keydown_writing(self, event:py.event.Event):
        if self.process_keydown_base(event):
            return
        
        if event.key == py.K_RETURN:
            root.handler.gui.writing.submit_input()
        elif event.key == py.K_BACKSPACE:
            root.input = root.input[:-1]
        elif event.key == py.K_ESCAPE:
            root.handler.gui.writing.close(False)
        else:
            if len(root.input) < 20:
                root.input += event.unicode
        root.handler.gui.writing.update_input_field()

    #@logger
    def process_keydown_building(self, event:py.event.Event):
        if self.process_keydown_base(event):
            return
        if event.key == py.K_ESCAPE:
                root.change_window_state("game")

    #@logger
    def process_keydown_reciept(self, event:py.event.Event):
        if self.process_keydown_base(event):
            return
        if event.key == py.K_ESCAPE:
                root.change_window_state("building")
                root.handler.gui.reciept.reciept_y_offset = 0

    #@logger
    def process_keydown_technology(self, event:py.event.Event):
        if self.process_keydown_base(event):
            return
        if event.key == py.K_w:
            root.handler.tech_tree.scroll_up()
        elif event.key == py.K_s:
            root.handler.tech_tree.scroll_down()
        elif event.key == py.K_a:
            root.handler.tech_tree.scroll_left()
        elif event.key == py.K_d:
            root.handler.tech_tree.scroll_right()
        elif event.key == py.K_ESCAPE:
            root.change_window_state("game")
    
    #@logger
    def process_keydown_policy(self, event:py.event.Event):
        if self.process_keydown_base(event):
            return
        if event.key == py.K_ESCAPE:
            root.change_window_state("game")

    #@logger
    def process_keydown_fraction(self, event:py.event.Event):
        if self.process_keydown_base(event):
            return
        if event.key == py.K_ESCAPE:
            root.change_window_state("game")
    
    #@logger
    def process_keydown_share_menu(self, event:py.event.Event):
        if self.process_keydown_base(event):
            return
        if event.key == py.K_ESCAPE:
            root.change_window_state("game")

    #@logger
    def process_keydown_inventory(self, event:py.event.Event):
        if self.process_keydown_base(event):
            return
        if event.key == py.K_ESCAPE:
            root.change_window_state("game")

    #PROCESS_KEYUP------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #@logger
    def process_keyup(self, event:py.event.Event):
        if event.key == py.K_LCTRL or event.key == py.K_RCTRL:
            self.is_ctrl_pressed = False
            return
        elif event.key == py.K_LSHIFT or event.key == py.K_RSHIFT:
            self.is_shift_pressed = False
            return
        elif event.key == py.K_LALT or event.key == py.K_RALT:
            self.is_alt_pressed = False
            return
        elif root.window_state == "game":
            if event.key == py.K_w:
                self.k_w_pressed = False
            elif event.key == py.K_s:
                self.k_s_pressed = False
            elif event.key == py.K_a:
                self.k_a_pressed = False
            elif event.key == py.K_d:
                self.k_d_pressed = False

    #PROCESS_MOUSEDOWN--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #@logger
    def process_mousebuttondown(self, event:py.event.Event):
        pass #will be replaced in root.change_window_state

    #@logger
    def process_mousebuttondown_game(self, event:py.event.Event):
        mouse_pos = event.pos
        if event.button == 1:
            if root.handler.gui.game.jobs_list:
                if root.handler.gui.game.jobs_list.rect.collidepoint(mouse_pos):
                    root.handler.gui.game.jobs_list.click()
                    return

            if root.handler.gui.game.action_list:
                if root.handler.gui.game.action_list.rect.collidepoint(mouse_pos):
                    root.handler.gui.game.action_list.click()
                    return

            if root.handler.gui.game.buildings_types_list:
                if root.handler.gui.game.buildings_types_list.rect.collidepoint(mouse_pos):
                    root.handler.gui.game.buildings_types_list.click()
                    return
                
                for scheme in root.handler.gui.game.scheme_list:
                    if scheme.bg_rect.collidepoint(mouse_pos):
                        root.handler.gui.game.choise_scheme(scheme)
                        return

            if root.handler.gui.game.world_map:
                if root.handler.gui.game.world_map.rect.collidepoint(mouse_pos):
                    root.handler.gui.game.hide_jobs()
                    root.handler.gui.game.hide_action_list()
                    root.handler.gui.game.hide_scheme_list()
                    root.handler.gui.game.world_map.click(mouse_pos, 1)
                    return

            screen_middle = (root.window_size[0] // 2, root.window_size[1] // 2)

            if mouse_pos[1] < screen_middle[1]:
                for item in root.handler.gui.game.header_content:
                    if item.rect.collidepoint(mouse_pos):
                        item.click()
                        return
            elif mouse_pos[1] > screen_middle[1]:
                for item in root.handler.gui.game.footer_content:
                    if item.rect.collidepoint(mouse_pos):
                        item.click()
                        return
            #if mouse_pos[0] > screen_middle[0]:
            #    if gui.main_info_window_content:
            #        if gui.main_info_window_content.rect.collidepoint(mouse_pos):
            #            gui.main_info_window_content.click()
            #            return

            root.handler.gui.game.main_info_window_content_close()
            root.handler.gui.game.hide_jobs()
            root.handler.gui.game.hide_action_list()
            update_gui()
            
        elif event.button == 3:
            if root.handler.gui.game.world_map:
                if root.handler.gui.game.world_map.rect.collidepoint(mouse_pos):
                    root.handler.gui.game.hide_jobs()
                    root.handler.gui.game.hide_action_list()
                    root.handler.gui.game.hide_scheme_list()
                    root.handler.gui.game.world_map.click(mouse_pos, 3)
                    return

        elif event.button == 4:
            root.cell_size_scale += 1
            if root.cell_size_scale > len(root.cell_sizes)-1:
                root.cell_size_scale = len(root.cell_sizes)-1
            root.handler.world_map.resize()
            root.handler.gui.change_position_for_new_screen_sizes()
            update_gui()

        elif event.button == 5:
            root.cell_size_scale -= 1
            if root.cell_size_scale < 0:
                root.cell_size_scale = 0
            root.handler.world_map.resize()
            root.handler.gui.change_position_for_new_screen_sizes()
            update_gui()
    
    #@logger
    def process_mousebuttondown_fraction(self, event:py.event.Event):
        mouse_pos = event.pos
        if root.handler.gui.fraction.fraction_name_edit_button.rect.collidepoint(mouse_pos):
                root.handler.gui.fraction.fraction_name_edit_button.click()
        update_gui()
    
    #@logger
    def process_mousebuttondown_writting(self, event:py.event.Event):
        mouse_pos = event.pos
        if root.handler.gui.writing.submit_button.rect.collidepoint(mouse_pos):
                root.handler.gui.writing.submit_button.click()
        update_gui()

    #@logger
    def process_mousebuttondown_building(self, event:py.event.Event):
        mouse_pos = event.pos
        if event.button == 1:
            if root.handler.gui.building.building_reciept_button.rect.collidepoint(mouse_pos):
                root.handler.gui.building.building_reciept_button.click()
        update_gui()
    
    #@logger
    def process_mousebuttondown_share_menu(self, event:py.event.Event):
        mouse_pos = event.pos
        if event.button in [1, 3]:
            for cell, _ in root.handler.gui.sharemenu.share_starter_inventory:
                if cell.rect.collidepoint(mouse_pos):
                    root.handler.gui.sharemenu.click(cell, "starter", event.button)
                    return
            if isinstance(root.handler.gui.sharemenu.share_target_inventory, list):
                for cell, _ in root.handler.gui.sharemenu.share_target_inventory:
                    if cell.rect.collidepoint(mouse_pos):
                        root.handler.gui.sharemenu.click(cell, "target", event.button)
                        return
            elif isinstance(root.handler.gui.sharemenu.share_starter_inventory, dict):
                for inventory_type in root.handler.gui.sharemenu.share_target_inventory.keys(): #type: ignore
                    for cell, _ in root.handler.gui.sharemenu.share_target_inventory[inventory_type]:
                        if cell.rect.collidepoint(mouse_pos):
                            root.handler.gui.sharemenu.click(cell, "target", event.button)
                            return

    #@logger
    def process_mousebuttondown_reciept(self, event:py.event.Event):
        mouse_pos = event.pos
        if event.button == 1 and root.handler.gui.reciept.reciepts != None:
            root.handler.reciept_manager.use_recipe(mouse_pos)
        elif event.button == 4:
            root.handler.gui.reciept.reciept_y_offset += root.interface_size//8
        elif event.button == 5:
            root.handler.gui.reciept.reciept_y_offset -= root.interface_size//8
        update_gui()
    
    #@logger
    def process_mousebuttondown_policy(self, event:py.event.Event):
        mouse_pos = event.pos
        if event.button == 4:
            root.handler.policy_table.scroll_up()
        elif event.button == 5:
            root.handler.policy_table.scroll_down()
        update_gui()
    
    #@logger
    def process_mousebuttondown_technology(self, event:py.event.Event):
        mouse_pos = event.pos
        if event.button == 1:
            root.handler.tech_tree.collidepoint(mouse_pos)
        elif event.button == 3:
            root.handler.tech_tree.set_none_tech()
        elif event.button == 4:
            if self.is_shift_pressed:
                root.handler.tech_tree.scroll_left()
            else:
                root.handler.tech_tree.scroll_up()
        elif event.button == 5:
            if self.is_shift_pressed:
                root.handler.tech_tree.scroll_right()
            else:
                root.handler.tech_tree.scroll_down()
        update_gui()

    #@logger
    def process_mousebuttondown_inventory(self, event:py.event.Event):
        mouse_pos = event.pos
        #if root.handler.gui.inventory.owner_inventory:
        #    if event.button == 1:
        #        for cell, _ in root.handler.gui.inventory.owner_inventory:
        #            if cell.rect.collidepoint(mouse_pos):
        #                root.handler.gui.inventory.click(event.button)
        #                return
        #    elif event.button == 3:
        #        for cell, _ in root.handler.gui.inventory.owner_inventory:
        #            if cell.rect.collidepoint(mouse_pos):
        #                root.handler.gui.inventory.click(event.button)
        #                return

    #PROCESS_MOUSEUP----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #@logger
    def process_mousebuttonup(self, event:py.event.Event):
        pass #there are no functions yet

    #PROCESS_MOUSEMOTION------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #@logger
    def process_mousemotion(self, event:py.event.Event):
        pass #there are no functions yet

    #@logger
    def process_mousemotion_game(self, event:py.event.Event):
        mouse_pos = event.pos
        if root.handler.gui.game.sticked_object:
            root.handler.gui.game.sticked_object.change_position(mouse_pos)
            update_gui()
            return
        
        for coord in root.handler.buildings_manager.buildings.keys():
            coord = (int(coord[1]), int(coord[4]))
            rel_mouse_pos = (mouse_pos[0] - root.handler.world_map.rect.x - root.handler.world_map.x_offset, mouse_pos[1] - root.handler.world_map.rect.y - root.handler.world_map.y_offset)
            cell = root.handler.world_map.get_cell_by_coord(coord)
            if cell.rect.collidepoint(rel_mouse_pos):
                if self.cell_under_mouse != cell:
                    self.cell_under_mouse = cell
                    root.handler.gui.game.show_building_info(coord, mouse_pos)
                    root.update_gui()
                    return
            root.handler.gui.game.hide_building_info()
        for pawn in root.handler.pawns_manager.pawns:
            cell = root.handler.world_map.get_cell_by_coord(pawn.coord)
            rel_mouse_pos = (mouse_pos[0] - root.handler.world_map.rect.x - root.handler.world_map.x_offset, mouse_pos[1] - root.handler.world_map.rect.y - root.handler.world_map.y_offset)
            if cell.rect.collidepoint(rel_mouse_pos):
                root.handler.gui.game.show_pawn_info(pawn, mouse_pos)
                root.update_gui()
                return
        root.handler.gui.game.hide_building_info()