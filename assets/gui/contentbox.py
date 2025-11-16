import pygame as py
import root
from .auxiliary_stuff import update_gui

class ContentBox(py.sprite.Sprite):
    def __init__(self, width:int=0, height:int=0, color:tuple[int, int, int]=(255, 255, 255), position:tuple[int, int]=(10, 10), value:int=0, img:str="", allowed_range:list[int]|None=[0, 100], font_size: int = 20):
        super().__init__()
        self.width = width if width > 0 else root.info_box_size[0]
        self.height = height if height > 0 else root.info_box_size[1]
        self.font_size = font_size
        self.color = color
        self.position = position
        self.value = value
        self.allowed_range = allowed_range

        self.bg = py.Surface((self.width, self.height))
        self.bg.fill(color)
        if img == "":
            self.image = py.Surface((self.width, self.height))
            self.image.fill(color)
        else:
            try:
                self.image = root.image_manager.get_image(f"data/icons/{img}")
            except FileNotFoundError:
                try:
                    self.image = root.image_manager.get_image(f"data/{img}")
                except FileNotFoundError:
                    self.image = root.image_manager.get_image("data/icons/none.png")
            self.image = py.transform.scale(self.image, (self.width, self.height))
        self.rect = py.Rect(position[0], position[1], self.width, self.height)

        self.font = py.font.Font(None, font_size)

        self.value_surface = self.font.render(str(value), False, (0, 255, 0))
        self.value_rect = self.value_surface.get_rect(topleft=(position[0] - 5, 10))

        self.draw()
    
    def get_value(self) -> int:
        return self.value
    
    def set_value(self, new_value:int) -> bool:
        if self.allowed_range is not None:
            if len(self.allowed_range) == 2:
                if new_value < self.allowed_range[0] or new_value > self.allowed_range[1]:
                    return False
        self._change_value_surface_and_rect(new_value)
        return True

    def change_value(self, change:int) -> bool:
        new_value = self.value + change
        return self.set_value(new_value)

    def _change_value_surface_and_rect(self, new_value:int):
        self.value = new_value
        self.value_surface = self.font.render(str(self.value), False, (0, 255, 0))
        update_gui()
    
    def change_position(self, new_position:tuple[int, int]):
        self.position = new_position
        self.rect.topleft = new_position
        self.value_rect.topleft = (new_position[0] - 5, new_position[1])
        self.draw()
    
    def draw(self):
        self.bg.blit(self.image, (0, 0))
        self.bg.blit(self.value_surface, self.value_rect)
        root.screen.blit(self.bg, self.rect)