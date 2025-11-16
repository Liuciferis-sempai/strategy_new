import pygame as py
from ... import root
from ...auxiliary_stuff import update_gui
from ...root import language, logger

class Button(py.sprite.Sprite):
    def __init__(self, text:str="Button", img:str="", width:int=0, height:int=0, color:tuple[int, int, int]|tuple[int, int, int, int]=(255, 255, 255), font_size:int=20, position:tuple[int, int]=(5, 5)):
        super().__init__()
        self.name = str(self.__class__).split(".")[-1].replace("'>", "")

        self.text = text
        self.width = width if width > 0 else root.button_standard_size[0]
        self.height = height if height > 0 else root.button_standard_size[1]
        self.color = color
        self.font_size = font_size
        self.position = position

        #self.image = py.Surface((self.width, self.height))
        #self.image.fill(color)
        #self.rect = py.Rect(position[0], position[1], self.width, self.height)

        self.img = img
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

    def __repr__(self) -> str:
        return f"<{self.name}>"
    
    def click(self):
        logger.info(f"Button '{self}' clicked", "Button.click()")
        #print(f"{self.text} button clicked!")
        pass

    def draw(self):
        self.image.blit(self.text_surface, self.text_rect)
        root.screen.blit(self.image, self.rect)
    
    def change_position(self, new_position:tuple[int, int]):
        self.position = new_position
        self.rect.topleft = new_position
        self.text_rect.center = (self.width // 2, self.height // 2)
        self.draw()