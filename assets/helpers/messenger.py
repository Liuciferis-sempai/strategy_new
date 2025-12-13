import pygame as py
from .. import root
from ..gui.buttons import *
from ..auxiliary_stuff import update_gui
from typing import Any

class Messenger:
    def __init__(self, font_size: int = 25, font_color: dict[str, tuple[int, int, int]] = {"info": (255, 255, 255), "warning": (255, 0, 0)}, bg_color: tuple[int, int, int]|tuple[int, int, int, int] = (100, 100, 100, 180), position: tuple[int, int] = (10, 10), line_lifespan: int = 4):
        self.font_size = font_size
        self.font_color = font_color
        self.bg_color = bg_color
        self.position = position
        self.line_lifespan = line_lifespan*root.config["FPS"]

        self.last_tick = 0

        self.lines: list[tuple[int, MessageLine]] = []
        self.buffer = None

    def set_buffer(self, message: str, message_kwargs: dict[str, Any] = {}, messanger_target: None|tuple[int, int, int] = None, message_type: str = "info"):
        self.buffer = (message, message_kwargs, messanger_target, message_type)
    
    def print_buffer(self):
        if self.buffer:
            try:
                self.print(self.buffer[0], self.buffer[1], self.buffer[2], self.buffer[3])
            except:
                root.logger.error(f"false buffer value: {self.buffer}", "messenger.print_buffer(...)")
        self.buffer = None

    def print(self, message: str, message_kwargs: dict[str, Any] = {}, messanger_target: None|tuple[int, int, int] = None, message_type: str = "info"):
        if len(self.lines) == 0: self.last_tick = 0
        self.lines.append(
            (self.last_tick+100*len(self.lines),
             MessageLine(
                bg_color=self.bg_color,
                font_color=self.font_color[message_type],
                font_size=self.font_size, text=f"{message}",
                height=self.font_size,
                text_kwargs=message_kwargs,
                button_state=root.window_state,
                messanger_target=messanger_target
             )
            )
        )
        self.change_position()

    def change_position(self, new_position: tuple[int, int] = (-1, -1)):
        if new_position != (-1, -1):
            self.position = new_position

        for i, (_, line) in enumerate(self.lines):
            line.change_position((self.position[0], self.position[1]+(line.text_rect.height+10)*i))
        update_gui()
    
    def tick(self):
        if len(self.lines) == 0: return
        self.last_tick += 1
        old_line_lenght = len(self.lines)
        self.lines = [(tick, line) for tick, line in self.lines if tick + self.line_lifespan > self.last_tick]
        if old_line_lenght != len(self.lines):
            self.change_position()
    
    def draw(self):
        for _, line in self.lines: line.draw()