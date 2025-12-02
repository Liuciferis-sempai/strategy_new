import pygame as py
from .. import root
from .buttons import ListButton
from functools import partial

class ListOf(py.sprite.Sprite):
    def __init__(self, list_:list=[], color:tuple[int, int, int]=(255, 255, 255), position:tuple[int, int]=(10, 10), font_size:int=20, open_direction:str="up", window_state: str = "none", func: partial|None = None):
        super().__init__()

        self.height = len(list_)*(font_size+5)
        self.width = root.interface_size
        self.color = color
        if open_direction == "up":
            self.position = (position[0], position[1]-self.height-15)
        else:
            self.position = (position[0], position[1]+self.height+15)
        self.list = list_

        self.image = py.Surface((self.width, self.height))
        self.image.fill(color)
        self.rect = py.Rect(self.position[0], self.position[1], self.width, self.height)

        self.list = [ListButton(e, (self.position[0], self.position[1]+(i*(font_size+5))), button_state=window_state, processor=self) for i, e in enumerate(list_)]
        self.function = func
    
    def draw(self):
        root.screen.blit(self.image, self.rect)
        for button in self.list:
            button.draw()

    def click(self, button_text: str):
        if self.function:
            self.function(button_text)