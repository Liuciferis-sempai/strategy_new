from typing import Any
import pygame as py
import assets.root as root

class TextField(py.sprite.Sprite):
    def __init__(self, width:int=0, height:int=0, color:tuple[int, int, int]=(255, 255, 255), position:tuple[int, int]=(10, 10), text:str="", font_size:int=40):
        super().__init__()
        self.width = width if width >= 0 else root.window_size[0] - 20
        self.height = height if height >= 0 else root.interface_size
        self.color = color
        self.position = position
        self.text = text
        self.font_size = font_size

        self.image = py.Surface((self.width, self.height))
        self.image.fill(color)
        self.rect = py.Rect(position[0], position[1], self.width, self.height)

        self.font = py.font.Font(None, font_size)
        self.update_text_surface()
    
    def update_text_surface(self):
        self.text_surface = self.font.render(root.language.get(self.text) if not self._can_be_int(self.text) else str(self.text), True, (0, 0, 0))
        self.text_rect = self.text_surface.get_rect(topleft=(self.position[0] + 5, self.position[1] + (self.height - self.text_surface.get_height()) // 2))
    
    def set_text(self, new_text:str):
        self.text = new_text
        self.update_text_surface()
    
    def draw(self):
        root.screen.blit(self.image, self.rect)
        root.screen.blit(self.text_surface, self.text_rect)

    def change_position(self, position: tuple[int, int]):
        self.position = position
        self.rect.topleft = position
        self.text_rect.topleft = (position[0] + 5, position[1] + (self.height - self.text_surface.get_height()) // 2)
        self.draw()

    def _can_be_int(self, text: str) -> bool:
        try:
            int(text)
            return True
        except:
            return False