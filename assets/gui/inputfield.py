import pygame as py
import assets.root as root
from assets.root import loading, logger, language

class InputField(py.sprite.Sprite):
    def __init__(self, width: int = 0, height: int = 0, position: tuple[int, int] = (10, 10), place_holder: str = "", font_size: int = 20, bg_color: tuple[int, int, int, int] = (0, 0, 0, 0), ch_color: tuple[int, int, int, int] = (0, 255, 0, 255), input_processor=None, hidden: bool = False):
        super().__init__()
        self.width = width
        self.height = height
        self.position = position
        self.place_holder = place_holder
        self.value = ""
        self.font_size = font_size
        self.bg_color = bg_color
        self.hidden = hidden

        self.processor = input_processor

        self.image = py.Surface((width, height))
        self.image.fill(self.bg_color)
        if len(self.bg_color) == 4: self.image.set_alpha(self.bg_color[-1])

        self.ch_image = py.Surface((width+10, height+10))
        self.ch_image.fill(ch_color)

        self.ch_rect = self.ch_image.get_rect()
        self.ch_rect.topleft = (self.position[0]-5, self.position[1]-5)

        self.rect = self.image.get_rect()
        self.rect.topleft = self.position

        self.font = py.font.Font(None, font_size)
        self.update_text_surface()

    def __repr__(self) -> str:
        return f"<InputField {self.processor} {self.value} {self.place_holder}>"

    def update_text_surface(self):
        text = self.value if self.value != "" else self.place_holder
        if root.input_field_active: text += "<"
        self.text_surface = self.font.render(text, True, (0, 0, 0))
        self.text_rect = self.text_surface.get_rect(topleft=(self.position[0] + 5, self.position[1] + (self.height - self.text_surface.get_height()) // 2))
    
    def draw(self):
        if root.input_field_active:
            root.screen.blit(self.ch_image, self.ch_rect)
        root.screen.blit(self.image, self.rect)
        root.screen.blit(self.text_surface, self.text_rect)

    def click(self):
        root.game_manager.chose_input_field(self)
        root.input_field_active = True
        self.update_text_surface()
    
    def key_down(self, event: py.event.Event):
        if event.key == py.K_ESCAPE:
            root.game_manager.reset_chosen_inputfield()
            root.input_field_active = False
        elif event.key == py.K_BACKSPACE:
            self.value = self.value[:-1]
        elif event.key == py.K_RETURN:
            if self.processor != None:
                self.processor.process_input(self.value)
            else:
                root.game_manager.reset_chosen_inputfield()
                root.input_field_active = False
        else:
            self.value += event.unicode
        self.update_text_surface()

    def change_size(self, new_width:int, new_height:int):
        self.width = new_width
        self.height = new_height

        self.image = py.Surface((self.width, self.height))
        self.image.fill(self.bg_color)

        self.rect = self.image.get_rect()
        self.rect.topleft = self.position

        self.update_text_surface()
    
    def change_position(self, new_position: tuple[int, int]):
        self.position = new_position
        self.rect.topleft = new_position
        self.ch_rect.topleft = (new_position[0]-5, new_position[1]-5)
        self.text_rect.topleft = new_position
        self.draw()