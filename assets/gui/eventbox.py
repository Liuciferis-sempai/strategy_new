from typing import Any
import pygame as py
from .. import root
from ..auxiliary_stuff import *

class EventBox(py.sprite.Sprite):
    def __init__(
            self,
            event_id: str = "unknow",
            width: int = 0, height: int = 0,
            event_titel: str = "unknow", event_titel_kwargs: dict = {},
            event_desc: str = "unknow", event_desc_kwargs: dict = {},
            event_choices: list[tuple[str, dict[str, Any], tuple[int, int, int]]] = [("unknow", {}, (0, 0, 0))],
            event_context: dict|None = None,
            font_size: int = 30, font_color: tuple[int, int, int] = (0, 0, 0),
            titel_color: None|tuple[int, int, int] = None,
            desc_color: None|tuple[int, int, int] = None,
            background: str|tuple[int, int, int, int]|tuple[int, int, int] = (220, 220, 220),
            auto_height: bool = True,
            translate: bool = True
            ):
        super().__init__()
        self.event_id = event_id
        self.width = width if width > 0 else root.interface_size*3
        self.height = height

        if event_context:
            if is_empty(event_titel_kwargs): event_titel_kwargs = event_context
            if is_empty(event_desc_kwargs): event_desc_kwargs = event_context
            for _, choice_kwargs, _ in event_choices:
                if is_empty(choice_kwargs):
                    choice_kwargs = event_context
        self.event_context = event_context

        if not titel_color: titel_color = font_color
        if not desc_color: desc_color = font_color

        self.font = py.font.Font(None, font_size)

        self.titel = event_titel if not translate else root.language.get(event_titel, event_titel_kwargs)
        self.titel_surface = self.font.render(self.titel, True, titel_color)
        self.titel_rect = self.titel_surface.get_rect()
        
        self.desc = event_desc if not translate else root.language.get(event_desc, event_desc_kwargs)
        text = wrap_text(self.desc, self.width, self.font)

        self.desc_surface = py.Surface((self.width, font_size*len(text)), py.SRCALPHA)
        for i, t in enumerate(text):
            desc_surface = self.font.render(t, True, desc_color)
            self.desc_surface.blit(desc_surface, (5, font_size*i))
        self.desc_rect = self.desc_surface.get_rect()
        
        self.choices: list[tuple[py.Surface, py.Rect, str]] = []
        for event_choice, choice_kwargs, choice_color in event_choices:
            if translate: event_choice = root.language.get(event_choice, choice_kwargs)
            choice_surface = self.font.render(event_choice, True, choice_color)
            self.choices.append((choice_surface, choice_surface.get_rect(), event_choice))

        if auto_height:
            self.height = 20
            self.height += self.titel_rect.height
            self.height += self.desc_rect.height
            for _, choice_rect, _ in self.choices:
                self.height += choice_rect.height
        
            if self.height < root.window_size[1]//2:
                self.height = root.window_size[1]//2
    
        self.titel_rect.center = (root.window_size[0]//2, root.window_size[1]//2-self.height//2+font_size+5)
        self.desc_rect.center = (root.window_size[0]//2, root.window_size[1]//2-self.height//2+font_size+5+self.titel_rect.height+self.desc_rect.height//2)

        for i, (_, choice_rect, _) in enumerate(self.choices):
            choice_rect.center = (root.window_size[0]//2, root.window_size[1]//2+self.height//2-(font_size//2+5)*(len(self.choices)-i))

        if isinstance(background, str):
            self.background = root.image_manager.get_image(f"{background}")
        elif len(background) == 3:
            self.background_color = (background[0], background[1], background[2], 255)
            self.background = py.Surface((self.width, self.height), py.SRCALPHA)
            self.background.fill(self.background_color)
        else:
            self.background_color = background
            self.background = py.Surface((self.width, self.height), py.SRCALPHA)
            self.background.fill(self.background_color)

        self.background_rect = self.background.get_rect()
        self.background_rect.center = (root.window_size[0]//2, root.window_size[1]//2)
    
    def draw(self):
        root.screen.blit(self.background, self.background_rect)
        root.screen.blit(self.titel_surface, self.titel_rect)
        root.screen.blit(self.desc_surface, self.desc_rect)
        
        for choice_surface, choice_rect, _ in self.choices:
            root.screen.blit(choice_surface, choice_rect)
    
    def click(self, mouse_pos: tuple[int, int]) -> bool:
        for _, choice_rect, choice_name in self.choices:
            if choice_rect.collidepoint(mouse_pos):
                root.game_manager.event_manager.event_choice(self.event_id, choice_name.strip(), self.event_context)
                return True
        
        if self.background_rect.collidepoint(mouse_pos): return True
        return False