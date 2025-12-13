from ...auxiliary_stuff import read_json_file, update_gui, get_cell_side_size
import pygame as py
import os
from ... import root
from .tech import Tech, Link
from ...root import loading
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...gamemanager import GameManager

class Techtree:
    def __init__(self, tech_tree_data: list[dict], fraction_id: int):
        #self.scale = 1.0
        self.fraction_id = fraction_id
        self.move_distance = get_cell_side_size()//4

        self.techs: list[Tech] = []
        for tech in tech_tree_data:
            self.techs.append(Tech(tech))

        self.links: list[Link] = []
        for tech in self.techs:
            if tech.data.get("prerequisites", []) != []:
                for prerequisite in tech.data["prerequisites"]:
                    prerequisite_tech = [t for t in self.techs if t.data.get("id") == prerequisite]
                    if prerequisite_tech:
                        prerequisite_tech = prerequisite_tech[0]
                        link = Link(prerequisite_tech, tech)
                        self.links.append(link)
        self.chosen_tech = None

    def __repr__(self) -> str:
        return f"<Techtree has {len(self.techs)} Techs>"

    def get_tech(self, tech_id: str) -> Tech:
        for tech in self.techs:
            if tech.id == tech_id:
                return tech

        return root.game_manager.get_default_technology()

    def collidepoint(self, mouse_pos: tuple[int, int]) -> bool:
        for tech in self.techs:
            if tech.rect.collidepoint(mouse_pos):
                if tech.is_allowed():
                    root.game_manager.fraction_manager.get_fraction_by_id(self.fraction_id).set_research_technology(tech.id)
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
        root.game_manager.fraction_manager.get_fraction_by_id(self.fraction_id).reset_research_technology()
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
            tech.rect.y += self.move_distance
        update_gui()
    
    def scroll_down(self):
        for tech in self.techs:
            tech.rect.y -= self.move_distance
        update_gui()
    
    def scroll_left(self):
        for tech in self.techs:
            tech.rect.x += self.move_distance
        update_gui()
    
    def scroll_right(self):
        for tech in self.techs:
            tech.rect.x -= self.move_distance
        update_gui()