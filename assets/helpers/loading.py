import pygame as py
from .. import root

class Loading:
    def __init__(self):
        self.font = py.font.Font(None, 50)
        self.primer_text = "Loading..."
        self.primer_text_surface = self.font.render(self.primer_text, False, (255, 255, 255))
        self.primer_text_rect = self.primer_text_surface.get_rect(center=(400, 300))
    
    def draw(self, sub_text: str="loading...", text: str|None = None):
        screen_center = py.display.get_surface().get_rect().center

        if text == None: text = self.primer_text
        else: self.primer_text = text
        self.primer_text_surface = self.font.render(text, False, (255, 255, 255))
        self.primer_text_rect = self.primer_text_surface.get_rect(center=(screen_center[0], screen_center[1]-50))

        self.seconder_text_surface = self.font.render(sub_text, False, (255, 255, 255))
        self.seconder_text_rect = self.seconder_text_surface.get_rect(center=(screen_center[0], screen_center[1]+50))

        screen = py.display.get_surface()
        screen.fill((0, 0, 0))
        screen.blit(self.primer_text_surface, self.primer_text_rect)
        screen.blit(self.seconder_text_surface, self.seconder_text_rect)
        py.display.flip()