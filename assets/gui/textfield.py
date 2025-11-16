from typing import Any
import pygame as py
import assets.root as root

class TextField(py.sprite.Sprite):
    def __init__(self, width:int|str=0, height:int|str=0, font_color: tuple[int, int, int] = (0, 0, 0), bg_color:tuple[int, int, int]|tuple[int, int, int, int]=(255, 255, 255), position:tuple[int, int]=(10, 10), text:str="", font_size:int=40, translate: bool = True):
        super().__init__()
        self.text = text
        self.font_color = font_color
        self.position = position
        self.translate = translate

        self.font = py.font.Font(None, font_size)
        self.width, self.height = (0, 0)
        self.set_text(self.text)

        if isinstance(width, int) and isinstance(height, int):
            self.width = width if width >= 0 else root.window_size[0] - 20
            self.height = height if height >= 0 else root.interface_size
            self.update_text_surface()
        else:
            self.width = self.text_rect.width
            self.height = self.text_rect.height

        self.bg_color = bg_color
        self.font_size = font_size

        self.image = py.Surface((self.width, self.height))
        self.image.fill(bg_color)
        if len(self.bg_color) == 4: self.image.set_alpha(self.bg_color[-1])
        self.rect = py.Rect(position[0], position[1], self.width, self.height)
    
    def update_text_surface(self):
        self.text_surface = self.font.render(str(self.text), True, self.font_color)
        self.text_rect = self.text_surface.get_rect(topleft=(self.position[0] + 5, self.position[1] + (self.height - self.text_surface.get_height()) // 2))
    
    def set_text(self, new_text:str):
        if self.translate:
            self.text = root.language.get(new_text)
        else:
            self.text = str(new_text)
        self.update_text_surface()
    
    def draw(self):
        root.screen.blit(self.image, self.rect)
        root.screen.blit(self.text_surface, self.text_rect)

    def change_position(self, position: tuple[int, int]):
        self.position = position
        self.rect.topleft = position
        self.text_rect.topleft = (position[0] + 5, position[1] + (self.height - self.text_surface.get_height()) // 2)
        self.draw()