from typing import Any
import pygame as py
from .. import root

class AchievmentBox(py.sprite.Sprite):
    def __init__(
        self,
        width:int = 0,
        height:int = 0,
        font_color: tuple[int, int, int] = (0, 0, 0),
            titel_font_color: tuple[int, int, int]|None = None,
            desc_font_color: tuple[int, int, int]|None = None,
        bg_color: tuple[int, int, int]|tuple[int, int, int, int] = (160, 160 ,160),
        ico: str|None = None,
            ico_size: int = 50,
        position: tuple[int, int] = (10, 10),
        titel: str = "unknow",
            titel_kwargs: dict[str, Any] = {},
        desc: str = "unknow desc",
            desc_kwargs: dict[str, Any] = {},
        font_size: int = 40,
            titel_font_size: int|None = None,
            desc_font_size: int|None = None,
        translate: bool = True,
        positioning: str = "left_top",
        auto_height: bool = True,
        auto_width: bool = True
        ):
        super().__init__()
        if len(bg_color) == 3:
            bg_color = (bg_color[0], bg_color[1], bg_color[2], 255)
        self.bg_color = bg_color
        self.font = py.font.Font(None, font_size)
        
        self.width = width
        self.height = height
        self.titel_font_color = titel_font_color if titel_font_color else font_color
        self.desc_font_color = desc_font_color if desc_font_color else font_color
        self.titel_font_size = titel_font_size if titel_font_size else font_size
        self.desc_font_size = desc_font_size if desc_font_size else desc_font_size
        self.titel = titel if not translate else root.language.get(titel, titel_kwargs)
        self.desc = desc if not translate else root.language.get(desc, desc_kwargs)
        self.desc_kwargs = desc_kwargs
        self.ico = ico
        self.ico_size = ico_size
        self.positioning = positioning
        self.position = position
        self.auto_height = auto_height
        self.auto_width = auto_width

        self.render()
        self.set_image()
    
    def set_image(self):
        self.image = py.Surface((self.width, self.height), py.SRCALPHA)
        self.image.fill(self.bg_color)
        self.image.set_alpha(self.bg_color[3])
        self.rect = self.image.get_rect()
        self.change_position(self.position)

    def render(self):
        if self.ico:
            self.ico_surface = root.image_manager.get_image("data/achievments/img"+self.ico, "data/achievments/none.png")
            self.ico_surface = py.transform.scale(self.ico_surface, (self.ico_size, self.ico_size))
            self.ico_rect = self.ico_surface.get_rect()

        self.titel_surface = self.font.render(self.titel, True, self.titel_font_color)
        self.titel_rect = self.titel_surface.get_rect()

        self.desc_surface = self.font.render(self.desc, True, self.desc_font_color)
        self.desc_rect = self.desc_surface.get_rect()

        need_set_image = False
        if self.auto_width:
            self.width = self.titel_rect.width if self.titel_rect.width > self.desc_rect.width else self.desc_rect.width
            if self.ico: self.width += self.ico_size + 10
            need_set_image = True
        if self.auto_height:
            self.height = self.titel_rect.height + self.desc_rect.height + 20
            need_set_image = True
        
        if need_set_image: self.set_image()
    
    def change_position(self, new_position: tuple[int, int]):
        self.position = new_position
        if "left" in self.positioning:
            self.rect.left = self.position[0]
        elif "right" in self.positioning:
            self.rect.right = self.position[0]
        if "top" in self.positioning:
            self.rect.top = self.position[1]
        elif "bottom" in self.positioning:
            self.rect.bottom = self.position[1]

        self.titel_rect.topleft = (self.rect.topleft[0]+10, self.rect.topleft[1]+5)
        self.desc_rect.topleft = (self.titel_rect.bottomleft[0], self.titel_rect.bottomleft[1]+10)
        if self.ico:
            self.ico_rect.topleft = (self.rect.topleft[0]+5, self.rect.topleft[1]+5)
            self.titel_rect.left += self.ico_size+5
            self.desc_rect.left += self.ico_size+5
    
    def draw(self):
        root.screen.blit(self.image, self.rect)
        root.screen.blit(self.titel_surface, self.titel_rect)
        root.screen.blit(self.desc_surface, self.desc_rect)
        if self.ico: root.screen.blit(self.ico_surface, self.ico_rect)