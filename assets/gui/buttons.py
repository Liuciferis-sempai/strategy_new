import pygame as py
import assets.root as root
from assets.functions import update_gui
from assets.root import language, logger

class Button(py.sprite.Sprite):
    def __init__(self, text:str="Button", img:str="", width:int=0, height:int=0, color:tuple[int, int, int]|tuple[int, int, int, int]=(255, 255, 255), font_size:int=20, position:tuple[int, int]=(5, 5)):
        super().__init__()

        self.text = text
        self.width = width if width > 0 else root.button_standard_size[0]
        self.height = height if height > 0 else root.button_standard_size[1]
        self.color = color
        self.font_size = font_size
        self.position = position

        #self.image = py.Surface((self.width, self.height))
        #self.image.fill(color)
        #self.rect = py.Rect(position[0], position[1], self.width, self.height)

        if img != "":
            self.image = root.image_manager.get_image(f"data/icons/{img}")
            self.image = py.transform.scale(self.image, (self.width, self.height))
        else:
            self.image = py.Surface((self.width, self.height))
            self.image.fill(color)
        self.rect = py.Rect(position[0], position[1], self.width, self.height)

        self.font = py.font.Font(None, font_size)
        self.text_surface = self.font.render(language.get(text), False, (0, 0, 0))
        self.text_rect = self.text_surface.get_rect(center=(self.width // 2, self.height // 2))
        self.image.blit(self.text_surface, self.text_rect)
    
    def click(self):
        logger.info(f"Button '{self.text}' clicked", "Button.click()")
        #print(f"{self.text} button clicked!")
        pass

    def draw(self):
        self.image.blit(self.text_surface, self.text_rect)
        root.screen.blit(self.image, self.rect)
    
    def change_position(self, new_position:tuple[int, int]):
        self.position = new_position
        self.rect.topleft = new_position
        self.text_rect.center = (self.width // 2, self.height // 2)

#Game's buttons
class FractionButton(Button):
    def __init__(self):
        super().__init__(text="Fraction", width=100, height=50, color=(200, 200, 200), font_size=20, position=(10, 10))
    
    def click(self):
        super().click()
        root.change_window_state("fraction")
        root.game.gui.fraction.open_player_fraction()

class TechnologyButton(Button):
    def __init__(self):
        super().__init__(text="Technology", width=100, height=50, color=(200, 200, 200), font_size=20, position=(10, 10))
    
    def click(self):
        super().click()
        root.change_window_state("technology")
        root.game.gui.technology.open()

class PolicyButton(Button):
    def __init__(self):
        super().__init__(text="Policy", width=100, height=50, color=(200, 200, 200), font_size=20, position=(10, 10))
    
    def click(self):
        super().click()
        root.change_window_state("policy")
        root.game.gui.policy.open()
    
class NextTurnButton(Button):
    def __init__(self):
        super().__init__(text="", img="next_turn.png", width=50, height=50, color=(200, 200, 200), font_size=20, position=(10, 10))

    def click(self):
        super().click()
        #gui.gui.turn_counter.change_value(1) #после сделать нормальную функцию для смены хода
        root.game.turn_manager.do_step()

class BuildingButton(Button):
    def __init__(self):
        super().__init__(text="Open", width=100, height=50, color=(200, 200, 200), font_size=20, position=(10, 10))

    def click(self):
        super().click()
        root.game.gui.building.open()
        root.change_window_state("building")
        update_gui()

class RecieptButton(Button):
    def __init__(self):
        super().__init__(text="Reciept", width=100, height=50, color=(200, 200, 200), font_size=20, position=(10, 10))

    def click(self):
        super().click()
        root.game.gui.building.open()
        root.game.gui.reciept.open()
        root.change_window_state("reciept")
        update_gui()

class OpenInventoryButton(Button):
    def __init__(self):
        super().__init__(text="Inventory", width=100, height=50, color=(200, 200, 200), font_size=20, position=(10, 10))

    def click(self):
        super().click()
        root.game.gui.inventory.open()
        root.change_window_state("inventory")
        update_gui()

class JobButton(Button):
    def __init__(self, text:str, position:tuple[int, int]):
        super().__init__(text=text, width=200, height=20, color=(200, 200, 200), font_size=20, position=position)

class ShowJobButton(Button):
    def __init__(self):
        super().__init__(text="Job", width=100, height=50, color=(200, 200, 200), font_size=20, position=(10, 10))

    def click(self):
        super().click()
        root.game.gui.game.show_jobs()

class SchemeListButton(Button):
    def __init__(self):
        super().__init__(text="Schemes", width=100, height=50, color=(200, 200, 200), font_size=20, position=(10, 10))
    
    def click(self):
        super().click()
        root.game.gui.game.open_scheme_list()
        update_gui()

#Fraction's buttons
class FractionNameEditButton(Button):
    def __init__(self):
        super().__init__(text="Edit", width=50, height=50, color=(200, 200, 200, 0), font_size=20, position=(10, 10))
    
    def click(self):
        super().click()
        root.change_window_state("writing")
        root.game.gui.writing.writing = "Fraction Name"
        root.game.gui.writing.start_writing()

class InputSubmitButton(Button):
    def __init__(self):
        super().__init__(text="Submit", width=100, height=50, color=(200, 200, 200), font_size=20, position=(10, 10))
    
    def click(self):
        super().click()
        root.game.gui.writing.submit_input()

#Building's buttons
class WorkbenchButton(Button):
    def __init__(self):
        super().__init__(text="", img="reciept.png", width=100, height=100, position=(10, 10))

    def click(self):
        super().click()
        root.game.gui.reciept.open()
        root.change_window_state("reciept")
        update_gui()

class UpgradeBuildingButton(Button):
    def __init__(self):
        super().__init__(text="upgrade", width=100, height=50, position=(10, 10))

    def click(self):
        super().click()
        root.game.buildings_manager.get_building_by_coord(root.game.get_chosen_cell_coord()).set_upgrade_mod(True)
        root.change_window_state("game")
        update_gui()