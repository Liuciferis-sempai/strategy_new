from typing import Any
import pygame as py
import assets.root as root

class InfoBox(py.sprite.Sprite):
    def __init__(self, title:str="Title", text:str="Description", width:int=0, height:int=0, color:tuple[int, int, int]=(255, 255, 255), font_size:int=40, position:tuple[int, int]=(5, 5)):
        super().__init__()
        self.title = title
        self.text = text
        self.width = width if width > 0 else root.interface_size*2
        self.height = height if height > 0 else root.interface_size*3
        self.color = color
        self.font_size = font_size
        self.position = position

        self.closed = False

        self.image = py.Surface((self.width, self.height))
        self.image.fill(color)
        self.rect = py.Rect(position[0], position[1], self.width, self.height)

        self.font = py.font.Font(None, font_size)
        self.title_surface = self.font.render(root.language.get(title), False, (0, 0, 0))
        self.title_rect = self.title_surface.get_rect(center=(self.width // 2, 20))
        self.image.blit(self.title_surface, self.title_rect)

        #text wrapping
        line_length = self.width - 20
        wrapped_text = [""]
        for line in root.language.get(text).splitlines():
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
            line.get_rect(center=(self.width // 2, 40 + i * (self.font_size + 5))) for i, line in enumerate(self.lines_surface)
        ]

        self.draw()

    def click(self):
        #print(f"{self.title} box clicked!")
        self.close()

    def draw(self):
        if not self.closed:
            self.image.blit(self.title_surface, self.title_rect)
            for i, line_surface in enumerate(self.lines_surface):
                self.image.blit(line_surface, self.text_rect[i])
            root.screen.blit(self.image, self.rect)

    def change_position(self, new_position:tuple[int, int]):
        self.position = new_position
        self.rect.topleft = new_position
        for i, _ in enumerate(self.lines_surface):
            self.text_rect[i].topleft = (new_position[0] + 10, new_position[1] + 40 + i * (self.font_size + 5))
        self.draw()

    def close(self):
        self.closed = True
        self.image.fill((0, 0, 0, 0))
        root.handler.world_map.unchose_cell()
        if not root.handler.is_opened_pawn_default():
            root.handler.reset_opened_pawn()


    def open(self, content:dict[str, Any]):
        self.closed = False
        self.title = content.get("title", "No Title")
        self.text = content.get("text", "No Description")
        
        self._update_title()
        self._update_text()

        self.draw()

    def _update_title(self):
        self.title_surface = self.font.render(root.language.get(self.title), False, (0, 0, 0))
        self.title_rect = self.title_surface.get_rect(center=(self.width // 2, 20))

    def _update_text(self):
        line_length = self.width - 20
        wrapped_text = [""]
        for line in self.text.splitlines():
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
            self.font.render(root.language.get(line), False, (0, 0, 0)) for line in wrapped_text
        ]
        self.text_rect = [
            line.get_rect(center=(self.width // 2, 40 + i * (self.font_size + 5))) for i, line in enumerate(self.lines_surface)
        ]