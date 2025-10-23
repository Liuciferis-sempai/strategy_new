import pygame as py
import assets.root as root
from .buttons import JobButton

class ListOf(py.sprite.Sprite):
    def __init__(self, list_:list=[], color:tuple[int, int, int]=(255, 255, 255), position:tuple[int, int]=(10, 10), font_size:int=20, open_direction:str="up", type_of_list="job_list"):
        super().__init__()
        self.type_of_list = type_of_list

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

        self.jobs = [JobButton(e, (self.position[0], self.position[1]+(i*(font_size+5)))) for i, e in enumerate(list_)]
    
    def draw(self):
        root.screen.blit(self.image, self.rect)
        for job in self.jobs:
            job.draw()

    def click(self):
        mouse_pos = py.mouse.get_pos()
        if self.type_of_list == "job_list":
            for job in self.jobs:
                if job.rect.collidepoint(mouse_pos):
                    if not root.handler.is_opened_pawn_default():
                        root.handler.pawns_manager.do_job(root.handler.get_opened_pawn(), job.text)
        elif self.type_of_list == "scheme_list":
            for job in self.jobs:
                if job.rect.collidepoint(mouse_pos):
                    root.handler.gui.game.open_scheme_type(job.text)