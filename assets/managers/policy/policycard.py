import pygame as py
from ... import root
from typing import Any
import copy
from ...auxiliary_stuff import wrap_text, is_color_cold
import math

class PolicyCard(py.sprite.Sprite):
    def __init__(self, policy_data: dict, pos: tuple[int, int]=(0, 0), size: int|float = root.interface_size * 1.6):
        super().__init__()
        policy_data = copy.deepcopy(policy_data)

        self.id = policy_data.get("id")
        self.is_locked = policy_data.get("is_locked", True)
        self.data = policy_data
        self.size = size

        self.name = policy_data.get("id", "Unknown Policy")
        self.description = policy_data.get("desc", "no_desc_found")
        self.info = ""
        self.icon = policy_data.get("ico", "default_icon.png")
        self.color = policy_data.get("color", "#FFFFFF")
        self.figure = policy_data.get("figure", "square")
        self.number = policy_data.get("number", 0)

        self.font = py.font.Font(None, 30)

        self.image = root.image_manager.get_image(f"data/icons/{self.icon}")
        self.image = py.transform.scale(self.image, (self.size, self.size*2))
        self.rect = self.image.get_rect()
        self.update_info()
        self.rect.topleft = pos

        self.title = self.font.render(self.name, True, (0, 0, 0))
        self.title_rect = self.title.get_rect(center=(self.rect.width // 2, 20))

        self.info_surface = [self.font.render(des, True, (0, 0, 0)) for des in self.info]
        self.info_rect = [des.get_rect(topleft=(10, 40+i*40)) for i, des in enumerate(self.info_surface)]

        fs = int(size / 2.9)
        self.figure_size = (fs, fs)
        self.figure_pos = (size - 5 - fs, size * 2 - 6 - fs)
        self.figure_surface = py.Surface(self.figure_size, py.SRCALPHA)
        color = py.Color(self.color)

        def _regular_polygon_points(n: int, w: int, h: int, padding: float = 0.08) -> list[tuple[int, int]]:
            cx, cy = w / 2.0, h / 2.0
            r = min(w, h) / 2.0 * (1.0 - padding)
            pts = []
            for i in range(n):
                angle = -math.pi / 2 + i * (2 * math.pi) / n
                x = cx + r * math.cos(angle)
                y = cy + r * math.sin(angle)
                pts.append((int(x), int(y)))
            return pts

        shape = (self.figure or "square").lower()
        if shape == "circle":
            py.draw.circle(self.figure_surface, color, (fs // 2, fs // 2), fs // 2)
        elif shape == "triangle":
            py.draw.polygon(self.figure_surface, color, _regular_polygon_points(3, fs, fs))
        elif shape == "pentagon":
            py.draw.polygon(self.figure_surface, color, _regular_polygon_points(5, fs, fs))
        elif shape == "hexagon":
            py.draw.polygon(self.figure_surface, color, _regular_polygon_points(6, fs, fs))
        elif shape == "octagon":
            py.draw.polygon(self.figure_surface, color, _regular_polygon_points(8, fs, fs))
        else:  # square / fallback
            self.figure_surface.fill(color)
    
        self.number_surface = self.font.render(str(self.number), True, (0, 0, 0))
        self.number_rect = self.number_surface.get_rect(center=(self.figure_surface.get_width() // 2, self.figure_surface.get_height() // 2))
        self.lock_surface = root.image_manager.get_image("data/icons/lock.png")
        self.lock_surface = py.transform.scale(self.lock_surface, (self.size//2, self.size//2))
        self.lock_rect = self.lock_surface.get_rect(center=(self.image.get_width()//2, self.image.get_height()//2))
        #self.figure_surface.blit(self.number_surface, self.number_rect)
        #self.image.blit(self.figure_surface, self.figure_pos)
        #self.image.blit(self.title, self.title_rect)
        #self.image.blit(self.description_surface, self.description_rect)
        self.blit_fragments()
    
    def __repr__(self) -> str:
        return f"<PolicyCard {self.id}>"
    
    def copy(self) -> "PolicyCard":
        return PolicyCard(self.data, size=self.size)

    def change_position(self, new_position: tuple[int, int]):
        self.rect.topleft = new_position
    
    def check_available_status(self):
        if self.data.get("trigger"):
            if isinstance(self.data["trigger"], list):
                for trigger in self.data["trigger"]:
                    self._is_availble(trigger)
            else:
                self._is_availble(self.data["trigger"])
        elif self.is_locked:
            self.is_locked = False
            self.blit_fragments()
    
    def _is_availble(self, trigger: dict[str, Any]) -> bool:
        if hasattr(root.game_manager.trigger_manager, trigger["type"]):
            trigger_func = getattr(root.game_manager.trigger_manager, trigger["type"])
            is_allowed = trigger_func(**trigger["args"])
            return is_allowed
        return False

    def blit_fragments(self):
        self.image = root.image_manager.get_image(f"data/icons/{self.icon}")
        self.image = py.transform.scale(self.image, (self.size, self.size*2))

        if self.is_locked: self.image.blit(self.lock_surface, self.lock_rect)
        self.figure_surface.blit(self.number_surface, self.number_rect)
        self.image.blit(self.figure_surface, self.figure_pos)
        self.image.blit(self.title, self.title_rect)
        for desc_surf, desc_rect in zip(self.info_surface, self.info_rect):
            self.image.blit(desc_surf, desc_rect)
    
    def draw(self):
        #self.number_surface = self.font.render(str(self.number), True, (0, 0, 0))
        #self.number_rect = self.number_surface.get_rect(center=(self.rect.width // 2, (self.rect.height - 60) // 2))
        root.screen.blit(self.image, self.rect)
    
    def get_info(self) -> dict:
        return {"name": self.name, "description": self.description, "icon": self.icon, "color": self.color, "color_is":  "cord" if is_color_cold(self.color) else "warm", "figure": self.figure, "number": self.number}
    
    def update_info(self):
        self.info = root.language.get(self.description) + "\n"
        if self.data.get("influence"):
            for key, value in self.data["influence"].get("values", {}).items():
                #influence_value = value * self.get_influence_weight()
                if key.endswith("_factor"):
                    translated = root.language.get(key, {f"{key}": f"{value*self.get_influence_weight()}"})
                else:
                    translated = root.language.get(key, {f"{key}": f"{value}"})
                self.info += translated + "\n"
            self.info += root.language.get("policy_weight", {"weight": f"{self.get_influence_weight()}"}) +"\n"
        self.info = wrap_text(self.info, self.rect.width-20) #type: ignore

        self.info_surface = [self.font.render(des, True, (0, 0, 0)) for des in self.info]
        self.info_rect = [des.get_rect(topleft=(10, 40+i*40)) for i, des in enumerate(self.info_surface)]

    def get_influence(self) -> dict:
        return self.data.get("influence", {})

    def get_influence_categories(self) -> list[str]:
        influence = self.get_influence()
        return influence.get("categories", [])
    
    def get_influence_values(self) -> dict[str, Any]:
        influence = self.get_influence()
        return influence.get("values", {})
    
    def get_influence_weight(self) -> float:
        influence = self.get_influence()
        return influence.get("weight", 1.0)
    
    def set_influence_weight(self, new_weight: float):
        if "influence" in self.data:
            self.data["influence"]["weight"] = new_weight