import pygame as py
from ... import root
from ...auxiliary_stuff import update_gui
from ...root import logger
from typing import Any

class Button(py.sprite.Sprite):
    def __init__(self, text:str="Button", img:str="", width:int=0, height:int=0, color:tuple[int, int, int]|tuple[int, int, int, int]=(255, 255, 255), font_size:int=20, font_color: tuple[int, int, int] = (0, 0, 0), position:tuple[int, int]=(5, 5), text_kwargs: dict[str, Any] = {}, button_state: str = "none", auto_process: bool = True, auto_width: bool = False, translate: bool = True):
        super().__init__()
        if len(color) == 3:
            color = (color[0], color[1], color[2], 255)
        self.name = str(self.__class__).split(".")[-1].replace("'>", "")

        self.text = text
        self.text_kwargs = text_kwargs
        self.width = width if width > 0 else root.button_standard_size[0]
        self.height = height if height > 0 else root.button_standard_size[1]
        self.color = color
        self.font_color = font_color
        self.font_size = font_size
        self.position = position

        self.auto_process = auto_process
        self.auto_width = auto_width
        self.translate = translate

        self.font = py.font.Font(None, font_size)

        self.img = img
        self.set_text(self.text, self.text_kwargs)
        self.set_image()

        root.game_manager.add_button(self, button_state)

    def __repr__(self) -> str:
        return f"<{self.name}>"
    
    def click(self, button: int, mouse_pos: tuple[int, int]) -> bool:
        logger.info(f"Button '{self}' clicked", "Button.click()")
        #print(f"{self.text} button clicked!")
        return True

    def draw(self):
        root.screen.blit(self.image, self.rect)
        root.screen.blit(self.text_surface, self.text_rect)

    def change_position(self, new_position:tuple[int, int]):
        self.position = new_position
        self.rect.topleft = new_position
        self.text_rect.topleft = (new_position[0]+5, new_position[1]+self.rect.height//2-self.font_size//2)

    def set_text(self, new_text: str, text_kwargs: dict[str, Any] = {}, new_font_size: int = -1):
        if new_font_size > 0:
            self.font_size = new_font_size
            self.font = py.font.Font(None, new_font_size)
        if self.translate: self.text = root.language.get(new_text, text_kwargs)
        else: self.text = new_text
        
        self.render_text()
    
    def set_image(self):
        if self.img != "":
            self.image = root.image_manager.get_image(f"data/icons/{self.img}")
            self.image = py.transform.scale(self.image, (self.width, self.height))
        else:
            self.image = py.Surface((self.width, self.height), py.SRCALPHA)
            self.image.fill(self.color)
        self.image.set_alpha(self.color[3])

        self.rect = self.image.get_rect()
        self.change_position(self.position)

    def render_text(self):
        self.text_surface = self.font.render(self.text, True, self.font_color)
        self.text_rect = self.text_surface.get_rect()

        if self.auto_width:
            self.width = self.text_rect.width
            self.set_image()