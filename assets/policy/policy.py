import pygame as py
import assets.root as root

class PolicyCard(py.sprite.Sprite):
    def __init__(self, policy_data: dict, pos: tuple[int, int]=(0, 0)):
        super().__init__()
        self.data = policy_data

        self.name = policy_data.get("id", "Unknown Policy")
        self.description = policy_data.get("desc", "No description available.")
        self.icon = policy_data.get("ico", "default_icon.png")
        self.color = policy_data.get("color", "#FFFFFF")
        self.figure = policy_data.get("figure", "square")
        self.number = policy_data.get("number", 0)

        self.image = root.image_manager.get_image(f"data/icons/{self.icon}")
        self.image = py.transform.scale(self.image, (root.interface_size, root.interface_size*2))
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

        self.font = py.font.Font(None, 20)

        self.title = self.font.render(self.name, True, (0, 0, 0))
        self.title_rect = self.title.get_rect(center=(self.rect.width // 2, 20))

        self.description_surface = self.font.render(self.description, True, (0, 0, 0))
        self.description_rect = self.description_surface.get_rect(topleft=(10, 40))

        self.figure_size = (root.interface_size//2.9, root.interface_size//2.9)

        if self.figure == "circle":            
            self.figure_surface = py.Surface(self.figure_size, py.SRCALPHA)
            py.draw.circle(self.figure_surface, py.Color(self.color), (self.figure_size[0] // 2, self.figure_size[1] // 2), self.figure_size[0] // 2)
            self.figure_pos = (root.interface_size-5-root.interface_size//2.9, root.interface_size*2-6-root.interface_size//2.9)
    
        elif self.figure == "triangle":
            self.figure_surface = py.Surface(self.figure_size, py.SRCALPHA)
            points = [(self.figure_size[0]//2, 0), (0, self.figure_size[1]), self.figure_size]
            py.draw.polygon(self.figure_surface, py.Color(self.color), points)
            self.figure_pos = (root.interface_size-5-root.interface_size//2.9, root.interface_size*2-6-root.interface_size//2.9)
    
        elif self.figure == "pentagon":
            self.figure_surface = py.Surface(self.figure_size, py.SRCALPHA)
            points = [(self.figure_size[0]//2, 0), (self.figure_size[0], self.figure_size[1]//2), (self.figure_size[0], self.figure_size[1]*3//2), (0, self.figure_size[1]*3//2), (0, self.figure_size[1]//2)]
            py.draw.polygon(self.figure_surface, py.Color(self.color), points)
            self.figure_pos = (root.interface_size-5-root.interface_size//2.9, root.interface_size*2-6-root.interface_size//2.9)

        elif self.figure == "hexagon":
            self.figure_surface = py.Surface(self.figure_size, py.SRCALPHA)
            points = [(self.figure_size[0]//2, self.figure_size[1]), (0, self.figure_size[1]//2+self.figure_size[1]//4), (0, self.figure_size[1]//2-self.figure_size[1]//4), (self.figure_size[0]//2, 0), (self.figure_size[0], self.figure_size[1]//2-self.figure_size[1]//4), (self.figure_size[0], self.figure_size[1]//2+self.figure_size[1]//4)]
            py.draw.polygon(self.figure_surface, py.Color(self.color), points)
            self.figure_pos = (root.interface_size-5-root.interface_size//2.9, root.interface_size*2-6-root.interface_size//2.9)

        elif self.figure == "octagon":
            self.figure_surface = py.Surface(self.figure_size, py.SRCALPHA)
            points = [(self.figure_size[0]//2+self.figure_size[1]//4, self.figure_size[1]), (self.figure_size[0]//2-self.figure_size[1]//4, self.figure_size[1]), (0, self.figure_size[1]//2+self.figure_size[1]//4), (0, self.figure_size[1]//2-self.figure_size[1]//4), (self.figure_size[0]//2-self.figure_size[1]//4, 0), (self.figure_size[0]//2+self.figure_size[1]//4, 0), (self.figure_size[0], self.figure_size[1]//2-self.figure_size[1]//4), (self.figure_size[0], self.figure_size[1]//2+self.figure_size[1]//4)]
            py.draw.polygon(self.figure_surface, py.Color(self.color), points)
            self.figure_pos = (root.interface_size-5-root.interface_size//2.9, root.interface_size*2-6-root.interface_size//2.9)

        else: #square
            self.figure_surface = py.Surface(self.figure_size)
            self.figure_surface.fill(py.Color(self.color))
            self.figure_pos = (root.interface_size-5-root.interface_size//2.9, root.interface_size*2-6-root.interface_size//2.9)
    
        self.number_surface = self.font.render(str(self.number), True, (0, 0, 0))
        self.number_rect = self.number_surface.get_rect(center=(self.figure_surface.get_width() // 2, self.figure_surface.get_height() // 2))
        self.figure_surface.blit(self.number_surface, self.number_rect)
        self.image.blit(self.figure_surface, self.figure_pos)
        self.image.blit(self.title, self.title_rect)
        self.image.blit(self.description_surface, self.description_rect)
    
    def __repr__(self) -> str:
        return f"<PolicyCard {self.name} with args: {self.color} {self.figure} {self.number}>"

    def change_position(self, new_position: tuple[int, int]):
        self.rect.topleft = new_position
    
    def draw(self):
        self.number_surface = self.font.render(str(self.number), True, (0, 0, 0))
        self.number_rect = self.number_surface.get_rect(center=(self.rect.width // 2, (self.rect.height - 60) // 2))
        self.figure_surface.blit(self.number_surface, self.number_rect)
        self.image.blit(self.figure_surface, self.figure_pos)
        self.image.blit(self.title, self.title_rect)
        self.image.blit(self.description_surface, self.description_rect)
        root.screen.blit(self.image, self.rect)
    
    def get_info(self) -> dict:
        return {"name": self.name, "description": self.description, "icon": self.icon, "color": self.color, "figure": self.figure, "number": self.number}