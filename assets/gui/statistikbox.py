import pygame as py
from .. import root

class Statistikbox(py.sprite.Sprite):
    def __init__(self, width:int=0, height:int=0, color:tuple[int, int, int]=(255, 255, 255), position:tuple[int, int]=(10, 60), data:dict={}, font_size:int=20):
        super().__init__()
        self.width = width if width > 0 else root.window_size[0]-20
        self.height = height if height > 0 else root.interface_size*2
        self.color = color
        self.position = position
        self.data = data.copy()
        self.font_size = font_size

        self.image = py.Surface((self.width, self.height))
        self.image.fill(color)
        self.rect = py.Rect(position[0], position[1], self.width, self.height)

        self.font = py.font.Font(None, 20)

        self._wrapping_text(data)
    
    def draw(self):
        for i, line_surface in enumerate(self.lines_surface):
            self.image.blit(line_surface, self.text_rect[i])
        root.screen.blit(self.image, self.rect)

    def change_position(self, position: tuple[int, int]):
        self.position = position
        self.rect.topleft = position
    
    def update_statistics(self, data:dict={}):
        self._wrapping_text(data)
    
    def _wrapping_text(self, data:dict={}):
        text = _convert_data(data)
        line_length = self.width - 20
        wrapped_text = [""]
        for line in text.splitlines():
            words = line.split(" ")
            current_line = ""
            for word in words:
                if self.font.size(current_line + word)[0] <= line_length:
                    current_line += word + " "
                else:
                    wrapped_text.append(current_line.strip())
                    current_line = word + " "
            if current_line:
                wrapped_text.append(current_line.strip())

        self.lines_surface = [
            self.font.render(line, False, (0, 0, 0)) for line in wrapped_text
        ]
        self.text_rect = [
            line.get_rect(topleft=(10, 10 + i * (self.font_size + 5))) for i, line in enumerate(self.lines_surface)
        ]

def _convert_data(data:dict) -> str:
    text = ""
    for key, value in data.items():
        key = root.language.get(key)
        value = root.language.get(value)
        text = text + " " + key + " " + str(value) + "\n"
    return text