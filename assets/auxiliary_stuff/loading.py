import pygame as py
from .. import root

class Loading:
    def __init__(self):
        self.font = py.font.Font(None, 50)
        self.text_surface = self.font.render("Loading...", False, (255, 255, 255))
        self.text_rect = self.text_surface.get_rect(center=(400, 300))
    
    def draw(self, text: str="Loading..."):
        self.text_surface = self.font.render(text, False, (255, 255, 255))
        self.text_rect = self.text_surface.get_rect(center=py.display.get_surface().get_rect().center)
        screen = py.display.get_surface()
        screen.fill((0, 0, 0))
        screen.blit(self.text_surface, self.text_rect)
        py.display.flip()