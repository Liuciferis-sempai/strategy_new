from typing import Any
import pygame as py
from .. import root

class TextField(py.sprite.Sprite):
    def __init__(
            self,
            width:int=0,
            height:int=0,
            font_color: tuple[int, int, int] = (0, 0, 0),
            bg_color:tuple[int, int, int]|tuple[int, int, int, int]=(255, 255, 255),
            position:tuple[int, int]=(10, 10),
            padding: int = 5,
                padding_top_bottom: int|None = None,
                padding_top: int|None = None,
                padding_bottom: int|None = None,
                padding_left_right: int|None = None,
                padding_left: int|None = None,
                padding_right: int|None = None,
            text:str="",
            font_size:int=40,
            translate: bool = True,
            positioning: str = "left",
            auto_width: bool = True,
            auto_height: bool = True,
            text_kwargs: dict[str, Any]={}
            ):
        super().__init__()
        if len(bg_color) == 3:
            bg_color = (bg_color[0], bg_color[1], bg_color[2], 255)

        if not padding_left_right: padding_left_right = padding
        if not padding_top_bottom: padding_top_bottom = padding
        
        self.padding_left = padding_left if padding_left else padding_left_right
        self.padding_right = padding_right if padding_right else padding_left_right
        self.padding_top = padding_top if padding_top else padding_top_bottom
        self.padding_bottom = padding_bottom if padding_bottom else padding_top_bottom

        self.width = width + self.padding_left + self.padding_right
        self.height = height + self.padding_top + self.padding_bottom
        self.font_color = font_color
        self.bg_color = bg_color
        self.position = position
        self.text = text
        self.font_size = font_size
        self.translate = translate
        self.positioning = positioning
        self.auto_width = auto_width
        self.auto_height = auto_height
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
        self.image.set_alpha(self.bg_color[3])
        self.rect = self.image.get_rect()
        self.change_position(self.position)

    def render_text(self):
        self.text_surface = self.font.render(self.text, True, self.font_color)
        self.text_rect = self.text_surface.get_rect()

        need_set_image = False
        if self.auto_width:
            self.width = self.text_rect.width + self.padding_right + self.padding_left
            need_set_image = True
        if self.auto_height:
            self.height = self.text_rect.height + self.padding_bottom + self.padding_top
            need_set_image = True
        
        if need_set_image: self.set_image()

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