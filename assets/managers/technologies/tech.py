import pygame as py
from ... import root
import copy

class Tech(py.sprite.Sprite):
    def __init__(self, tech_data: dict = {}, is_default: bool = True):
        super().__init__()
        self.id: str = tech_data.get("id", "unknow")
        self.data = tech_data
        self.chosen = False
        self.is_default = is_default
        if self.is_default:
            root.logger.warning("created default tech", f"Tech.__init__(...)")

        self.background_color = (4, 239, 255)
        self.background_surface = py.Surface((root.interface_size*2+10, root.interface_size+10))
        self.background_surface.fill((0, 0, 0, 0))

        self.image = py.Surface((root.interface_size*2, root.interface_size))
        self.image.fill((50, 50, 255))
        self.rect = self.image.get_rect()
        self.rect.topleft = ((root.interface_size*3)*tech_data.get("x", 0)+20, (root.interface_size*2)*tech_data.get("y", 0)+20)

        self.font = py.font.Font(None, 20)

        self.title = self.font.render(root.language.get(tech_data.get("id", "Unknown Tech")), False, (0, 0, 0))
        self.title_rect = self.title.get_rect(center=(self.rect.width // 2, 20))

        self.description = self.font.render(root.language.get(tech_data.get("description", "")), False, (0, 0, 0))
        self.description_rect = self.description.get_rect(topleft=(10, 40))

        self.unlocks = [
            self.font.render(root.language.get(unlock), False, (0, 0, 0))
            for unlock in tech_data.get("unlocks", [])
            ]

        self.unlocks_rect = []
        x_offset = int(root.interface_size*1.2)
        y_offset = root.interface_size-20
        for i, unlock in enumerate(self.unlocks):
            rect = unlock.get_rect()
            if y_offset - i*20 < 0:
                x_offset += 100
                y_offset += i*20
            rect.topleft = (x_offset, y_offset - i*20)
            self.unlocks_rect.append(rect)

        self.icon = root.image_manager.get_image("data/icons/"+tech_data.get("icon", "none.png"))
        self.icon = py.transform.scale(self.icon, (root.interface_size//4, root.interface_size//4))
        self.icon_rect = self.icon.get_rect(topleft=(10, 10))

        self.cost: dict[str, int] = tech_data.get("cost", {})
        self.accumulated: dict[str, int] = copy.deepcopy(tech_data.get("cost", {}))
        for resource in self.accumulated:
            self.accumulated[resource] = 0
        
        self.render()
    
    #def scale(self, scale_factor:float):
    #    new_size = (int(self.rect.width * scale_factor), int(self.rect.height * scale_factor))
    #
    #    self.background_color = (4, 239, 255)
    #    self.background_surface = py.Surface(new_size)
    #    self.background_surface.fill((0, 0, 0, 0))
    #
    #    self.image = py.Surface(new_size)
    #    self.image.fill((50, 50, 255))
    #    self.rect = self.image.get_rect()
    #    self.rect.topleft = (((root.interface_size[0]*3)*scale_factor)*self.data.get("x", 0)+20, ((root.interface_size[1]*2)*scale_factor)*self.data.get("y", 0)+20)
    #
    #    self.font = py.font.Font(None, 20)
    #
    #    self.title = self.font.render(root.language.get(self.data.get("id", "Unknown Tech")), False, (0, 0, 0))
    #    self.title_rect = self.title.get_rect(center=(self.rect.width // 2, 20))
    #
    #    self.description = self.font.render(root.language.get(self.data.get("description", "")), False, (0, 0, 0))
    #    self.description_rect = self.description.get_rect(topleft=(10, 40))
    #
    #    self.unlocks = [self.font.render(root.language.get(unlock), False, (0, 0, 0)) for unlock in self.data.get("unlocks", [])]
    #    self.unlocks_rect = [unlock.get_rect(topleft=(root.interface_size[0]*1.25, root.interface_size[1]//2 + i * 20)) for i, unlock in enumerate(self.unlocks)]
    #
    #    self.icon = py.image.load("data/icons/"+self.data.get("icon", "none.png"))
    #    self.icon = py.transform.scale(self.icon, (new_size[0]//4, new_size[1]//4))
    #    self.icon_rect = self.icon.get_rect(topleft=(10, 10))
    #    self.image.blit(self.icon, self.icon_rect)

    def render(self):
        self.image.fill((50, 50, 255))
        self.image.blit(self.title, self.title_rect)
        self.image.blit(self.description, self.description_rect)
        self.image.blit(self.icon, self.icon_rect)

        y_offset = 150
        for resource, count in self.cost.items():
            cost_text = root.language.get("tech_cost", {"tech_res": root.language.get(resource), "acc": self.accumulated[resource], "cost": count})
            cost_surface = self.font.render(cost_text, False, (255, 0, 0) if self.accumulated[resource] < count else (0, 255, 0))
            cost_rect = cost_surface.get_rect(topleft=(10, y_offset))
            self.image.blit(cost_surface, cost_rect)
            y_offset += 20
        
        for unlock, rect in zip(self.unlocks, self.unlocks_rect):
            self.image.blit(unlock, rect)

        self.background_surface.blit(self.image, (5, 5))
    
    def draw(self):
        if self.chosen: self.render()
        root.screen.blit(self.background_surface, self.rect)
    
    def is_allowed(self) -> bool:
        for prerequisite in self.data.get("prerequisites", []):
            if root.game_manager.trigger_manager.has_no_tech(prerequisite, root.player_id):
                return False
        return True

    def chosen_tech(self):
        if self.chosen:
            self.background_surface.fill(self.background_color)
        else:
            self.background_surface.fill((0, 0, 0, 0))
        self.render()

class Link(py.sprite.Sprite):
    def __init__(self, prerequisite: Tech, tech: Tech):
        super().__init__()

        self.prerequisite = prerequisite
        self.tech = tech

    def draw(self):
        py.draw.line(root.screen, (255, 0, 0), (self.prerequisite.rect.right, self.prerequisite.rect.centery), (self.tech.rect.left, self.tech.rect.centery))