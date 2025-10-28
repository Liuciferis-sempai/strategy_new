from assets.work_with_files import read_json_file
import pygame as py
import os
import assets.root as root
from .tech import Tech
from assets.root import loading
from assets.functions import update_gui

class Link(py.sprite.Sprite):
    def __init__(self, prerequisite: Tech, tech: Tech):
        super().__init__()

        self.prerequisite = prerequisite
        self.tech = tech

        self.draw()

    def draw(self):
        py.draw.line(root.screen, (255, 0, 0), (self.prerequisite.rect.right, self.prerequisite.rect.centery), (self.tech.rect.left, self.tech.rect.centery))

class Techtree:
    def __init__(self):
        #self.scale = 1.0

        self.techs = []
        loading.draw("Loading technologies...")
        self.load_techs()

        loading.draw("Setting up technology links...")
        self.links = []
        for tech in self.techs:
            if tech.data.get("prerequisites", []) != []:
                for prerequisite in tech.data["prerequisites"]:
                    prerequisite_tech = [t for t in self.techs if t.data.get("id") == prerequisite]
                    if prerequisite_tech:
                        prerequisite_tech = prerequisite_tech[0]
                        link = Link(prerequisite_tech, tech)
                        self.links.append(link)
        self.chosen_tech = None

    def load_techs(self):
        self.techs = []
        for techfile in os.listdir("data/technologies"):
            if techfile.endswith(".json"):
                tech_data = read_json_file(f"data/technologies/{techfile}")
                self.techs.append(Tech(tech_data))

    def collidepoint(self, mouse_pos: tuple[int, int]) -> bool:
        for tech in self.techs:
            if tech.rect.collidepoint(mouse_pos):
                if tech.is_allowed():
                    root.game.allFractions.edit_fraction(id=root.player_id, data={"set": True, "research_technology": tech.data.get("id")})
                    if self.chosen_tech is not None:
                        self.chosen_tech.chosen = False
                        self.chosen_tech.chosen_tech()
                    self.chosen_tech = tech
                    tech.chosen = True
                    tech.chosen_tech()
                    update_gui()
                    return True
        return False

    def set_none_tech(self):
        root.game.allFractions.edit_fraction(id=root.player_id, data={"set": True, "research_technology": "none_technology"})
        if self.chosen_tech is not None:
            self.chosen_tech.chosen = False
            self.chosen_tech.chosen_tech()
        self.chosen_tech = None
        update_gui()
    
    def draw(self):
        for link in self.links:
            link.draw()
        for tech in self.techs:
            tech.draw()

    #def scaling_up(self):
    #    self.scale += 0.1
    #    if self.scale > 2.0:
    #        self.scale = 2.0
    #    print(f"Scaling up: {self.scale}")
    #    for tech in self.techs:
    #        tech.scale(self.scale)
    #    update_gui()
    
    #def scaling_down(self):
    #    self.scale -= 0.1
    #    if self.scale < 0.1:
    #        self.scale = 0.1
    #    print(f"Scaling down: {self.scale}")
    #    for tech in self.techs:
    #        tech.scale(self.scale)
    #    update_gui()
    
    def scroll_up(self):
        for tech in self.techs:
            tech.rect.y += root.interface_size//2
        update_gui()
    
    def scroll_down(self):
        for tech in self.techs:
            tech.rect.y -= root.interface_size//2
        update_gui()
    
    def scroll_left(self):
        for tech in self.techs:
            tech.rect.x += root.interface_size//2
        update_gui()
    
    def scroll_right(self):
        for tech in self.techs:
            tech.rect.x -= root.interface_size//2
        update_gui()