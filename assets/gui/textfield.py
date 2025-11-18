from typing import Any
import pygame as py
from .. import root

class TextField(py.sprite.Sprite):
    def __init__(self, width:int=0, height:int=0, font_color: tuple[int, int, int] = (0, 0, 0), bg_color:tuple[int, int, int]|tuple[int, int, int, int]=(255, 255, 255), position:tuple[int, int]=(10, 10), text:str="", font_size:int=40, translate: bool = True, positioning: str = "left", width_as_text_width: bool = False):
        super().__init__()
        self.text = text
        self.font_color = font_color
        self.position = position
        self.translate = translate
        self.positioning = positioning
        self.width_as_text_width = width_as_text_width

        self.font = py.font.Font(None, font_size)
        self.width, self.height = (0, 0)
        self.set_text(self.text)

        if width_as_text_width:
            self.width = self.text_rect.width
            self.height = self.text_rect.height
        else:
            self.width = width if width >= 0 else root.window_size[0] - 20
            self.height = height if height >= 0 else root.interface_size

        self.bg_color = bg_color
        self.font_size = font_size

        self.rect = py.Rect(position[0], position[1], self.width, self.height)

        self.image = py.Surface((self.width, self.height))
        self.image.fill(bg_color)
        if len(self.bg_color) == 4: self.image.set_alpha(self.bg_color[-1])
        self._set_position(position)
    
    def update_text_surface(self):
        self.text_surface = self.font.render(str(self.text), True, self.font_color)
        self.text_rect = self.text_surface.get_rect()
        self._set_text_pisition(self.position)
    
    def set_text(self, new_text:str):
        if self.translate:
            self.text = root.language.get(new_text)
        else:
            self.text = str(new_text)
        self.update_text_surface()
        if hasattr(self, "rect"):
            if self.width_as_text_width and self.rect.width != self.text_rect.width:
                self.rect.width = self.text_rect.width
                self.width = self.text_rect.width
                self.image = py.Surface((self.width, self.height))
                self.image.fill(self.bg_color)
                if len(self.bg_color) == 4: self.image.set_alpha(self.bg_color[-1])
                self._set_position(self.position)
    
    def draw(self):
        root.screen.blit(self.image, self.rect)
        root.screen.blit(self.text_surface, self.text_rect)

    def change_position(self, position: tuple[int, int]):
        self.position = position
        self._set_position(position)

    def _set_position(self, position: tuple[int, int]):
        if self.positioning == "right":
            self.rect.topright = position
            self.text_rect.topright = (position[0] + 5, position[1] + (self.height - self.text_surface.get_height()) // 2)
        else:
            self.rect.topleft = position
            self.text_rect.topleft = (position[0] + 5, position[1] + (self.height - self.text_surface.get_height()) // 2)

    def _set_text_pisition(self, position: tuple[int, int]):
        if self.positioning == "right":
            self.text_rect.topright = (position[0] + 5, position[1] + (self.height - self.text_surface.get_height()) // 2)
        else:
            self.text_rect.topleft = (position[0] + 5, position[1] + (self.height - self.text_surface.get_height()) // 2)