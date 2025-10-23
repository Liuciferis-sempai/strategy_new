import pygame as py
import assets.root as root

class Icon(py.sprite.Sprite):
    def __init__(self, width:int=0, height:int=0, color:tuple[int, int, int]=(255, 255, 255), position:tuple[int, int]=(10, 10), img:str="", spec_path:str="data/icons", bg:tuple[int, int, int, int]=(0, 0, 0, 0)):
        super().__init__()
        self.width = width
        self.height = height
        self.img = img
        self.color = color
        self.position = position
        
        if img != "":
            self.image = root.image_manager.get_image(f"{spec_path}/{img}", f"{spec_path}/none.png")
        else:
            self.image = py.Surface((self.width, self.height), py.SRCALPHA)
        self.bg_image = py.Surface((self.width, self.height), py.SRCALPHA)
        self.bg_image.fill(bg)
        self.bg_rect = self.bg_image.get_rect(topleft=position)
        self.image = py.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect(topleft=position)

        self.draw()

    def draw(self):
        self.bg_image.blit(self.image, (0, 0))
        root.screen.blit(self.bg_image, self.bg_rect)

    def change_position(self, position: tuple[int, int]):
        self.position = position
        self.rect.topleft = position
        self.bg_rect.topleft = position
        self.draw()