from typing import Any
import pygame as py
from .. import root

class TextField(py.sprite.Sprite):
    def __init__(self, width:int=0, height:int=0, font_color: tuple[int, int, int] = (0, 0, 0), bg_color:tuple[int, int, int]|tuple[int, int, int, int]=(255, 255, 255), position:tuple[int, int]=(10, 10), text:str="", font_size:int=40, translate: bool = True, positioning: str = "left", width_as_text_width: bool = True, text_kwargs: dict[str, Any]={}):
        super().__init__()

        self.width = width
        self.height = height
        self.font_color = font_color
        self.bg_color = bg_color
        self.position = position
        self.text = text
        self.font_size = font_size
        self.translate = translate
        self.positioning = positioning
        self.width_as_text_width = width_as_text_width
        self.text_kwargs = text_kwargs

        self.font = py.font.Font(None, font_size)

        self.set_text(self.text, self.text_kwargs)
        self.set_image()

    def set_text(self, new_text: str, text_kwargs: dict[str, Any] = {}, new_font_size: int = -1):
        if new_font_size > 0:
            self.font_size = new_font_size
            self.font = py.font.Font(None, new_font_size)
        if self.translate: self.text = root.language.get(new_text, text_kwargs)
        else: self.text = new_text
        
        self.render_text()
    
    def set_image(self):
        self.image = py.Surface((self.width, self.height), py.SRCALPHA)
        self.image.fill(self.bg_color)
        if len(self.bg_color) == 4: self.image.set_alpha(self.bg_color[-1])
        self.rect = self.image.get_rect()
        self.change_position(self.position)

    def render_text(self):
        self.text_surface = self.font.render(self.text, True, self.font_color)
        self.text_rect = self.text_surface.get_rect()

        if self.width_as_text_width:
            self.width = self.text_rect.width
            self.set_image()
    
    def change_position(self, new_position: tuple[int, int]):
        self.position = new_position
        if self.positioning == "left":
            self.rect.topleft = self.position
            self.text_rect.topleft = (self.position[0]+5, self.position[1]+5)
        elif self.positioning == "right":
            self.rect.topright = self.position
            self.text_rect.topright = (self.position[0]+5, self.position[1]+5)
    
    def draw(self):
        root.screen.blit(self.image, self.rect)
        root.screen.blit(self.text_surface, self.text_rect)