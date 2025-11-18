import pygame as py
from .. import root
from ..gui.textfield import TextField
from ..auxiliary_stuff import update_gui

class Messenger:
    def __init__(self, font_size: int = 25, font_color: dict[str, tuple[int, int, int]] = {"info": (255, 255, 255), "warning": (255, 0, 0)}, bg_color: tuple[int, int, int]|tuple[int, int, int, int] = (10, 10, 10, 100), position: tuple[int, int] = (10, 10), line_lifespan: int = 5):
        self.font_size = font_size
        self.font_color = font_color
        self.bg_color = bg_color
        self.position = position
        self.line_lifespan = line_lifespan*root.config["FPS"]

        self.last_tick = 0

        self.lines: list[tuple[int, TextField]] = []

    def print(self, message: str, message_type: str = "info"):
        self.lines.append(
            (self.last_tick, TextField(bg_color=self.bg_color, font_color=self.font_color[message_type], font_size=self.font_size, text=f"{message}", width=0, height=0, width_as_text_width=True))
        )
        self.change_position()

    def change_position(self, new_position: tuple[int, int] = (-1, -1)):
        if new_position != (-1, -1):
            self.position = new_position

        for i, (_, line) in enumerate(self.lines):
            line.change_position((self.position[0], self.position[1]+(line.text_rect.height+10)*i))
        update_gui()
    
    def tick(self):
        self.last_tick += 1
        to_remove = []
        for tick, line in self.lines:
            if tick+self.line_lifespan > self.last_tick:
                to_remove.append((tick, line))
        if to_remove != []:
            for item in to_remove:
                self.lines.remove(item)
            self.change_position()
    
    def draw(self):
        for _, line in self.lines:
            line.draw()